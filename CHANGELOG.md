# Changelog

All notable changes to LUNA × Lily documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows [Semver](https://semver.org/).

---

## [Unreleased]
### Planned
- Lily-B analyst persona (Day 4)
- Handoff to human agent + SLA fake data (Day 4)
- AI usage widget + cost/pricing (Day 5)
- 5 more sub-agents + CI/CD pipeline (Day 5)
- Cloud Run + Vercel deployment (Day 6)
- OpenClaw / Hermes spike (Day 6)

---

## [0.3.0] — 2026-09-09

Day 3 (working Day 2): Function-calling tools + Supabase auth + realtime dashboard.

### Added
- `tools/orders.py` — Lily-C looks up orders by email or order number via Gemini function calling
- `tools/returns.py` — Lily-C initiates returns, writing to Supabase `handoff_inbox`
- Supabase Auth with 3 seed users (Emily/David/Alex) + email+password + Google OAuth
- `/login` page + `/admin` page + audit trail
- Supabase Realtime — admin activity log auto-updates without refresh
- Buyer chats also flow to `event_logs` table
- 3 sub-agent stubs: `linter-agent`, `security-agent`, `deploy-agent`

### Changed
- LLM runtime: `gemini-3.6-flash` → `gemini-3.5-flash-lite` (higher free-tier req/day quota)
- UI default language: Chinese → English (Shopify Plus targets NA market)
- Merchant names: 王小美 → Emily Chen etc.

### Fixed
- React StrictMode duplicate subscribe error (unique realtime channel name)
- Python 3.9 compatibility (`Optional[str]` instead of `str | None`)
- Dark mode contrast issue (force light theme in `globals.css`)

---

## [0.2.0] — 2026-09-08 (evening)

Day 2 (compressed same day): Seed data + product recommendation + multi-turn + auth foundation.

### Added
- Seed data: 10 SKUs, 25 reviews, 30 orders, US shipping rules, policies, 10 conversation samples
- `tools/catalog.py` — Injects full catalog + top reviews into Lily-C system prompt
- `tools/metrics.py` — JSONL logger for token/cost/latency (Q7 evidence base)
- `/metrics` endpoint aggregates tokens/cost/latency stats
- Session memory: 10-message context window, `/reset` endpoint
- Frontend: `localStorage`-based session_id, `⟳` reset button, EN/中 language toggle

### Changed
- Brand rename: LUNA Botanica → LUNA Beauty
- Default language: en (was zh); target market North America

---

## [0.1.0] — 2026-09-08 (morning)

Day 1 (compressed): Scaffolding + hello-world agent + tool ecosystem.

### Added
- Next.js 15 frontend (TypeScript + Tailwind + App Router)
- FastAPI backend with CORS + `/health` + `/chat` endpoints
- Gemini API integration (SDK: `google-genai`)
- Bilingual system prompts (EN + zh)
- Chat widget UI with streaming-ready message list
- Superpowers Claude Code plugin installed
- Gstack Claude Code setup installed to `~/.claude/skills/gstack/`
- Agency-Agents 231-persona library cloned to `vendor/agency-agents/`
- 8 documentation files: `spec.md`, `product-vision.md`, `architecture.md`, `process-log.md`, `metrics.md`, `q1-7-draft.md`, `CLAUDE.md`, `README.md`
- 2 mockups: `mockup/store.html` + `mockup/dashboard.html`

### Infrastructure
- Git initialized, `.gitignore` protects secrets
- Environment: Python 3.9 + Node 24 + venv

---

## Versioning Policy

- **v0.x** — pre-launch demo iterations (LUNA × Lily is a take-home)
- **v1.0** — take-home submission-ready (target: 2026-09-15)
- **v1.x** — post-hire iterations (hypothetical)
- **v2.0** — production launch (hypothetical)

Breaking changes bump minor for pre-1.0, major for post-1.0.
