# LUNA × Lily

**Take-home demo for PalUp AI Agent Designer**

A dual-agent (C 端 + B 端) AI system for Shopify Plus 美妝品牌 LUNA Beauty.
- **Lily-C**：C 端買家 chat widget（客服 + 業務推廣 + 訂單/退貨/多語/handoff）
- **Lily-B**：B 端內勤 conversational BI dashboard

## 快速起手

### Frontend (Next.js)

```bash
cd frontend
npm run dev
# 開 http://localhost:3000
```

### Backend (FastAPI)

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8080
# 開 http://localhost:8080/health
```

## 專案結構

```
palup-demo/
├── frontend/          # Next.js + Tailwind + TypeScript
├── backend/           # FastAPI + Gemini + Supabase
├── seed/              # 假資料
├── sub-agents/        # Agent Army CI/CD 定義
├── mockup/            # (Day 1) Static HTML mockup
├── vendor/agency-agents/  # 231 個 persona 藍本
├── spec.md            # Scope + 決策
├── product-vision.md  # 完整願景 + roadmap
├── architecture.md    # 技術架構 + 流程圖
├── process-log.md     # Q3 執行過程紀錄
├── metrics.md         # Q7 tokens/時間/成本
└── q1-7-draft.md      # 7 題答案 draft
```

## Tech Stack

- **LLM Runtime**: Gemini 2.5 Flash (free tier)
- **Backend**: Python + FastAPI (Fly.io)
- **Frontend**: Next.js + Tailwind + assistant-ui (Vercel)
- **DB**: Supabase Postgres (free tier)
- **CI/CD**: GitHub Actions + 8 sub-agents

## Development Tools

- **Claude Code** (Opus 4.7, 1M context)
- **Superpowers** plugin — 14 dev skills
- **Gstack** — Garry Tan's Claude Code setup
- **Agency-Agents** — 231 persona library

## 環境變數

複製 `backend/.env.example` 到 `backend/.env` 填入你的 keys。
