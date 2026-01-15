-- Champs nécessaires pour l'agent (formatage, contexte, audit léger)

alter table public.captures
  add column if not exists title text null,
  add column if not exists raw_input_text text null,
  add column if not exists enriched_json jsonb not null default '{}'::jsonb;

create index if not exists captures_user_title_idx
  on public.captures (user_id, title);


