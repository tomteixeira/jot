from __future__ import annotations

import json


def extract_first_json_object(text: str) -> dict:
    """
    Gemini peut renvoyer du texte autour du JSON.
    On extrait le premier objet JSON plausible.
    """
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("No JSON object found in model output")
    raw = text[start : end + 1]
    return json.loads(raw)



