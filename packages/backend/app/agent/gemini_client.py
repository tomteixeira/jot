from __future__ import annotations

import os
from dataclasses import dataclass

import httpx


@dataclass(frozen=True, slots=True)
class GeminiConfig:
    api_key: str
    model: str


def load_gemini_config() -> GeminiConfig:
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("Missing required env var: GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL", "").strip() or "gemini-2.0-flash"
    return GeminiConfig(api_key=api_key, model=model)


class GeminiClient:
    def __init__(self, config: GeminiConfig) -> None:
        self._config = config

    async def generate_text(self, prompt: str) -> str:
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self._config.model}:generateContent"
        )
        params = {"key": self._config.api_key}
        payload = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.2, "maxOutputTokens": 800},
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, params=params, json=payload)
            response.raise_for_status()
            data = response.json()

        candidates = data.get("candidates") or []
        if not candidates:
            raise RuntimeError("Gemini returned no candidates")

        content = candidates[0].get("content") or {}
        parts = content.get("parts") or []
        if not parts:
            raise RuntimeError("Gemini returned empty content parts")

        text = (parts[0].get("text") or "").strip()
        if not text:
            raise RuntimeError("Gemini returned empty text")
        return text


