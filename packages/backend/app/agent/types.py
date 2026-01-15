from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

Category = Literal["TODO", "NOTE"]
AgentAction = Literal["create_new", "update_existing"]


class AgentIngestRequest(BaseModel):
    raw_input_text: str = Field(min_length=1, max_length=50_000)
    source: Literal["text", "voice"] = "text"


class ExistingCaptureSummary(BaseModel):
    id: str
    title: str | None = None
    content: str
    category: Category


class AgentDecision(BaseModel):
    action: AgentAction
    target_capture_id: str | None = None
    category: Category
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1, max_length=50_000)
    confidence: float = Field(ge=0.0, le=1.0)
    reason: str = Field(min_length=1, max_length=1_000)
    debug: dict[str, Any] = Field(default_factory=dict)


class AgentIngestResult(BaseModel):
    decision: AgentDecision
    capture: dict[str, Any]


