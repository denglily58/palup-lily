# Q1-7 答案（面試交付版）

**專案**: LUNA × Lily（PalUp AI Agent Designer take-home）
**Live URL**: https://palup-lily.vercel.app · https://palup-lily.vercel.app/admin
**Repo**: https://github.com/denglily58/palup-lily
**耗時**: 2026-09-08 → 2026-09-10（3 個 calendar day）

---

## Q1: AI Agents（OpenClaw, Hermes 這類）最重要的精神是什麼？

**三個精神**：

**1. Autonomy（自主 loop）**
Agent 不是「你問我答」的 chatbot——它有目標、有工具、會自己決定何時呼叫哪個 tool、何時該停止。我在 LUNA × Lily 用 Gemini function calling 讓 Lily-C 自主 route 到 5 個 tools（orders / returns / handoff / demand_gap / catalog），面試官打「where is my order」時 agent 自動抽出 email → 呼叫 lookup → 產生回覆——這個 loop 就是 autonomy 的最小單位。

**2. Persistent Memory（跨 session 記憶）**
Hermes 的 GEPA 三層記憶、OpenClaw 的 session 續存都在解同一個問題：agent 需要「知道你剛才講過什麼」+「記得專案 context」。我在 backend 實作了 10-message context window（in-memory）+ Supabase persistent conversation log，讓 Lily-C 記得「太 warm → 換 cool」的追問，Lily-B 能查跨 session 的買家歷史。

**3. LLM-Agnostic Architecture（可插拔）**
真正的 agent 系統把 model 當**可替換 config**，不是硬 dependency。我遇到 gemini-3.6-flash 免費層 20 req/day 用光→ swap 到 3.5-flash-lite，只改 `backend/agents/model_registry.yaml` 一個字，其餘 code 不動。這就是「LLM-agnostic」帶來的抗風險能力。

**面試講述金句**：Agent = **自主 loop + 持久記憶 + 可替換 brain**。三者缺一，只是 chatbot。

---

## Q2: 目前用 AI Agents 最需要注意/解決的問題？

**5 個真痛點，全部我這 3 天親身踩到**：

**1. Model 版本頻繁失效**
Google 一天內把 gemini-2.5-flash、2.5-flash-lite 都標 "EOL for new users"，強推 gemini-3.6-flash 又只給 20 req/day 免費。**解法**：`model_registry.yaml` 記 primary + fallback chain + 每次 swap 附 reason。任何生產級 agent 都需要這個。

**2. 幻覺（Hallucination）尤其在 structured data**
Agent 可能編造商品名、價格、訂單編號。**解法**：`agents/prompts/lily_c_en_v1.md` 明寫「Never make up product names, prices, or reviews」+ 用 function calling 強制查真資料，而不是靠 model 「記」。實測 Lily-C 引用的每個評論都是 seed 裡真實資料。

**3. Cost / rate limit 透明度**
Merchant 對「AI 每個月要多少錢」看不到→ 不敢投放。**解法**：backend `/metrics` 端點 + B 端 AI Usage widget，顯示累計 tokens + $ estimate（付費層計價）。實測 3 天累積 85k tokens = $0.007，讓 merchant 看見規模。

**4. 觀察性（Observability）**
Multi-agent 出錯難 debug。**解法**：event_logs table 記每個 action（login/chat_query/handoff/return）+ Supabase Realtime 讓 admin dashboard 即時看見。買家的每一次對話 3 秒內出現在 merchant 面前。

**5. Handoff 品質（Agent → Human）**
Agent 承接不住時，交接給人的 context 完整度=產品是否好用的關鍵。**解法**：`handoff_inbox` 表存完整 transcript + urgency + reason，B 端有 dashboard 專區。實測 seed 10 handoff 有 8 準時 2 超時，SLA 80% 可見。

**面試講述金句**：這 5 個不是理論，我 3 天內每一個都遇到、每一個都在 repo 裡有 fix commit。

---

## Q3: 這個專案怎麼執行的？過程是什麼？

**7 個階段**（完整過程見 `process-log.md`，18 個 phase 記錄）：

**Phase 0-2（Day 1 上午）— 情報 + 對齊**
先驗證作業列的 6 個工具（Superpowers/Gstack/Agency-Agents/OpenClaw/Hermes/Agent Army）是否真實 → 全都真。同時研究 PalUp 公司 = 宇泰華科技，主打 Shopify Plus 商家的 Aria 產品 → 決定 demo 要對齊「Shopify Plus 北美美妝品牌」情境。

**Phase 3-6（Day 1 下午）— 需求收斂**
拆解成 dual-actor（C 端買家 + B 端內勤 merchant）。痛點盤點兩層：戰略層（錢+信任）+ 體驗層（UX 摩擦）合併成 12 buckets。垂直領域選定 = 美妝 = 虛構品牌 LUNA Beauty。**關鍵 turning point**：意識到這是 dual-purpose deliverable（40% product / 60% Q1-7 evidence）。

**Phase 7-10（Day 2）— 基礎建置**
安裝 Superpowers plugin + Gstack skill 包 + Agency-Agents 231 persona 庫。建 Next.js + FastAPI 專案。跑通第一個 Lily-C hello world。做 5 份 seed data（10 SKU / 25 reviews / 30 orders / shipping / policies）+ 商品目錄 tool + session memory + token log。

**Phase 11-14（Day 2 續）— Multi-actor + 認證**
Supabase Auth setup + 3 seed merchant 帳號（Emily/David/Alex）+ event_logs realtime + Lily-B 分析師人格 + B 端 dashboard 6 widgets。用 Gemini function calling 讓 Lily-C 會查訂單 / 退貨 / handoff / 記錄 demand gap。

**Phase 15-17（Day 3）— UI polish + Version Control**
LUNA store 首頁 + 10 商品用 Unsplash 真圖 + chat widget 浮右下。8 個 Agent Army sub-agents 定義完備。Version Control 5 層：prompt md + model_registry.yaml + CHANGELOG + migrations README + agents.yaml（runtime load 從 md 檔）。

**Phase 18（Day 3）— 3-lens spec review**
用 Gstack `plan-eng-review` + Agency-Agents `product-manager` + `code-reviewer` 三個角度 review spec，找出 19 個 findings 分 must-fix/should/nice，回填修正。這是**動用 skill packs 的實錄**。

**Phase 19（今 Day 3-4）— Deploy**
GitHub Actions ci.yml (linter/security/test) + deploy.yml (fly + vercel + health-check + rollback) + Fly.io backend + Vercel frontend + Supabase realtime，14 個 git commits 全公開。

**面試講述金句**：不是 waterfall、也不是純 sprint，是「**每個 phase 完成就 write 進 process-log**，然後從 log 迭代 spec」——過程即產出。

---

## Q4: 開發時調用哪些 Open source Agents 管 Sub-Agents？

**4 種，都實際用過**：

**1. Claude Code 內建 sub-agent**（主力）
- `Explore` — 跨檔案搜尋 / grep symbol
- `Plan` — 架構規劃前用
- `claude-code-guide` — Claude Code / API 諮詢
- 每天 dev 中不斷 spawn，是 Q4 最實在的工具

**2. Superpowers `subagent-driven-development` skill**（Day 3 spec review 時用）
自動 spawn parallel sub-agent 做 code review + verify-before-completion 5-phase discipline

**3. Agency-Agents persona library**（Q6 Agent Army 藍本來源）
從 231 個 persona 挑 `engineering-code-reviewer`、`engineering-devops-automator`、`engineering-git-workflow-master` 改寫成 CI/CD 8 個 sub-agent（見 `sub-agents/*.md`）

**4. Agency Swarm（評估後未採用）**
Python runtime multi-agent 框架。原打算用它 orchestrate Lily-C + Lily-B，但發現直接用 FastAPI + Gemini function calling 更輕（KISS 原則），Agency Swarm 移到 `product-vision.md` Phase 1 roadmap。

**面試講述金句**：Claude Code sub-agent 是**主力**、Superpowers 補**紀律**、Agency-Agents 提供**現成 persona 藍本**、Agency Swarm 是**可選 runtime**——四者角色不衝突。

---

## Q5: Superpowers / Agency-Agents / Gstack 如何協助您開發？

**三個 skill pack，各自負責不同 phase**：

**Superpowers（obra / Prime Radiant，14 skills）— Dev 過程紀律**
- `writing-plans` — spec 撰寫前用（Day 1 我先寫 plan 再寫 spec.md）
- `test-driven-development` — 寫 code 前，讓 sub-agent 先想測試案例
- `subagent-driven-development` — Day 3 3-lens review 時 spawn 平行檢查
- `verification-before-completion` — 每次「宣稱完成」前強制 curl 驗證，避免我自欺
- `systematic-debugging` — 遇 bug（Docker COPY 語法、Python 3.9 `str | None`、CORS）時用

**Gstack（Garry Tan，23 skills）— Ship 過程紀律**
- `plan-eng-review` — 3-lens spec review 的**其中 1 lens**，找出 seed data schema/session ID/cross-agent DB 3 個 must-fix
- `setup-deploy` — CI/CD workflow 撰寫時 reference
- `ship` — Day 6 部署前的 checklist
- `guard` — security review 前用

**Agency-Agents（msitarzewski，231 persona）— 現成藍本**
- `product/product-manager` — 3-lens review 的另一 lens
- `engineering/code-reviewer` — 3-lens review 的第 3 lens
- `engineering/devops-automator` — `sub-agents/deploy-agent.md` 的原型
- `engineering/git-workflow-master` — `docs/git-workflow.md` GitHub Flow 決策參考

**面試講述金句**：Superpowers 教我**如何開發**，Gstack 教我**如何 ship**，Agency-Agents 給我 231 個**專家範本**。三者是 dev tool 不是 runtime——這區隔面試官會加分。

---

## Q6: 如何調用 Agent Army 管理 CI/CD？

**8 個 sub-agent，全在 `sub-agents/` 目錄，全部連接 GitHub Actions**：

| # | Sub-agent | 觸發 | 職責 |
|---|---|---|---|
| 1 | linter-agent | push | ruff + eslint 靜態分析 |
| 2 | security-agent | push | 依賴 CVE + secret 洩漏掃描 |
| 3 | test-runner-agent | push | pytest + import smoke test |
| 4 | e2e-agent | main | Playwright 5 個 critical scenario |
| 5 | deploy-agent | main + all green | flyctl + vercel 平行部署 |
| 6 | health-check-agent | 部署完 | 5 個 endpoint smoke test |
| 7 | rollback-agent | health fail | flyctl releases rollback |
| 8 | pr-reviewer-agent | PR opened | 自動 review + 引 CLAUDE.md 慣例 |

**自動化程度矩陣**：

| Stage | 全自動 | Alert | Human 決策 |
|---|---|---|---|
| Lint | ✅ | warning 提示 | 無 |
| Security | ✅ | 高風險 block | Merge 時決策 |
| Test | ✅ | 失敗 alert | 修 or ignore |
| Deploy | ✅ | 開始/完成通知 | 無 |
| Health | ✅ | 失敗自動觸發 rollback | 無 |
| Rollback | ✅ | 執行後 alert | 無 |
| PR Review | ✅ | 有 blocker 提示 | Merge 決策 |

**自動化 Level = 4/5**，human-in-the-loop 只在 merge 決策 + release note 潤飾。

**Pipeline 實錄**：Day 6 部署觸發真實 flow：GitHub push → Actions 跑 CI (3 job) → 全綠 → deploy job → Fly deploy 成功 → Vercel deploy 成功 → health check 5/5 綠 → done。全程約 3-5 分鐘。實錄可看 [github.com/denglily58/palup-lily/actions](https://github.com/denglily58/palup-lily/actions)。

**面試講述金句**：8 個 sub-agent 不是 markdown 擺著看的，是**真的接上 GitHub Actions workflow yaml、真的跑過、失敗真的會 rollback**。這是 pipeline 不是幻燈片。

---

## Q7: 多 Agents 協同執行 20000 行 codes 大約要花多少錢多少時間？

**本專案實測數據**（來自 `metrics.md` + `backend/logs/chat_logs.jsonl`）：

| 指標 | 值 |
|---|---|
| 開發總時長 | 3 個 calendar day（實工作 ~20 hr） |
| Code LoC 產出 | ~2000 行（frontend + backend + tools + agents） |
| Docs LoC 產出 | ~1500 行（spec / architecture / process-log / metrics / q1-7-draft / product-vision / CHANGELOG / git-workflow / sub-agents × 8） |
| Chat 次數（agent runtime） | 34 |
| Tokens 總量 | 85,479（82.7k input + 2.7k output） |
| API 成本（as-if 付費） | $0.007（實際 $0，Gemini 免費層） |
| Claude Code 用量 | 由 Lily Max 訂閱 cover（無變動費） |

**單位成本**：
- $/LoC = $0.007 / 2000 = $0.0000035（runtime API 成本，趨近於 0）
- min/LoC = 20 hr × 60 / 2000 = 0.6 分鐘（含 debug + iteration + Claude Code 對話）

**外推 20000 行 code**：

**線性外推**（naive）：
- 時間：0.6 × 20000 = 12000 min = **200 hr ≈ 25 個工作天（1 人 8hr/day）**
- 成本：$0.007 × 10 = $0.07（runtime tokens）+ Claude Code Max ~$100（1 個月 subscription）

**現實外推（含 non-linear 因素）**：
| 變數 | 影響 |
|---|---|
| 從零 vs. brownfield | 從零 exploration 多 ~30% |
| 有無詳細 spec | 有 spec 省 ~40% |
| Model 選擇 | Opus 貴但少錯、Haiku 便宜但需多輪 |
| 複雜度 | CRUD × 1x / 演算法 × 2-3x / 分散式 × 5x+ |
| Multi-agent overhead | Orchestration + inter-agent 溝通 +20-40% |
| Human review 頻率 | 高 review 慢但錯少 |
| Prompt caching | 命中省 90% cost |

**現實估算 20000 行**：
- 時間：**35-50 個工作天**（1 人 + Claude Code Max）
- 成本：**$100-500**（含 API + Claude subscription）
- 若 3 人平行：**15-20 天**、成本 3 倍但總 wall-clock 快 3x

**面試講述金句**：本專案 3 天做 2000 行 + docs + deploy + spec，單位成本趨近 $0（Gemini 免費層 + Claude Max 打底）。**線性外推騙人——真正 scale 到 20000 行**要考慮 complexity 非線性 + orchestration overhead + human review frequency。**pipeline 對齊、agent tooling 對齊，才是效率關鍵**，不是 raw model 選擇。

---

## Bonus: 面試 additional talking points

**Live URLs**（面試官可自己玩）：
- Store: https://palup-lily.vercel.app
- Admin: https://palup-lily.vercel.app/admin （emily@luna.beauty / LunaDemo2026!）

**GitHub commits 時間軸**（14 commit，3 天）：
- Day 1（09-08）：需求 + 骨架 + hello world
- Day 2（09-09）：seed + agent tools + auth + realtime + version control
- Day 3（09-10）：Docker + deploy + UI polish + Q1-7 定稿

**若被問「下一步 roadmap」** → 翻 `product-vision.md`（3 phase：MVP→Beta→Enterprise）

**若被問「為什麼 demo 用 Gemini 不用 Claude」** → LLM-agnostic 架構驗證 + 免費層 cost design + Claude Code 全程開發（Claude 生態核心其實在 dev tool，不在 runtime）
