-- LUNA × Lily initial schema
-- Run this in Supabase SQL Editor:
--   Dashboard → SQL Editor → New query → paste → Run

-- ============================
-- event_logs: audit trail
-- ============================
create table if not exists public.event_logs (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id) on delete set null,
  user_email text,
  action text not null,           -- login / logout / chat_query / pin_widget / handoff_taken / ...
  target text,                    -- object being acted on (e.g. widget_id, conversation_id)
  metadata jsonb default '{}'::jsonb,
  timestamp timestamptz not null default now()
);

create index if not exists idx_event_logs_user_id on public.event_logs(user_id);
create index if not exists idx_event_logs_timestamp on public.event_logs(timestamp desc);
create index if not exists idx_event_logs_action on public.event_logs(action);

-- ============================
-- chat_logs: Q7 token/cost tracking (backend writes)
-- ============================
create table if not exists public.chat_logs (
  id uuid primary key default gen_random_uuid(),
  session_id text,
  endpoint text not null,
  model text,
  lang text,
  input_tokens int default 0,
  output_tokens int default 0,
  total_tokens int generated always as (input_tokens + output_tokens) stored,
  latency_ms int,
  cost_usd numeric(10, 6) default 0,
  user_msg_preview text,
  timestamp timestamptz not null default now()
);

create index if not exists idx_chat_logs_session on public.chat_logs(session_id);
create index if not exists idx_chat_logs_timestamp on public.chat_logs(timestamp desc);

-- ============================
-- widgets: B端 pinned dashboard cards
-- ============================
create table if not exists public.widgets (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id) on delete cascade,
  query text not null,
  response_snapshot text,
  chart_config jsonb,
  position int default 0,
  created_at timestamptz not null default now()
);

create index if not exists idx_widgets_user on public.widgets(user_id);

-- ============================
-- handoff_inbox: transfers to human
-- ============================
create table if not exists public.handoff_inbox (
  id uuid primary key default gen_random_uuid(),
  session_id text,
  status text not null default 'pending',  -- pending / in_progress / resolved
  urgency text default 'normal',            -- low / normal / high
  transcript jsonb,
  assigned_to uuid references auth.users(id),
  created_at timestamptz not null default now(),
  resolved_at timestamptz
);

create index if not exists idx_handoff_status on public.handoff_inbox(status);

-- ============================
-- demand_gaps: what buyers asked for that we don't sell
-- ============================
create table if not exists public.demand_gaps (
  id uuid primary key default gen_random_uuid(),
  question text not null,
  product_category text,
  count int default 1,
  first_asked timestamptz not null default now(),
  last_asked timestamptz not null default now(),
  resolved boolean default false
);

create index if not exists idx_demand_gaps_category on public.demand_gaps(product_category);

-- ============================
-- RLS (Row Level Security) — event_logs & widgets scoped to user
-- ============================
alter table public.event_logs enable row level security;
alter table public.widgets enable row level security;
alter table public.handoff_inbox enable row level security;

-- All authenticated merchants can read all event logs (internal audit)
create policy "authenticated can read event_logs" on public.event_logs
  for select to authenticated using (true);

-- Users can only pin/unpin their own widgets
create policy "users manage own widgets" on public.widgets
  for all to authenticated using (auth.uid() = user_id);

-- All authenticated merchants can read handoff inbox (shared queue)
create policy "authenticated can read handoff" on public.handoff_inbox
  for select to authenticated using (true);

-- Service role bypasses RLS (backend writes)
