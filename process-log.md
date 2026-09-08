# 執行過程紀錄（Q3 答案素材）

> **用途**：作業 Q3「請問您是怎麼執行這個專案的？過程是什麼？」的**真實**紀錄。
> **原則**：只記實際發生的事，不美化不編造。
> **維護**：每個 phase 完成就更新，Day 6 定稿時整理成 Q3 答案。

---

## 使用中的工具鏈

| 工具 | 用途 | 開始使用時間 |
|---|---|---|
| Claude Code (Opus 4.7, 1M context) | 主開發環境，PM+Eng+Design 三角 | Day 1 |
| WebSearch | 工具生態/公司背景研究 | Day 1 |
| Memory system | 存 PalUp 情報 + 個人偏好持久化 | Day 1 |
| Task management | 追蹤 Day 1 sub-tasks 進度 | Day 1 |
| **待引入**：Superpowers plugin | 5-phase 開發紀律 | Day 2 |
| **待引入**：Gstack | Role-based 開發技能包 | Day 2 |
| **待引入**：Agency Swarm | 多 agent 編排（Lily-C + Lily-B） | Day 3 |
| **待引入**：Claude Code sub-agents | Agent Army 分工做 CI/CD | Day 5 |

---

## Day 1 — 2026-09-08

### Phase 0: 情報收集（~30 min）

**發生的事**：
- Lily 貼作業題目：AI Agent + 線上業務+客服 + CI/CD + 7 題問答
- **Claude red-flag 判斷**：對 6 個工具名稱（OpenClaw / Hermes / Superpowers / Gstack / Agency-Agents / Agent Army）逐個標記可信度
- **WebSearch 驗證**：6 個工具全部為真實、屬 2026 上半年 Claude Code 生態爆紅的 tools（Claude 的 knowledge cutoff 是 2026-01，這些多是之後才紅）
- **WebSearch PalUp 公司背景**：確認宇泰華科技（TW startup）、南港、1-10 人、主打 Aria = Shopify **Plus** 商家 AI 業務+客服

**產出**：
- 6 個工具的分類清單（Runtime Agent / Skills Framework / Pattern）
- PalUp 公司 memory 檔（`job_palup_2026.md`）

### Phase 1: 對齊工作模式（~10 min）

**發生的事**：
- Lily 定義合作角色：「你以工程、設計、pm 等全方位角度」
- Claude 定位為 PM + Eng + Designer 三角，Lily 為決策者 + 內化者
- Lily 自述技術程度：小白新手 → 決定 vibe coding 模式（Claude 主寫、Lily 決策 + 測試）

**產出**：一週作戰藍圖（Day 1-7）

### Phase 2: 需求拆解（~15 min）

**發生的事**：
- Lily 要求「先拆解題目再往下」
- Claude 提出 7 個維度拆解框架：誰用 / 在哪接觸 / 想幹嘛 / 能做什麼動作 / 讀哪些後台資料 / 交接時機 / 成功長怎樣
- Lily 補充：Agent 命名為 **Lily**（與本人同名，記憶點）
- Lily 補充：B 端內勤要能得知消費者需求

**產出**：產品變成 dual-actor（C 端 + B 端）

### Phase 3: Demo scope 收斂（~15 min）

**發生的事**：
- Claude 從 demo 導演角度反推：找 money shot
- 分析 5 種 wow angle，選定 **C+B 聯動即時流**（因對到 Aria 產品定位）
- 5 分鐘 storyboard 草擬
- Lily 選定 B 端 dashboard 3 模組：對話全文+意圖 / 需求缺口 / 問答回覆狀態
- Lily 加入「問答回覆狀態」5 種分類

**產出**：初版 spec.md、split-screen demo UX

### Phase 4: 痛點盤點（~20 min）

**發生的事**：
- Claude 初擬 C 端 9 條 + B 端 9 條（UX 摩擦視角）
- Lily 補「錢+信任」戰略層痛點（B 端銷售/財務/流量/轉單；C 端符合需求/效果/物流/售後/評論）
- Claude reframe 兩層合併成 **12 個 buckets**（C 端 6 + B 端 6）
- Lily 明確：「你說的痛點也是對的」→ 保留兩批

**產出**：spec.md 痛點結構化 by bucket

### Phase 5: Scope 進化（~10 min）

**發生的事**：
- 因痛點層次拉高，Claude 提議加 scope：
  - 後台資料 3 → **6 樣**（+ 評論、運送、銷售成本）
  - B 端 dashboard 3 → **4 模組**（+ 商業指標儀表）
- Lily 全部 lock ✅
- Lily 加關鍵決策：**B 端 dashboard 都要能用問的**
- 觸發架構升級：Lily 分裂成雙人格 **Lily-C（賣手）+ Lily-B（分析師）**

**產出**：conversational BI 架構、chat-first + 卡片 UX 提案

### Phase 6: 垂直領域選定（~15 min）

**發生的事**：
- Claude 產出 3 領域評分表（保養美妝 / 寵物 / 3C），推薦保養
- Lily lock 保養美妝
- Lily 補關鍵情報：**PalUp 核心 = Shopify Plus 商家**（不是一般 SMB）
- Claude 據此調整品牌等級：中高階 DTC
- Claude 提議虛構品牌 **LUNA Botanica**

**產出**：memory 更新 Shopify Plus 定位、seed 品牌提案

### Phase 6b: 垂直領域細化（~10 min）

**發生的事**：
- Lily 拋出「改美妝」，質疑「會資料比較多一點嗎」
- Claude 分析純保養 / 純美妝 / 混合 三種資料量差異
- 提議混合品牌以最大化 wow 度
- Lily lock: 純美妝
- 品牌 LUNA Botanica 定調為純美妝品牌

**產出**：SKU 組成表（10-12 base products，加色號共 ~30 variants）

### Phase 7: 🎯 Reframe — Dual-Purpose Deliverable（~10 min）

**發生的事**：
- Lily 提醒：「最後我們會回到這個目的是面試 AI Agent Designer」
- Claude 意識到先前過度傾向「產品 MVP」思維，忽略了 Q1-7 evidence 才是主秀
- **重設權重**：Product MVP 40% / Q1-7 evidence 60%
- 拆解每題答案需要的**具體證據**：實際使用 OpenClaw/Hermes、安裝 Superpowers/Gstack、真的做 sub-agent CI/CD、追 tokens/cost 實測

**建立的新素材檔**（Day 2+ 持續填）：
- `metrics.md`（Q7 tokens/時間/成本追蹤）
- `q1-7-draft.md`（7 題答案 iterative draft）
- `sub-agents/`（Q6 Agent Army 定義目錄）

**refined 一週藍圖**：
- Day 2 一定要安裝 Superpowers + Gstack + Agency Swarm
- Day 2 開始追 metrics
- Day 5 真的做 8 個 sub-agent md 檔
- Day 6 spin up OpenClaw or Hermes 小實驗（親身經驗）

**Turning point 意義**：從「做 demo 順便答問題」→「demo 是答問題的載體」。整個 Day 2-7 執行邏輯翻轉。

**產出**：4 個素材檔骨架、藍圖 refine

### Phase 8: B 端 UI/UX 定稿（~15 min）

**發生的事**：
- Claude 提議 chat-first + 快速指標卡（推薦選項 c）
- Lily 選 (d)：以 (c) 為底 + **可 pin 儲存自訂 dashboard**
- Claude 意識到這是把 B 端從「靜態 dashboard」升級為 **personal analytics workspace**（ThoughtSpot Sage / Amplitude AI 等級）
- Lily 校正 demo 模式：**簡報引導式，Lily 主 demo**，會後面試官會玩玩看
- 需求升級：**真部署 + robust for poke**，不能是皮

**產出**：
- Dashboard UX = starter 4 widgets 預 pinned + chat 問 → pin 加新
- Demo 模式 = Lily 引導 5 分鐘 script + 會後可玩
- 韌性需求：rate limit、auth、seed 假對話資料

### Phase 9: Tech Stack 選型（~30 min）

**發生的事**：
- Claude 先提 stack（含 Anthropic API 付費）
- Lily 質疑「有免費版本嗎」→ **Claude 校正過度推薦付費**
- 修正為 **$0 stack**：Gemini 2.5 Flash 免費層 + Vercel/Fly.io/Supabase/GitHub Actions 全免費
- Lily 補：**已訂 Claude Max** → 開發階段 Claude Code 用量涵蓋
- **Q5 三工具評估**：Lily 提問「都會用到嗎」
- Claude 提三種選擇（全用 / 用 2 / 全用但 phase 分工）
- Lily 追問「Agency-Agents 是 Agency Swarm？」→ **Claude 發現重大認知錯誤**
- WebSearch 校正：Agency-Agents = Flavio Copes 232 markdown persona 集合，**跟 Agency Swarm 完全無關**
- Q1-7 draft 校正、tech stack 簡化（runtime 不需 Agency Swarm）
- Lily 3 lock：$0 stack ✅、Q5 三工具全用 phase 分工 ✅、Agency Swarm 先跳過 ✅

**產出**：
- Tech stack Locked（見 spec.md）
- Q1-7 draft 修正 Q4/Q5 對 Agency-Agents 的描述
- 認知教訓：**工具名稱要 WebSearch 驗證，不要憑名字聯想**（Q3 反思材料）

### Phase 10: Mockup 展示 + Scope 擴增（~30 min）

**發生的事**：
- Lily 問「開發部署 workflow / dev 資料哪裡來 / 給皮」
- Claude 寫 2 個 static HTML mockup（store.html + dashboard.html），彈瀏覽器
- Lily 問「這是 dev 不是 prod 對嗎」→ Claude 澄清定位：**Demo/Staging environment with prod-grade CI/CD**
- Lily 要求看完整 product picture vs demo picture 對照 → Claude 產出 3-column matrix
- Lily 決定 promote 4 個功能從 mature → demo：**訂單查詢 / 退貨啟動 / 多語 / 真人 handoff**
- 5 min demo storyboard 重寫成完整買家旅程版本
- 建立 `product-vision.md` 存完整願景 + 3-phase roadmap + 面試講述模板

**產出**：
- `mockup/store.html`、`mockup/dashboard.html`（給 Lily 視覺化預覽）
- `product-vision.md`（完整願景文件，面試材料）
- spec.md 更新：C 端功能 +4、一週藍圖 refine、Demo storyboard 定稿

**觀察**（Q3 反思）：
- Mockup 先於 code 是對的：Lily 看到具體才能判斷 scope
- Scope 擴增雖然吃 Day 6 buffer，但換來「完整旅程」demo，值
- Post-demo roadmap 講述在面試最重要，這個模板 Day 6 收尾要複習

### Phase 11: 進行中 — 建專案骨架

（下一步）

---

## Day 1 觀察 / 反思（給 Q3 用）

**做得好**：
- 沒有跳過 requirements 直接寫 code，避免 rework
- 兩層痛點框架（戰略 + 體驗）比單層乾淨
- WebSearch 驗證工具真偽（避免答錯 Q1-2）
- 每個決策都有 rationale 記錄

**如果重來會改**：
- Claude 初擬痛點時應該先問 Lily 是否有 commerce 視角，不會兩批合併後才發現
- Shopify Plus 這個定位資訊應該 Phase 0 就問，不會走到 Phase 6 才修正

---

## Day 2+ 待填
