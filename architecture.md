# Architecture — LUNA × Lily

**用途**：專案結構 + 系統架構 + 主要流程圖。你面試 walkthrough 直接翻這份。

---

## 1. 系統架構總覽

```
                          ┌────────────────────┐
                          │  面試官 / 買家 / 內勤 │
                          └──────┬─────────────┘
                                 │
                ┌────────────────┼───────────────┐
                │                                │
         ┌──────▼───────┐                 ┌─────▼──────┐
         │  C 端         │                 │  B 端       │
         │ LUNA 商店     │                 │ Admin       │
         │ + Chat 視窗   │                 │ Dashboard   │
         │ (Next.js)    │                 │ (Next.js)   │
         │ [Vercel]     │                 │ [Vercel]    │
         └──────┬───────┘                 └─────┬──────┘
                │                                │
                └────────────────┬───────────────┘
                                 │  HTTPS / JSON
                                 │
                         ┌───────▼────────┐
                         │  FastAPI       │
                         │  Backend       │
                         │  [Fly.io]      │
                         └───────┬────────┘
                                 │
        ┌────────────┬───────────┼────────┬─────────────┐
        │            │           │        │             │
   ┌────▼──────┐ ┌───▼────┐  ┌──▼──┐  ┌──▼────┐   ┌────▼──────┐
   │ Lily-C    │ │Lily-B  │  │Tools│  │Intent │   │Handoff    │
   │ Agent     │ │Agent   │  │(讀寫│  │Classi │   │Router     │
   │ (賣手+客服)│ │(分析師) │  │資料) │  │fier   │   │(觸發轉真人)│
   └────┬──────┘ └───┬────┘  └──┬──┘  └───────┘   └───────────┘
        │            │          │
        └────┬───────┴──────────┘
             │
        ┌────▼──────────┐
        │  Gemini 2.5   │
        │  Flash API    │
        │  (LLM Runtime) │
        └───────────────┘

        ┌───────────────────┐
        │  Supabase         │
        │  Postgres + Auth  │
        │  + Realtime       │
        │  (資料層)          │
        └───────────────────┘

        ┌───────────────────┐
        │  GitHub Actions   │
        │  + 8 sub-agents   │
        │  (CI/CD)          │
        └───────────────────┘
```

---

## 2. 專案 Folder 結構

```
palup-demo/
│
├── frontend/                    # Next.js（C 端 + B 端）
│   ├── app/
│   │   ├── page.tsx            # C 端 LUNA 商店首頁
│   │   ├── admin/
│   │   │   └── page.tsx        # B 端 dashboard
│   │   ├── api/                # Next.js API routes（proxy 到 backend）
│   │   └── layout.tsx
│   ├── components/
│   │   ├── ChatWidget.tsx      # C 端 chat 視窗
│   │   ├── ProductGrid.tsx     # 商品陳列
│   │   ├── ProductCard.tsx
│   │   ├── DashboardWidget.tsx # B 端 starter widget
│   │   ├── LilyBChat.tsx       # B 端 chat
│   │   ├── PinnedWidget.tsx    # 用戶自訂 pinned widget
│   │   └── LanguageSwitcher.tsx # 多語切換
│   ├── lib/
│   │   ├── api.ts              # 呼叫 backend
│   │   ├── i18n.ts             # 多語字典
│   │   └── supabase.ts         # Supabase client
│   ├── public/
│   ├── tailwind.config.ts
│   └── package.json
│
├── backend/                     # Python FastAPI
│   ├── app/
│   │   ├── main.py             # FastAPI 入口
│   │   ├── agents/
│   │   │   ├── lily_c.py       # C 端 agent
│   │   │   ├── lily_b.py       # B 端 agent
│   │   │   ├── intent.py       # 意圖分類器
│   │   │   └── prompts/        # System prompts (含多語版本)
│   │   │       ├── lily_c_zh.md
│   │   │       ├── lily_c_en.md
│   │   │       ├── lily_b_zh.md
│   │   │       └── lily_b_en.md
│   │   ├── tools/              # Agent 可呼叫的 tools
│   │   │   ├── products.py     # 讀商品目錄 / 搜尋
│   │   │   ├── orders.py       # 訂單查詢
│   │   │   ├── returns.py      # 退貨啟動
│   │   │   ├── reviews.py      # 引評論
│   │   │   ├── shipping.py     # 物流 ETA
│   │   │   ├── handoff.py      # 轉真人
│   │   │   ├── conversations.py # 對話查詢 (B 端用)
│   │   │   └── analytics.py    # 銷售/需求缺口統計 (B 端用)
│   │   ├── db/
│   │   │   ├── supabase.py     # Supabase client
│   │   │   └── schema.sql      # 資料表 DDL
│   │   ├── routes/
│   │   │   ├── chat.py         # /chat 端點（C 端 Lily-C）
│   │   │   ├── analytics.py    # /analytics 端點（B 端 Lily-B）
│   │   │   ├── admin.py        # /admin 端點（dashboard 資料）
│   │   │   └── health.py       # /health（給 CI/CD 用）
│   │   ├── middleware/
│   │   │   ├── ratelimit.py    # slowapi rate limit
│   │   │   ├── auth.py         # B 端保護
│   │   │   └── logging.py      # 觀測性
│   │   └── config.py           # 環境變數
│   ├── tests/
│   │   ├── test_agents.py
│   │   ├── test_tools.py
│   │   └── test_routes.py
│   ├── requirements.txt
│   ├── Dockerfile              # for Fly.io deploy
│   └── fly.toml
│
├── seed/                        # 假資料（一鍵重置）
│   ├── products.json           # LUNA 10 SKU + 色號
│   ├── reviews.json            # 每商品 5-10 則
│   ├── orders.json             # 30 筆訂單（跨 30 天）
│   ├── conversations.json      # 20-30 場預錄
│   ├── shipping_rules.json     # 物流規則
│   └── seed.py                 # 一鍵重置 DB
│
├── sub-agents/                  # Q6 Agent Army 定義
│   ├── README.md
│   ├── linter-agent.md
│   ├── security-agent.md
│   ├── test-runner-agent.md
│   ├── e2e-agent.md
│   ├── deploy-agent.md
│   ├── health-check-agent.md
│   ├── rollback-agent.md
│   └── pr-reviewer-agent.md
│
├── .github/workflows/           # CI/CD pipeline
│   ├── ci.yml                  # push 觸發 lint/test/security/e2e
│   └── deploy.yml              # main merge 觸發 deploy
│
├── mockup/                      # (Day 1) 靜態 HTML mockup
│   ├── store.html
│   └── dashboard.html
│
├── spec.md                      # 主 spec（scope + 決策）
├── product-vision.md            # 完整願景 + roadmap（面試素材）
├── architecture.md              # 本檔（技術架構）
├── process-log.md               # 執行過程紀錄（Q3）
├── metrics.md                   # tokens/時間/成本追蹤（Q7）
├── q1-7-draft.md                # 7 題 iterative draft
├── CLAUDE.md                    # 給 Claude Code 的專案指令
├── README.md                    # Repo 首頁
├── .gitignore
├── .env.example
└── docker-compose.yml           # 本地 dev（backend + Postgres）
```

---

## 3. 流程圖：C 端買家對話

```
Buyer 打開 LUNA 網站
        ↓
ChatWidget 主動彈出 (Lily 打招呼)
        ↓
Buyer 打字：「25 歲黃調肌想找日常口紅」
        ↓
Frontend → POST /chat
   { session_id, message, lang: "zh" }
        ↓
FastAPI /chat 接收
        ↓
Intent Classifier 分類：
   "recommend_product"
        ↓
Lily-C Agent 啟動
        ├── Tool: products.search({category:"lip", undertone:"yellow"})
        ├── Tool: reviews.summarize(matched_ids)
        └── Gemini 生成推薦話術
        ↓
Response streaming 回前端
        ↓
ChatWidget 渲染回覆 + 內嵌商品卡片
        ↓
[背景] 對話 log 寫入 Supabase (conversations)
   意圖 = "recommend_product"
   狀態 = "✅ 已回答"
        ↓
[Supabase Realtime] 推播給 B 端 dashboard
```

---

## 4. 流程圖：C 端訂單查詢 / 退貨

```
Buyer：「我上週訂單到了嗎？email is xxx@yy.com」
        ↓
Intent Classifier: "query_order"
        ↓
Lily-C Agent
   ├── Tool: orders.lookup_by_email("xxx@yy.com")
   ├── 找到 order #1234 (shipped)
   ├── Tool: shipping.get_eta("1234")
   └── Gemini 生成回覆
        ↓
"你 9/5 訂的 Nude Rose 已於 9/6 出貨，
 預計 9/9 到台北。追蹤碼: XXX。"

————————————————————————

Buyer：「這隻要退」
        ↓
Intent: "initiate_return"
        ↓
Lily-C Agent
   ├── Tool: returns.create(order="1234", reason="...")
   ├── 寫入 handoff_inbox (status=pending_review)
   └── Gemini 生成確認回覆
        ↓
"已提交退貨申請，2 個工作日內客服會聯繫您安排取件。
 申請編號: R5678"
        ↓
[Supabase Realtime] B 端 inbox +1
```

---

## 5. 流程圖：真人 Handoff

```
Buyer：「我要找真人客服」
        ↓
Intent: "request_human"
        ↓
Lily-C Agent
   ├── Tool: handoff.create({session_id, transcript, urgency})
   ├── 對話 status 標 "🟠 轉真人"
   └── Gemini 生成安撫回覆
        ↓
"了解，已為您轉接客服。
 工作日 9:00-18:00 內會回覆您，
 目前是離峰時段，約 30 分鐘。"
        ↓
[Supabase Realtime]
   B 端 dashboard 紅色警報 +1
   inbox 頂部出現新 handoff 卡
```

---

## 6. 流程圖：B 端 Lily-B 分析對話

```
Merchant 打開 Admin dashboard
        ↓
4 starter widgets 從 Supabase 拉即時數字
        ↓
Merchant：「本週敏感肌客人問什麼？」
        ↓
Frontend → POST /analytics { question, user_id }
        ↓
FastAPI /analytics
        ↓
Lily-B Agent
   ├── Tool: conversations.query(
   │       filter: {tag:"敏感肌", period:"7d"})
   ├── Tool: analytics.aggregate_by_intent(matched)
   └── Gemini 生成回覆 (含 chart_config + insight)
        ↓
Response {text, chart_config, insight, related_ids}
        ↓
LilyBChat 動態渲染：
   ├── text (文字)
   ├── chart (長條圖)
   ├── insight (💡 建議)
   └── [📌 存成儀表卡] 按鈕
        ↓
若 pin → POST /widgets → Supabase.widgets +1
        ↓
下次登入 dashboard，卡片還在，數字即時更新
```

---

## 7. 流程圖：多語

```
初始：Frontend 讀 navigator.language = "zh-TW"
        ↓
UI 文字用 i18n dictionary 渲染
        ↓
User 點右上角語言切換 → "en"
        ↓
UI 立即切換 + 送 { lang: "en" } 給 backend
        ↓
Lily-C 讀對應 prompt (prompts/lily_c_en.md)
        ↓
呼叫 Tools 時，商品資料仍是原始資料
        ↓
Gemini 在生成回覆時自動用 English + 翻商品文案
        ↓
若使用者打中文問，Lily 自動偵測回中文
   (LLM 天然支援語言 mirroring)
```

---

## 8. 流程圖：Dev → Deploy

```
Dev 改 code (locally)
        ↓
localhost 測試 OK
        ↓
git add + commit
        ↓
git push origin feature-branch
        ↓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GitHub Actions 觸發 CI workflow
   平行執行 8 sub-agents:
     ├── linter-agent      → ruff + eslint
     ├── security-agent    → Snyk-like 依賴掃描 + 密鑰洩漏檢查
     ├── test-runner-agent → pytest + vitest
     ├── e2e-agent         → Playwright 跑核心 flow
     └── pr-reviewer-agent → 自動 code review
        ↓
全綠 → PR 標 ready
        ↓
Human review + merge to main
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
main push 觸發 deploy workflow
   ├── deploy-agent      → docker build + push to Fly.io
   ├── deploy-agent      → Vercel deploy (frontend)
        ↓
   ├── health-check-agent → smoke test 5 個關鍵端點
        ↓
     ✅ 綠 → 完成 + changelog-agent 更新
     ❌ 紅 → rollback-agent 自動回上個版本
        ↓
Console log + Slack notification (optional)
```

---

## 9. 資料 Schema（簡化）

```
products
  id, sku, name, category, price, colors[], description,
  image_url, in_stock, cost, tags[]

reviews
  id, product_id, rating, text, author, created_at, tags[]

orders
  id, order_number, email, items[], total, status,
  created_at, shipping_eta, tracking_no

conversations
  id, session_id, actor (buyer/merchant), lang,
  messages[], intent, status (✅🟡🔴🟠⏸), created_at

handoff_inbox
  id, conversation_id, status, urgency, assigned_to,
  created_at, resolved_at

widgets  (B 端 pinned)
  id, user_id, query, response_snapshot,
  chart_config, position, refresh_interval, created_at

demand_gaps
  id, question, product_category, count,
  first_asked, last_asked, resolved

analytics_snapshots  (每小時 aggregate)
  id, period_start, total_conversations, total_conversions,
  total_revenue, top_intents[], top_demand_gaps[]
```

---

## 10. Env 變數清單

```
# Backend
GEMINI_API_KEY=xxx              # Google AI Studio (免費層)
SUPABASE_URL=xxx
SUPABASE_SERVICE_KEY=xxx        # server 端用
SENTRY_DSN=xxx                  # 監控 (免費層)
BASIC_AUTH_USER=demo            # B 端保護
BASIC_AUTH_PASS=xxx

# Frontend
NEXT_PUBLIC_SUPABASE_URL=xxx
NEXT_PUBLIC_SUPABASE_ANON_KEY=xxx
NEXT_PUBLIC_BACKEND_URL=https://palup-demo-api.fly.dev

# CI/CD
FLY_API_TOKEN=xxx
VERCEL_TOKEN=xxx
```
