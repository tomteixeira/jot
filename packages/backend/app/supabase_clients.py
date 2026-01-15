from __future__ import annotations

from supabase import Client, create_client

from app.settings import Settings


def create_user_supabase_client(settings: Settings, access_token: str | None) -> Client:
    """
    Client Supabase utilisé pour les endpoints "user-facing".

    - Utilise la clé ANON
    - Si un JWT est fourni, il est injecté dans PostgREST => RLS s'applique via auth.uid()
    """
    client = create_client(settings.supabase_url, settings.supabase_anon_key)
    if access_token:
        client.postgrest.auth(access_token)
    return client


def create_admin_supabase_client(settings: Settings) -> Client:
    """
    Client Supabase "admin" (service role) pour bypass RLS, uniquement côté serveur.
    """
    if not settings.supabase_service_role_key:
        raise RuntimeError("SUPABASE_SERVICE_ROLE_KEY is required for admin operations")
    return create_client(settings.supabase_url, settings.supabase_service_role_key)


