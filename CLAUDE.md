# Claude Code Instructions for LUNA × Lily

## Project Purpose

Take-home demo for PalUp **AI Agent Designer** position.
**Dual-purpose deliverable**: (1) working demo, (2) evidence for Q1-7 answers.

## Key Files (讀順序)

1. `spec.md` — 全部 scope 與決策
2. `product-vision.md` — 完整願景 + roadmap
3. `architecture.md` — 技術架構 + 流程圖
4. `process-log.md` — 執行過程（Q3 答案基底）
5. `q1-7-draft.md` — 7 題答案 iterative draft
6. `metrics.md` — tokens/時間/成本追蹤（Q7）

## Working Style

- **User = Lily**：iKala 剛畢業 PM，技術小白新手
- **Vibe coding**：Claude 主寫、Lily 決策 + 測試 + 內化
- **節奏慢**、勿一次拋大量、勿催進度
- **不 fabricate**：只講實際做過/驗證過的事
- **不用 subagent 除非任務 >30 秒**：Lily 對等待敏感

## Tech Constraints

- LLM runtime: **Gemini 2.5 Flash / gemini-3.6-flash** (免費層)
- Dev LLM: Claude Opus 4.7 via Claude Max
- Backend: Python 3.9 (系統) + FastAPI
- Frontend: Next.js 15 + Tailwind + TypeScript

## Development Tools

- **Superpowers** skills — always call `writing-plans` before code, `test-driven-development` when implementing
- **Gstack** — role-based skill router
- **Agency-Agents** — persona library at `vendor/agency-agents/`

## Env

- API key: `backend/.env` (gitignored)
- Never commit secrets

## Q1-7 Reminders

Every meaningful action should feed one of:
- Q3: log in `process-log.md`
- Q7: record tokens/time/cost in `metrics.md`
- Q6: add sub-agents to `sub-agents/` on Day 5
- Q1-2: Day 6 需要 spin up OpenClaw or Hermes for real experience

## Commit Message Convention

`feat/fix/docs/chore: <what>`
