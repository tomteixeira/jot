-- Flux / Jot - Supabase schema (MVP)
-- Objectif: captures rapides, classification async, recherche, soft delete

create extension if not exists pgcrypto;

create table if not exists public.captures (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  content text not null,
  category text not null default 'NOTE' check (category in ('TODO', 'IDEA', 'NOTE')),
  source text not null default 'text' check (source in ('text', 'voice')),
  created_at timestamptz not null default now(),
  updated_at timestamptz null,
  is_deleted boolean not null default false,
  classification_status text not null default 'pending' check (classification_status in ('pending', 'done', 'failed')),
  raw_voice_text text null,
  content_tsv tsvector generated always as (to_tsvector('simple', coalesce(content, ''))) stored
);

create index if not exists captures_user_created_at_idx
  on public.captures (user_id, created_at desc);

create index if not exists captures_user_category_idx
  on public.captures (user_id, category);

create index if not exists captures_user_is_deleted_idx
  on public.captures (user_id, is_deleted);

create index if not exists captures_content_tsv_idx
  on public.captures using gin (content_tsv);

alter table public.captures enable row level security;

-- RLS policies
create policy "captures_select_own"
  on public.captures
  for select
  using (auth.uid() = user_id);

create policy "captures_insert_own"
  on public.captures
  for insert
  with check (auth.uid() = user_id);

create policy "captures_update_own"
  on public.captures
  for update
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

create policy "captures_delete_own"
  on public.captures
  for delete
  using (auth.uid() = user_id);

-- RPC: recherche (FTS) avec filtre user + soft-delete
create or replace function public.search_captures(
  search_query text,
  max_rows integer default 50,
  offset_rows integer default 0
)
returns setof public.captures
language sql
stable
as $$
  select c.*
  from public.captures c
  where
    c.user_id = auth.uid()
    and c.is_deleted = false
    and (
      search_query is null
      or length(trim(search_query)) = 0
      or c.content_tsv @@ websearch_to_tsquery('simple', search_query)
    )
  order by
    case
      when search_query is null or length(trim(search_query)) = 0 then c.created_at
      else ts_rank(c.content_tsv, websearch_to_tsquery('simple', search_query))
    end desc,
    c.created_at desc
  limit greatest(1, least(max_rows, 200))
  offset greatest(offset_rows, 0);
$$;


