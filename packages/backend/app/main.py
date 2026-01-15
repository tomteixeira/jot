from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Header, HTTPException, Query, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from app.agent.service import AgentService
from app.agent.types import AgentIngestRequest, AgentIngestResult, ExistingCaptureSummary
from app.settings import Settings, load_settings
from app.supabase_clients import create_admin_supabase_client, create_user_supabase_client

load_dotenv()

app = FastAPI(title="Jot Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Category = Literal["TODO", "NOTE"]
CaptureSource = Literal["text", "voice"]
ClassificationStatus = Literal["pending", "done", "failed"]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def get_settings() -> Settings:
    return load_settings()


def require_bearer_token(authorization: str | None = Header(default=None)) -> str:
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Authorization header")
    prefix = "Bearer "
    if not authorization.startswith(prefix):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Authorization header")
    token = authorization[len(prefix) :].strip()
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    return token


def require_admin_token(x_admin_token: str | None = Header(default=None)) -> str:
    if not x_admin_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing X-Admin-Token header")
    return x_admin_token


class CaptureCreateRequest(BaseModel):
    content: str = Field(min_length=1, max_length=50_000)
    source: CaptureSource = "text"
    raw_voice_text: str | None = Field(default=None, max_length=50_000)


class CapturePatchRequest(BaseModel):
    content: str | None = Field(default=None, min_length=1, max_length=50_000)
    category: Category | None = None
    is_deleted: bool | None = None
    classification_status: ClassificationStatus | None = None


class CaptureClassificationUpdateRequest(BaseModel):
    category: Category
    classification_status: ClassificationStatus = "done"


def get_user_id_from_access_token(supabase_client, access_token: str) -> str:
    try:
        user = supabase_client.auth.get_user(access_token)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token") from exc

    user_id = getattr(getattr(user, "user", None), "id", None)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to resolve user from token")
    return user_id


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "ts": utc_now_iso()}


@app.post("/captures", status_code=status.HTTP_201_CREATED)
async def create_capture(
    payload: CaptureCreateRequest,
    settings: Settings = Depends(get_settings),
    access_token: str = Depends(require_bearer_token),
) -> dict:
    supabase = create_user_supabase_client(settings, access_token)
    user_id = get_user_id_from_access_token(supabase, access_token)

    insert_payload = {
        "user_id": user_id,
        "content": payload.content,
        "source": payload.source,
        "raw_voice_text": payload.raw_voice_text,
        "category": "NOTE",
        "classification_status": "pending",
    }

    result = supabase.table("captures").insert(insert_payload).execute()
    if getattr(result, "error", None):
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(result.error))
    if not result.data:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Supabase insert returned no data")
    return result.data[0]


@app.get("/captures")
async def list_captures(
    settings: Settings = Depends(get_settings),
    access_token: str = Depends(require_bearer_token),
    category: Category | None = Query(default=None),
    include_deleted: bool = Query(default=False),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[dict]:
    supabase = create_user_supabase_client(settings, access_token)
    query = supabase.table("captures").select("*").order("created_at", desc=True).range(offset, offset + limit - 1)
    if category:
        query = query.eq("category", category)
    if not include_deleted:
        query = query.eq("is_deleted", False)  # noqa: E712
    result = query.execute()
    if getattr(result, "error", None):
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(result.error))
    return result.data or []


@app.get("/captures/search")
async def search_captures(
    q: str = Query(min_length=1, max_length=200),
    settings: Settings = Depends(get_settings),
    access_token: str = Depends(require_bearer_token),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[dict]:
    supabase = create_user_supabase_client(settings, access_token)
    result = supabase.rpc(
        "search_captures", {"search_query": q, "max_rows": limit, "offset_rows": offset}
    ).execute()
    if getattr(result, "error", None):
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(result.error))
    return result.data or []


@app.post("/agent/ingest", response_model=AgentIngestResult)
async def agent_ingest(
    payload: AgentIngestRequest,
    settings: Settings = Depends(get_settings),
    access_token: str = Depends(require_bearer_token),
    context_limit: int = Query(default=20, ge=0, le=50),
) -> AgentIngestResult:
    """
    Base de l'agent:
    - Prend une entrée (raw capture)
    - Regarde les notes existantes du user (RLS)
    - Décide create/update via Gemini
    - Applique la décision (CRUD)
    """
    supabase = create_user_supabase_client(settings, access_token)
    user_id = get_user_id_from_access_token(supabase, access_token)

    existing: list[ExistingCaptureSummary] = []
    if context_limit > 0:
        existing_result = (
            supabase.table("captures")
            .select("id,title,content,category")
            .eq("is_deleted", False)  # noqa: E712
            .order("created_at", desc=True)
            .limit(context_limit)
            .execute()
        )
        if getattr(existing_result, "error", None):
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(existing_result.error))
        existing = [ExistingCaptureSummary.model_validate(row) for row in (existing_result.data or [])]

    agent_service = AgentService()
    decision = await agent_service.decide(payload, existing)

    try:
        capture = agent_service.apply_decision(
            supabase=supabase,
            user_id=user_id,
            request=payload,
            decision=decision,
        )
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc

    return AgentIngestResult(decision=decision, capture=capture)


@app.patch("/captures/{capture_id}")
async def patch_capture(
    capture_id: str,
    payload: CapturePatchRequest,
    settings: Settings = Depends(get_settings),
    access_token: str = Depends(require_bearer_token),
) -> dict:
    supabase = create_user_supabase_client(settings, access_token)
    update_payload: dict[str, object] = {"updated_at": utc_now_iso()}
    if payload.content is not None:
        update_payload["content"] = payload.content
    if payload.category is not None:
        update_payload["category"] = payload.category
    if payload.is_deleted is not None:
        update_payload["is_deleted"] = payload.is_deleted
    if payload.classification_status is not None:
        update_payload["classification_status"] = payload.classification_status

    if len(update_payload) == 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")

    result = supabase.table("captures").update(update_payload).eq("id", capture_id).execute()
    if getattr(result, "error", None):
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(result.error))
    if not result.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Capture not found")
    return result.data[0]


@app.post("/captures/{capture_id}/delete")
async def soft_delete_capture(
    capture_id: str,
    settings: Settings = Depends(get_settings),
    access_token: str = Depends(require_bearer_token),
) -> dict:
    supabase = create_user_supabase_client(settings, access_token)
    result = (
        supabase.table("captures")
        .update({"is_deleted": True, "updated_at": utc_now_iso()})  # noqa: E712
        .eq("id", capture_id)
        .execute()
    )
    if getattr(result, "error", None):
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(result.error))
    if not result.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Capture not found")
    return result.data[0]


def ensure_admin_access(settings: Settings, provided_admin_token: str) -> None:
    if not settings.admin_token:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Admin endpoints disabled (ADMIN_TOKEN not configured)",
        )
    if provided_admin_token != settings.admin_token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid admin token")
    if not settings.supabase_service_role_key:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Admin endpoints disabled (SUPABASE_SERVICE_ROLE_KEY not configured)",
        )


@app.get("/admin/pending-captures")
async def list_pending_captures(
    settings: Settings = Depends(get_settings),
    admin_token: str = Depends(require_admin_token),
    limit: int = Query(default=50, ge=1, le=200),
) -> list[dict]:
    ensure_admin_access(settings, admin_token)
    supabase_admin = create_admin_supabase_client(settings)
    result = (
        supabase_admin.table("captures")
        .select("*")
        .eq("classification_status", "pending")
        .eq("is_deleted", False)  # noqa: E712
        .order("created_at", desc=False)
        .limit(limit)
        .execute()
    )
    if getattr(result, "error", None):
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(result.error))
    return result.data or []


@app.post("/admin/captures/{capture_id}/classification")
async def update_capture_classification(
    capture_id: str,
    payload: CaptureClassificationUpdateRequest,
    settings: Settings = Depends(get_settings),
    admin_token: str = Depends(require_admin_token),
) -> dict:
    ensure_admin_access(settings, admin_token)
    supabase_admin = create_admin_supabase_client(settings)
    result = (
        supabase_admin.table("captures")
        .update(
            {
                "category": payload.category,
                "classification_status": payload.classification_status,
                "updated_at": utc_now_iso(),
            }
        )
        .eq("id", capture_id)
        .execute()
    )
    if getattr(result, "error", None):
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(result.error))
    if not result.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Capture not found")
    return result.data[0]


@app.exception_handler(Exception)
async def unhandled_exception_handler(_: Request, __: Exception):  # type: ignore[override]
    # Évite de leak des détails (les logs sont hors-scope ici).
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


