from __future__ import annotations

from datetime import datetime, timezone

from supabase import Client

from app.agent.gemini_client import GeminiClient, load_gemini_config
from app.agent.json_utils import extract_first_json_object
from app.agent.prompt_builder import build_agent_prompt
from app.agent.types import AgentDecision, AgentIngestRequest, ExistingCaptureSummary


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _make_fallback_decision(raw_input_text: str) -> AgentDecision:
    title = raw_input_text.strip().split("\n", 1)[0].strip()
    title = title[:60] if len(title) > 60 else title
    content = raw_input_text.strip()
    return AgentDecision(
        action="create_new",
        target_capture_id=None,
        category="NOTE",
        title=title or "New capture",
        content=content,
        confidence=0.0,
        reason="Fallback decision (LLM unavailable or invalid output).",
        debug={"fallback": True},
    )


class AgentService:
    async def decide(self, request: AgentIngestRequest, existing: list[ExistingCaptureSummary]) -> AgentDecision:
        if not existing:
            prompt = build_agent_prompt(request.raw_input_text, existing)
        else:
            # On limite le contexte côté appelant; ici on construit juste le prompt.
            prompt = build_agent_prompt(request.raw_input_text, existing)

        try:
            gemini = GeminiClient(load_gemini_config())
            model_text = await gemini.generate_text(prompt)
            raw_json = extract_first_json_object(model_text)
            decision = AgentDecision.model_validate(raw_json)
        except Exception as exc:  # noqa: BLE001
            fallback = _make_fallback_decision(request.raw_input_text)
            fallback.debug["error"] = str(exc)
            return fallback

        if not existing:
            decision.action = "create_new"
            decision.target_capture_id = None

        if decision.action == "update_existing" and not decision.target_capture_id:
            decision.action = "create_new"

        return decision

    def apply_decision(
        self,
        supabase: Client,
        user_id: str,
        request: AgentIngestRequest,
        decision: AgentDecision,
    ) -> dict:
        enriched_json = {
            "agent": {"provider": "gemini"},
            "decision": {
                "action": decision.action,
                "confidence": decision.confidence,
                "reason": decision.reason,
            },
            "content_format": "markdown",
        }

        if decision.action == "update_existing" and decision.target_capture_id:
            update_payload = {
                "title": decision.title,
                "content": decision.content,
                "category": decision.category,
                "classification_status": "done",
                "updated_at": utc_now_iso(),
                "enriched_json": enriched_json,
            }
            result = supabase.table("captures").update(update_payload).eq("id", decision.target_capture_id).execute()
            if getattr(result, "error", None):
                raise RuntimeError(str(result.error))
            if not result.data:
                raise RuntimeError("Target capture not found")
            return result.data[0]

        insert_payload = {
            "user_id": user_id,
            "title": decision.title,
            "content": decision.content,
            "category": decision.category,
            "source": request.source,
            "raw_input_text": request.raw_input_text,
            "classification_status": "done",
            "enriched_json": enriched_json,
        }
        result = supabase.table("captures").insert(insert_payload).execute()
        if getattr(result, "error", None):
            raise RuntimeError(str(result.error))
        if not result.data:
            raise RuntimeError("Supabase insert returned no data")
        return result.data[0]


