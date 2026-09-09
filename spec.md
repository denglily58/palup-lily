# PalUp Take-home Demo — Spec

**Status**: Day 1 in progress
**Started**: 2026-09-08
**Deadline**: 2026-09-15 前後
**Target 職缺**: PalUp AI Agent Designer
**Product name**: **Lily**

---

## 🎯 Meta Reframe（Phase 7 補入）

**這是 dual-purpose deliverable**：

| 目的 | 權重 | 交付物 |
|---|---|---|
| A. 可跑的 demo | 40% | working system + demo 影片 |
| **B. Q1-7 答得漂亮的證據** | **60%** | process-log、metrics、實際使用工具的軌跡 |

**開發過程本身 = 一級交付物**，不是副產品。每個決策/動作都要問一句：這對 Q1-7 哪一題有幫助？

---

## 一句話產品定位

**Shopify Plus 電商用的 AI 業務員+客服（C端） + 消費者訊號雷達（B端）**

---

## 使用者 & 場景

### C 端消費者
- **誰**：來電商網站的買家（訪客 / 會員 / 回頭客）
- **在哪**：Shopify 店網頁右下 chat widget
- **想做什麼**：找商品、問規格、查訂單、退換貨、抱怨

### B 端內勤（Shopify Plus 品牌內勤）
- **誰**：電商 manager / 品牌經理（非老闆本人，more professional）
- **在哪**：內部 Dashboard
- **想做什麼**：即時掌握消費者需求、找商機、找內部改善點、看營收

---

## 垂直領域 & 品牌設定（Locked）

### 垂直：**美妝**（純美妝，非保養）

### 虛構品牌：**LUNA Beauty**（名稱可再改）
- **定位**：小眾、色彩鮮明、包容多元膚色的專業級美妝
- **客單**：NT$1500-4000
- **賣點**：純素、cruelty-free、包容多色底色、皮膚科醫師背書
- **有 loyalty program、月訂閱制**

### SKU 組成（8-12 個 base products，加色號後 ~30 variants）

| 類別 | Base products | 色號/變體 |
|---|---|---|
| 底妝 | 粉底液 x1、氣墊 x1、遮瑕 x1 | 各 4-6 色 |
| 眼妝 | 眼影盤 x2（中性 + 大地）、眉筆 x1、睫毛膏 x1 | 眉筆 3 色 |
| 唇妝 | 口紅 x1、唇釉 x1 | 各 6-8 色 |
| 頰彩 | 腮紅 x1 | 4 色 |
| 明星禮盒 | x1 | - |

---

## Demo Scope（全部 Locked）

### C 端功能
- Chat widget（右下浮動視窗）
- Lily 主動打招呼開場
- 客服 + 業務推廣雙職能
- 讀後台資料（見下方「後台資料清單」）
- 答不出來會誠實承認（不亂編）
- **訂單查詢**（用 email / 訂單編號查 seed orders）— 淺實作
- **退貨啟動**（觸發 → 記錄申請 → 進 B 端 inbox）— 淺實作
- **多語**（中/英切換 + Lily 自動偵測 + LLM 即時翻商品文案）— 淺實作
- **真人 handoff**（觸發轉真人 → 對話進 B 端 inbox + 客戶看到「已為您轉接」）— 淺實作

### B 端 Dashboard（chat-first + 快速指標卡）
**Conversational BI 架構** — 頂部快速指標卡 + 老闆用自然語言問 Lily-B

**6 個模組**（原 4 個 + 3-lens review 後 +2）：
1. **對話全文 + 意圖標籤即時流**
2. **需求缺口**（客人問過但店裡沒賣）
3. **問答回覆狀態**（每題答得如何，含 SLA compliance）
4. **💰 商業指標即時儀表**（今日對話→轉單/AoV/AI 成本 vs. 收入）
5. **🤖 AI 使用量**（tokens/cost 本月累計、趨勢、每對話成本）
6. **📋 活動記錄**（多帳號 audit log by user/action/date）

### Lily 雙人格
| 人格 | 對誰 | 幹嘛 |
|---|---|---|
| **Lily-C** | C 端買家 | 客服+推廣，讀商品/訂單/評論/運送 |
| **Lily-B** | B 端內勤 | 用自然語言查數據，讀對話/銷售/庫存 |

### 問答回覆狀態分類
| 狀態 | 意義 |
|---|---|
| ✅ 已回答 | 系統正常 |
| 🟡 已回答（低信心） | 需 merchant 抽查 |
| 🔴 無法回答 | 資料/訓練缺口 |
| 🟠 轉真人 | 人力訊號 |
| ⏸ 客戶離開 | 流失風險 |

### 後台資料清單（6 樣）
- 商品目錄（含色號 metadata）
- 訂單
- 政策 FAQ（退換貨、運費、促銷）
- 商品評論（沒這個 Lily 無法引用「社會證明」）
- 運送規則（沒這個 Lily 答不出「幾天到」）
- 銷售 + 成本 metadata（沒這個 B 端商業儀表空的）

### Demo UX
**Split screen 分割畫面**：左 C 端 chat（面試官打字）/ 右 B 端 dashboard（即時更新）

---

## 使用者痛點需求（by bucket）

> 兩層結構：
> **戰略層 buckets**（由 Lily 提出，「錢+信任」的商業本質）
> **體驗層 items**（Claude 初擬 + Lily 補充，具體摩擦與需求）

### C 端消費者痛點

#### 🎯 符合需求（實際上是不是我要的）
- 商品描述看半天還不確定適不適合自己【Claude】
- 網站搜尋不好用，找不到想要的【Claude】
- 猶豫要不要買，沒人給第二意見【Claude】

#### ✨ 效果驗證（商品實際效果）
- _待補_：想確認實際效果，光看描述不夠

#### 🚚 物流（下單多少天拿到）
- _待補_：想確認幾天到、能否指定時段

#### 🛠 售後（有問題怎麼辦、退換貨）
- 想退貨不知道流程【Claude】
- 收到不對的東西不知怎麼辦【Claude】

#### ⭐ 社會證明（實際購買過的評論）
- _待補_：想看真實買家怎麼說

#### 🔎 找得到 & 自助（Claude 加的 bucket）
- 深夜想買沒真人服務【Claude】
- 想問規格但開 email 太麻煩【Claude】
- 訂單狀態要登入才看得到，很煩【Claude】
- 想要的商品店裡沒有 → 只能離開【Claude】

---

### B 端內勤痛點

#### 💰 銷售結果（商品有沒有賣出去、賣多少）
- 商品有沒有賣出去【Lily】
- 賣多少【Lily】

#### 📈 銷售方法（怎麼賣、怎麼賣更多）
- 怎麼賣出去【Lily】
- 怎麼賣更多【Lily】
- 每天重複回答同樣問題，無法規模化【Claude】
- 不同員工回答不一致，客戶體驗參差【Claude】

#### 🧾 財務（成本、毛利、營業額）
- 成本多少【Lily】
- 毛利【Lily】
- 營業額多少【Lily】

#### 🚪 流量獲客（怎麼把消費者引進來）
- 怎麼把消費者引進來【Lily】

#### 🎯 旅程/轉單（完成消費旅程、轉單）
- 完成消費旅程【Lily】
- 轉單【Lily】
- 客人問完就跑，不知為何離開【Claude】

#### ⏱ 營運效率（Claude 加的 bucket）
- 週報/月報太慢，客訴延誤【Claude】
- 沒時間看每一則對話【Claude】
- 客訴/負評訊號沒被及時抓到【Claude】
- 真人接手時不知 AI 說過什麼【Claude】
- 淡旺季人力配置難抓【Claude】

---

## 痛點 → 產品功能 對照

### C 端痛點 → Lily-C 能力
| 痛點 bucket | Lily 對應能力 |
|---|---|
| 🎯 符合需求 | 顧問式對話推薦、澄清需求（膚色/需求/場合） |
| ✨ 效果驗證 | 引用評論/案例/數據 |
| 🚚 物流 | 查運送規則、算 ETA |
| 🛠 售後 | 政策諮詢、引導退換貨流程 |
| ⭐ 社會證明 | 主動秀相關評論 |
| 🔎 找得到 & 自助 | 24/7 chat、自然語言找商品、色號推薦 |

### B 端痛點 → Lily-B / Dashboard 對應
| 痛點 bucket | Dashboard 模組 |
|---|---|
| 💰 銷售結果 | 商業指標儀表 |
| 📈 銷售方法 | 對話→轉單分析、AI 一致性 |
| 🧾 財務 | 商業指標儀表（成本 vs. 營收） |
| 🚪 流量獲客 | (optional) 未進 demo |
| 🎯 旅程/轉單 | 對話狀態 + 轉單標記 |
| ⏱ 營運效率 | 對話全文流、意圖標籤、需求缺口、問答回覆狀態 |

---

## Tech Stack（Locked — 全部 $0）

| 層 | 選定 | 為什麼 |
|---|---|---|
| **LLM Runtime** | Gemini 2.5 Flash 免費層 | $0，速率夠 demo；agent 應 LLM-agnostic 是 Q2 亮點 |
| **開發用 LLM** | Claude Opus 4.7 (via Claude Code) | Lily Max 涵蓋 |
| **後端** | Python + FastAPI | 對齊 PalUp、支援 middleware |
| **前端** | Next.js + Tailwind + shadcn/ui | 主流 + Chat UI 現成 |
| **Chat UI** | `assistant-ui` npm | 快速接 streaming |
| **視覺化** | Recharts | Dashboard 卡片 |
| **DB** | Supabase 免費層 | 500MB 夠 demo |
| **前端部署** | Vercel Hobby | $0，一鍵接 Next.js |
| **後端部署** | Fly.io 免費層 | $0，Docker 支援 |
| **CI/CD** | GitHub Actions | Public repo 無限 |
| **認證** | Supabase Auth | 免費層 |
| **Rate limit** | slowapi | 免費 |
| **監控** | Sentry 免費層 | 5k errors/mo |

### Agent 開發工具（Q4/Q5 素材）

| 工具 | 用在 Phase | 為什麼 |
|---|---|---|
| Claude Code 內建 sub-agent | Day 2-7 全程 | Q4 主答案 |
| **Superpowers** | Day 2-4（dev 主線） | TDD / brainstorm / subagent-driven-dev |
| **Gstack** | Day 5-6（shipping） | release-check / browser-qa / shipping-discipline |
| **Agency-Agents**（Flavio Copes 232 personas） | Day 2-5（挑合適 persona） | 校正過：**不是 Agency Swarm** |
| Agency Swarm | Day 6 可選 | 若時間夠加 runtime 多 agent（非 Q5 範圍） |

### Runtime 多 agent 架構

- Lily-C + Lily-B 直接 FastAPI + Gemini SDK 寫，不引入 Agency Swarm（KISS）
- Day 6 有時間可 upgrade

---

## 剩餘待決（Day 1 剩下處理）

- [x] 全部 scope 決策 ✅
- [x] 垂直 = 美妝 / 品牌 = LUNA Beauty ✅
- [x] Tech stack ✅
- [ ] 每天 3-4 小時陪跑確認

---

## Q1-7 素材文件清單

| 檔案 | 用途 | Q 對應 |
|---|---|---|
| `process-log.md` | 執行過程逐 phase 紀錄 | Q3 |
| `metrics.md` | tokens/時間/成本追蹤 | Q7 |
| `q1-7-draft.md` | 7 題答案的 iterative draft | Q1-Q7 全部 |
| `sub-agents/` 目錄 | Agent Army CI/CD 定義 | Q6 |

---

## 一週作戰藍圖（09-09 重算，多一天 buffer）

**Day 1+2 昨天壓一天完成**，實際今天是 working Day 2。總計約 30-35 hr 可用工時 vs. ~25 hr 總 scope。

| 日期 | Working Day | 內容 | Q 素材 |
|---|---|---|---|
| 09-08 | Day 1（昨） | ✅ 需求 + 選型 + 骨架 + agent hello | Q3, Q4, Q5 |
| **09-09** | **Day 2（今）** | seed data ✅ + 商品推薦 + 多語 + session + token log + 開始 SSO | Q5, Q7 |
| 09-10 | Day 3 | 完 SSO + event log + 訂單查詢 + 退貨 + version control C（semver+CHANGELOG） | Q4, Q5 |
| 09-11 | Day 4 | handoff（+ SLA fake）+ Lily-B（雙人格）+ version control A+B（prompt+model） | Q4, Q5 |
| 09-12 | Day 5 | AI usage widget + Agent Army 8 sub-agents + version control D+E（migrations + agents.yaml） | Q6 |
| 09-13 | Day 6 | CI/CD → Fly.io + Vercel 部署 + OpenClaw / Hermes spike | Q1, Q2, Q6 |
| **09-14** | **Day 7 (buffer)** | Polish + demo rehearse 3x + Q1-7 定稿（**不錄影 — Lily 09-09 決策**） | 全部 |
| 09-15 | 交件 | 上傳 + 面試準備 | - |

### 每天投入
- 平均 **5 hr/day** × 6 天 = 30 hr（vs. 25 hr scope，5 hr buffer）
- 09-14 buffer 專門處理 rehearse + Q1-7 defense + 錄影
- 09-15 純交件 + 心理準備，不寫 code

## Demo Storyboard（5 分鐘完整旅程，經 pacing 調整）

| 時間 | 場景 | 秀什麼能力 |
|---|---|---|
| 0:00-0:20 | LUNA 首頁 + Lily 打招呼 | C 端 UX |
| 0:20-0:30 | 切英文 → 切回中文 | 多語 |
| 0:30-1:20 | 顧問式推薦口紅 + 引評論（50s） | 業務 + 社會證明 |
| 1:20-1:50 | 「查我上週訂單 xxx@」→ Lily 讀 order（30s） | 訂單查詢 |
| 1:50-2:20 | 「這隻要退」→ 觸發退貨（30s） | 退貨啟動 |
| 2:20-2:40 | 「我要真人」→ Lily「已為您轉接」（20s） | 真人 handoff |
| 2:40-3:00 | 「有沒有亞洲膚色眉筆」→ 記需求缺口（20s） | 需求缺口 |
| 3:00-3:20 | 切 B 端 dashboard → 剛剛 handoff 進 inbox | C+B 聯動 wow |
| 3:20-4:20 | Lily-B chat 問「本週敏感肌客人」+ pin widget | Conversational BI |
| 4:20-5:00 | 秀 GitHub Actions 8 sub-agent → 自動部署 | CI/CD |

### Demo 5 個必達成關鍵劇本（Day 6 rehearse checklist）
1. Lily-C 開場能認出「品牌名 = LUNA Beauty」，tone 正確
2. 推薦口紅時**真的引用了評論資料**（不是幻覺）
3. 訂單查詢**真的回真的訂單**（不編）
4. Handoff 觸發後 B 端 inbox **即時（<3 秒）**出現
5. Lily-B 分析回覆能生**圖表 + 洞察建議**（不只文字）

### 面試官會後亂玩的 fallback
- **Off-brand 問（政治/私人）**：「我專注在 LUNA Beauty 商品，這個我幫不上，回產品聊聊？」
- **意料外功能問**：「這是 demo scope，Phase X roadmap 會做」
- **想 hack prompt injection**：backend 有 guardrail，會拒答並記 log
- **API 掛了**：前端顯示「Lily 暫時休息，1 分鐘後再試」

---

## 🔧 Day 3 Prep 修正（來自 2026-09-09 3-lens review）

### Session / 多輪對話模型
- Frontend 首次載入生 `session_id`（UUID v4），存 `localStorage`
- 每個 `/chat` request 帶 `session_id`
- Backend 用 `session_id` 從 DB 拉最近 10 則歷史，塞給 Gemini 當 context
- Lily-B 分析時 group by `session_id` 認一場對話

### Cross-agent 資料共享（DB tables）
| Table | Lily-C | Lily-B | 用途 |
|---|---|---|---|
| `conversations` | 寫 | 讀 | 對話全文 |
| `chat_logs` | 寫（middleware） | 讀 | Token/latency/cost 每 call 一筆 |
| `handoff_inbox` | 寫 | 讀 | 轉真人事件 |
| `demand_gaps` | 寫 | 讀 | 客人問但店裡沒有 |
| `widgets` | - | 寫/讀 | B 端 pin 的自訂 widget |
| `orders` (seed) | 讀 | 讀 | 訂單查詢 |
| `products` (seed) | 讀 | 讀 | 商品目錄 |
| `reviews` (seed) | 讀 | 讀 | 引評論 |

### Token / Cost auto-logging（Q7 evidence 自動化）
- FastAPI middleware：每次 `/chat` 完成後 insert 一筆到 `chat_logs`
- 欄位：`timestamp`, `endpoint`, `session_id`, `input_tokens`, `output_tokens`, `latency_ms`, `model`, `cost_estimate`
- Day 6 收尾用 `SELECT SUM(...)` 一次拿全部數字

### Daily Ritual（Day 3-6 每晚 10 分鐘）
1. 更新 `process-log.md` 加當日 phases
2. 更新 `metrics.md` 加當日 tokens/time/cost 摘要
3. 更新 `q1-7-draft.md` 補新 evidence
4. Git commit

### 多語策略（clarify）
- **商品目錄**：seed 時就寫 `name_zh` + `name_en` + `description_zh` + `description_en`（不靠 LLM 即時翻）
- **對話回覆**：LLM 自動偵測 user 語言 mirror 回覆
- **UI 文字**：Next.js i18n dict (`lib/i18n.ts`)，中英雙檔

### Handoff mechanism 細節（含 SLA fake 資料）
- Lily-C 觸發：intent classifier 判定 → 寫 `handoff_inbox` row（status=pending, urgency, transcript）
- B 端通知：Supabase Realtime subscribe，dashboard 即時彈紅點
- **SLA 承諾**：工作日 4hr、Weekend 12hr
- **Fake 完整 demo**：seed 10 筆歷史 handoff，8 準時、2 過期 → dashboard 顯示 80% SLA compliance

### SSO + 多帳號 + Event Log（**Enterprise-level**）
- **登入**：Supabase Auth + Google OAuth，用戶用 Google 一鍵登入
- **User 區分**：seed 3 個 merchant 內勤角色
  - `emily@luna.beauty`（**Emily Chen, E-commerce Manager**）
  - `david@luna.beauty`（**David Wang, Marketing Manager**）
  - `alex@luna.beauty`（**Alex Kim, Admin**）
- **Pin/widget 綁 user_id**：不同角色看到不同儀表卡
- **Event log**（audit trail）：
  - Table：`event_logs (id, user_id, action, target, metadata, timestamp)`
  - Action 例：`login / logout / pin_widget / unpin / chat_query / handoff_taken / export`
  - Dashboard 新 tab **「活動記錄」**顯示可篩選 by user / by action / by date

### Token 使用量 + Cost/Pricing 作為 B 端 first-class feature
- **B 端 Dashboard 加 widget**：**「AI 使用量」**
  - 累計 tokens（本月）
  - 累計成本（本月 $）
  - 過去 30 天趨勢圖
  - Cost per conversation 顯示在每場對話下方
- **收費模型**（詳見 `product-vision.md` Pricing Model section）：
  - Starter $99/mo（1000 對話/月）
  - Growth $499/mo（10000 對話/月）
  - Enterprise $2999+/mo（無限 + SSO + audit + SLA）
- **面試講述金句**：Token 透明化 = 讓 merchant 信任 AI 成本可控

### 部署 env vars checklist
**Backend (Fly.io)**：`GEMINI_API_KEY` / `SUPABASE_URL` / `SUPABASE_SERVICE_KEY` / `SENTRY_DSN`（optional）/ `BASIC_AUTH_USER` / `BASIC_AUTH_PASS`
**Frontend (Vercel)**：`NEXT_PUBLIC_BACKEND_URL` / `NEXT_PUBLIC_SUPABASE_URL` / `NEXT_PUBLIC_SUPABASE_ANON_KEY`

### 其他約定
- **LLM 失敗 UI**：3 秒 timeout → 顯示「Lily 暫時休息，1 分鐘後試試」
- **Testing framework**：pytest (backend) + vitest (frontend) + Playwright (e2e)
- **Post-demo roadmap rehearsal**：Day 6 錄 demo 前，Lily 對著 `product-vision.md` 面試講述模板 練 3 次

### Version Control（5 層）

**A. Prompt versioning**
- 每個 system prompt 檔加 frontmatter `version: 1.0 | changed: 2026-09-09 | reason: ...`
- 位置：`backend/agents/prompts/*.md`
- 改動需寫 change reason，可 rollback

**B. Model versioning**
- `backend/agents/model_registry.yaml` 記錄每個 agent 用什麼 model + 為何選
- 例：`lily_c: gemini-3.6-flash, fallback: gemini-2.5-flash, reason: cost/quality trade`
- Model 掛了自動 fallback（try/except + swap）

**C. Semver + CHANGELOG.md**
- 產品版號：v0.1 (Day 2 hello) → v0.2 (Day 3 seed+多語) → v0.3 (Day 4 客服) → v0.5 (Day 5 CI/CD) → v1.0 (Day 6 交件)
- CHANGELOG.md：每個 release 手寫 or 用 `git-cliff` 自動生
- 每次 git tag 對應 release

**D. DB schema migrations**
- Supabase 內建 migration files（`supabase/migrations/*.sql`）
- 每個表變動一個 migration，可前進 / 回滾
- Day 3 用 migration 建 chat_logs / event_logs / handoff_inbox / demand_gaps / widgets 5 個新表

**E. Agent config version（agents.yaml）**
- `backend/agents/registry.yaml` 集中管理：
  ```yaml
  agents:
    lily_c:
      version: 1.0
      model: gemini-3.6-flash
      prompt: prompts/lily_c_v1.md
      tools: [products.search, orders.lookup, reviews.summarize, ...]
    lily_b:
      version: 1.0
      model: gemini-3.6-flash
      prompt: prompts/lily_b_v1.md
      tools: [conversations.query, analytics.aggregate, ...]
  ```
- 換 config 即換 agent 行為，可 A/B test

**Q1-Q2 面試講述金句**：
> 「AI 系統的痛點就是**沒有 diff-able 的版本控制** —— prompt 改一句話行為完全不同，但沒有 git blame。我做了 5 層 version control：prompt / model / product / schema / agent config 全部可追蹤可 rollback。」
