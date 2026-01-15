from __future__ import annotations

from app.agent.types import ExistingCaptureSummary


def build_agent_prompt(raw_input_text: str, existing_captures: list[ExistingCaptureSummary]) -> str:
    """
    Prompt orienté PRD:
    - vitesse / minimalisme
    - 2 types: TODO / NOTE
    - l'agent agit comme un CRUD: create_new ou update_existing
    """
    existing_block = ""
    if existing_captures:
        lines: list[str] = []
        for item in existing_captures:
            title = item.title or ""
            lines.append(
                f"- id={item.id} | category={item.category} | title={title!r}\n"
                f"  content={item.content!r}"
            )
        existing_block = "\n".join(lines)
    else:
        existing_block = "(none)"

    return f"""
You are an agent for a lightning-fast capture app (Flux/Jot).
Your job: take a NEW raw capture and decide whether to CREATE a new note, or UPDATE an existing note.

Constraints:
- Note types are ONLY: TODO, NOTE
- Output MUST be valid JSON ONLY (no markdown, no explanations outside JSON).
- If no existing notes, action MUST be "create_new".
- The "content" MUST be Markdown.
- Keep the note minimal, clean, and easy to scan.
- When type is TODO: rewrite as a checklist in Markdown (each line starts with "- [ ] ").
- When type is NOTE: rewrite as Markdown with short paragraphs and/or bullet points.
- Title should be short (<= 60 chars), descriptive, no emojis.

Existing notes (most recent first):
{existing_block}

New raw capture:
{raw_input_text!r}

Return JSON with this exact shape:
{{
  "action": "create_new" | "update_existing",
  "target_capture_id": string | null,
  "category": "TODO" | "NOTE",
  "title": string,
  "content": string,
  "confidence": number,
  "reason": string
}}

Decision rules:
- Prefer update_existing if the raw capture is clearly the same topic/project as one existing note.
- Otherwise create_new.
""".strip()


