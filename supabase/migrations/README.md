# Supabase Migrations

Every schema change lives in a numbered SQL file here. Applied in order via Supabase SQL Editor or `supabase db push` (Supabase CLI).

## Files

| # | File | Applied | What |
|---|---|---|---|
| 001 | `001_initial_tables.sql` | 2026-09-09 | event_logs, chat_logs, widgets, handoff_inbox, demand_gaps + RLS policies |
| 002 | `002_enable_realtime.sql` | 2026-09-09 | Add event_logs / chat_logs / handoff_inbox to `supabase_realtime` publication |

## How to add a new migration

1. `NEW_NUM=003` (next in sequence)
2. `NEW_FILE=$(printf "%03d" $NEW_NUM)_short_description.sql`
3. Write SQL: `CREATE TABLE ...` or `ALTER TABLE ...`
4. **Test locally** first (or use Supabase branch)
5. Apply in prod: paste in Dashboard → SQL Editor → Run
6. Update this README table

## Rollback pattern

- Prefer additive changes (`ADD COLUMN` with default, not `DROP COLUMN`)
- If you must destructive-change: write a paired `NNN_rollback.sql`
- **RLS changes**: test with `set role authenticated` to confirm policies before shipping

## Local dev vs prod

Currently: **prod-only** (Supabase free tier, single project).
Future: use Supabase branches for staging (`db branch create ...`).
