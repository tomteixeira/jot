# Backend (FastAPI) + Supabase

## Objectif

Exposer une API légère pour:
- Créer des **captures** (texte/voix)
- Lister / filtrer (All/TODO/IDEA/NOTE)
- Rechercher (FTS via RPC Supabase)
- Soft-delete

L’auth et l’isolation des données sont gérées par **Supabase Auth + RLS** (`auth.uid()`).

## Variables d’environnement

Copie `packages/backend/env.example` vers ton fichier d’env (ex: `.env` local, non commit).

- `SUPABASE_URL`: URL du projet Supabase
- `SUPABASE_ANON_KEY`: clé anon (publique)
- `SUPABASE_SERVICE_ROLE_KEY` (optionnel): pour endpoints admin (agent) qui bypass RLS
- `ADMIN_TOKEN` (optionnel): secret pour sécuriser les endpoints admin

## Schéma Supabase

Le SQL est dans `packages/backend/supabase/migrations/001_init.sql`.

À appliquer dans Supabase (SQL Editor) ou via Supabase CLI si tu l’utilises.

## Démarrer le backend

Depuis la racine:

```bash
pnpm start:backend
```

Le backend charge l’environnement via `python-dotenv` si tu l’utilises (voir `app/main.py`).


