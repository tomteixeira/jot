from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Settings:
    supabase_url: str
    supabase_anon_key: str
    supabase_service_role_key: str | None
    admin_token: str | None


def load_settings() -> Settings:
    supabase_url = os.getenv("SUPABASE_URL", "").strip()
    supabase_anon_key = os.getenv("SUPABASE_ANON_KEY", "").strip()

    if not supabase_url:
        raise RuntimeError("Missing required env var: SUPABASE_URL")
    if not supabase_anon_key:
        raise RuntimeError("Missing required env var: SUPABASE_ANON_KEY")

    supabase_service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "").strip() or None
    admin_token = os.getenv("ADMIN_TOKEN", "").strip() or None

    return Settings(
        supabase_url=supabase_url,
        supabase_anon_key=supabase_anon_key,
        supabase_service_role_key=supabase_service_role_key,
        admin_token=admin_token,
    )


