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

**4 個模組**：
1. **對話全文 + 意圖標籤即時流**
2. **需求缺口**（客人問過但店裡沒賣）
3. **問答回覆狀態**（每題答得如何）
4. **💰 商業指標即時儀表**（今日對話→轉單/AoV/AI 成本 vs. 收入）

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

## 一週作戰藍圖（scope 擴增後）

| Day | 階段 | 產出 | Q 素材 |
|---|---|---|---|
| Day 1（今天）| 需求收斂 + 選型 + mockup + 建骨架 | Spec + mockup + 5 個素材檔 + 空專案 | Q3 |
| Day 2 | 安裝 Superpowers/Gstack/Agency-Agents + 帳號註冊 + Agent hello | Chat UI 開起來、agent 回 hi | Q4, Q5 |
| Day 3 | 業務 agent + Shopify seed + **多語** + tracking tokens | 能對話推商品、中英切換 | Q5, Q7 |
| Day 4 | 客服 agent + **訂單查詢 + 退貨啟動** + Lily-C/Lily-B dual | Lily 完整 C 端能力 | Q4, Q5, Q7 |
| Day 5 | Agent Army 8 sub-agents + CI/CD → Fly.io + Vercel + **handoff → B 端 inbox** | 自動化部署 + 8 sub-agent md | Q6 |
| Day 6 | OpenClaw/Hermes 小實驗 + Polish + 錄 demo + Q1-7 定稿 | 交件包 | Q1, Q2 |
| Day 7 | Buffer / 交件 / 面試準備（buffer 已被 scope 擴增吃掉，實際只剩交件） | Done | - |

## Demo Storyboard（5 分鐘完整旅程）

| 時間 | 場景 | 秀什麼能力 |
|---|---|---|
| 0:00-0:30 | LUNA 首頁 + Lily 打招呼 | C 端 UX |
| 0:30-0:40 | **切英文**（demo 多語） | 多語 |
| 0:40-1:30 | 顧問式推薦口紅 + 引評論 | 業務 + 社會證明 |
| 1:30-2:00 | 「查我上週訂單」→ Lily 讀 order | **訂單查詢** |
| 2:00-2:30 | 「這隻要退」→ 觸發退貨 | **退貨啟動** |
| 2:30-2:50 | 「我要真人」→ Lily「已為您轉接」 | **真人 handoff** |
| 2:50-3:10 | 「有沒有亞洲膚色眉筆」→ Lily 記需求缺口 | 需求缺口 |
| 3:10-3:30 | 切 B 端 dashboard → 剛剛的 handoff 進 inbox | C+B 聯動 wow |
| 3:30-4:20 | Lily-B chat 問「本週敏感肌客人」+ pin widget | Conversational BI |
| 4:20-5:00 | 秀 GitHub Actions 8 sub-agent → 自動部署 | CI/CD |
