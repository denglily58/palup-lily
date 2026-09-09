-- Enable realtime updates on event_logs so admin dashboard auto-refreshes
-- Run in Supabase SQL Editor.

alter publication supabase_realtime add table public.event_logs;
alter publication supabase_realtime add table public.chat_logs;
alter publication supabase_realtime add table public.handoff_inbox;
