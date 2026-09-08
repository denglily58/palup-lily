# Q1-7 答案 iterative draft

> **用途**：作業 7 道問答題的持續 draft。
> **策略**：每個 phase 有新素材就補進來，Day 6 統整成最終答案。
> **原則**：只寫實際發生的、有 root cause 的內容，不從網路 copy 教科書答案。

---

## Q1: AI Agents（OpenClaw, Hermes 這類）最重要的精神是什麼？

### 候選精神詞（Day 6 收斂到 3 個）
- **自主性 (autonomy)** — agent 自己 loop 決策，不是 chatbot 你問我答
- **持久記憶 (persistent memory)** — 跨 session 記得你/專案/環境（Hermes 三層記憶）
- **動作能力 (action-taking)** — 不只講話，會操作工具/API/檔案
- **多通道 (multi-channel)** — 一個 agent 跨 Slack/Discord/Web/CLI（OpenClaw 12+ 通道）
- **自我演化 (skill self-evolution)** — Hermes GEPA、Skills 自動改進
- **意圖對齊 / action space** — 明確定義可做什麼，可預測可 debug（OpenClaw 特色）

### 待補實證
- Day 6：spin up OpenClaw or Hermes 做一個小任務，親身感受其精神
- 過程中觀察 Claude Code sub-agent 的行為，反推 agent 定義

---

## Q2: 目前最需要注意/解決的問題？

### 候選問題
- **幻覺 (hallucination)** — 對商業/財務資料尤其危險（假評論、假訂單、假折扣）
- **成本控管 (cost drift)** — token 開銷失控，尤其多 agent 對談
- **記憶漂移 (memory drift)** — 錯的記憶反覆用會強化
- **可觀測性 (observability)** — 多 agent 分散決策，出錯難 debug
- **安全 (safety)** — action-taking agent 存取權該多大（能不能發 refund？取消訂單？）
- **一致性 (consistency)** — 同一問題不同 session 給不同答案，品牌形象受傷
- **Handoff 品質** — agent 交給人時資訊完不完整
- **Prompt injection** — C 端使用者惡意輸入操縱 agent

### 待補實證
- 過程中我們踩到哪些坑（Day 2-6 持續記錄）
- 我們的解法（Day 6 統整）

---

## Q3: 這個專案怎麼執行的？過程是什麼？

→ 完整過程見 `process-log.md`。Day 6 統整成敘事版本。

**敘事骨架**（Day 6 展開）：
1. 情報收集：驗證 6 個工具真偽 + 挖 PalUp 產品定位
2. 對齊工作模式：PM+Eng+Design 三角
3. 需求拆解 → 痛點盤點 → scope 收斂
4. 垂直領域選定
5. 建置 → 迭代 → 部署
6. 反覆對照 Q1-7 收集素材

---

## Q4: 開發時調用哪些 Open source Agents 管 Sub-Agents？

### 已計畫使用
- **Claude Code 內建 sub-agent** — Explore（搜尋）、Plan（架構規劃）、claude-code-guide（Claude Code/API 諮詢）
- **Superpowers `subagent-driven-development` skill** — subagent + code review 內建流程
- **Agency-Agents persona library** — 從 232 個 markdown persona 挑合適的當 sub-agent 藍本

### 待評估後決定（可能不用，避免 tool bloat）
- **Agency Swarm** — Python runtime 框架，可作為進階加分
- **aider / Continue / OpenHands / CrewAI** — 若時間允許

### 待補實證
- 每個工具在專案哪個階段用到、幫了什麼
- git commit 佐證 or process-log 對應 phase

---

## Q5: Superpowers / Agency-Agents / Gstack 如何協助開發？

### Superpowers（Jesse Vincent / Prime Radiant）
**計畫使用的 skills**（Day 2 安裝後補實際使用）：
- `brainstorming` — Day 1 需求發散階段（回溯性用）
- `test-driven-development` — Day 3-4 寫核心 agent 時
- `subagent-driven-development` — Day 3-5 平行分工
- `systematic-debugging` — 遇到 bug 時
- `writing-plans` — Day 1 spec / 各 feature 前

### Gstack（Garry Tan）
**計畫使用的 skills**：
- `planner` — Day 1 spec, Day 2-5 每個 feature 前
- `engineer-review` — 每個 PR 前
- `browser-qa` — Day 4 UI 完成後
- `release-check` — Day 5 CI/CD 上線前
- `shipping-discipline` — Day 6 收尾

### Agency-Agents（Flavio Copes）— ⚠️ 校正：不是 Agency Swarm
**是什麼**：232 個 markdown 定義的 AI agent persona 集合（16 divisions），用於 Claude Code / Cursor。
**計畫用到的 personas**（Day 2 後補實際用到的）：
- `senior-frontend` — Next.js chat UI
- `backend-architect` — FastAPI 結構
- `security-reviewer` — Day 5 CI/CD 前
- `product-copywriter` — Lily 對話 tone
- （Day 2-5 挑更多）

### （可選加分）Agency Swarm（VRSEN）
不在 Q5 範圍。若 Day 6 有時間可加為 runtime multi-agent orchestration。

### 待補實證
- 每個 skill/role 在專案哪裡用到、產出什麼、省了多少時間
- 截圖 or git commit 佐證

---

## Q6: 如何調用 Agent Army 管 CI/CD？

### 計畫的 Agent Army（Day 5 定稿）

| Sub-agent | 職責 | 觸發時機 |
|---|---|---|
| `linter-agent` | ruff / eslint 檢查 | git push |
| `security-agent` | 依賴掃描（Snyk-like）、密鑰洩漏檢查 | git push |
| `test-runner-agent` | 跑 unit + integration | git push |
| `e2e-agent` | Playwright 跑核心 flow | main 分支 push |
| `deploy-agent` | 部署到 Cloud Run | main 分支 push + 全綠 |
| `health-check-agent` | 部署後跑 smoke test | 部署完成 |
| `rollback-agent` | health check 失敗自動回滾 | health check 失敗 |
| `changelog-agent` | 從 commit 生 CHANGELOG | 每次 release |
| `pr-reviewer-agent` | PR 開啟時自動 review | PR opened |

### 自動化程度矩陣

| Phase | 全自動 | Alert 提示 | Human 決策 |
|---|---|---|---|
| Lint | ✅ | 有 warning 提示 | 無 |
| Security | ✅ | 高風險強制 block | Merge 時決策 |
| Test | ✅ | 失敗 alert | 修 or ignore |
| Deploy | ✅ | 開始/完成通知 | 無 |
| Health check | ✅ | 失敗自動觸發 rollback | 無 |
| Rollback | ✅ | 執行後 alert | 無 |
| Changelog | ✅ | 無 | Release note 潤飾 |
| PR Review | ✅ | 有意見時提示 | Merge 決策 |

**自動化程度**：Level 4/5（human-in-the-loop 只在 merge 決策 + release note 潤飾）

### 待補實證
- Day 5 實際寫的 sub-agent .md 檔（存 `sub-agents/`）
- GitHub Actions workflow YAML 對應 hook
- 至少一次「觸發 → 自動處理」的實錄

---

## Q7: 多 Agents 協同 20000 行 code 的成本 / 時間？

### 方法論
1. 追蹤本專案 (~2000-5000 行) 的實際 tokens / 時間 / 費用（見 `metrics.md`）
2. 算平均 $ / LoC 與 min / LoC
3. 外推 × 20000
4. **註明變數**（外推不是線性，要說清楚）

### 待補實測（Day 6 填）
- 本專案 LoC：
- 本專案總 tokens：
- 本專案總 $：
- 本專案總時間：
- 平均 $ / LoC：
- 平均 min / LoC：
- 20000 行外推 $：
- 20000 行外推時間：

### 變數說明（答案裡一定要提）
| 變數 | 影響 |
|---|---|
| 從零 vs. brownfield | 從零 exploration 多 ~30% |
| 有無詳細 spec | 有 spec 省 ~40% |
| Model 選擇 | Opus vs. Haiku 差 ~5x |
| 複雜度 | CRUD 1x / 演算法 2-3x / 分散式 5x+ |
| Multi-agent overhead | Orchestration + 溝通 tokens ~20-40% |
| Human review 頻率 | 高 review 慢但錯少 |
| Prompt caching 命中率 | 命中省 90% cost |

### 我的預估邏輯（Day 6 定案）
```
假設本專案 4000 LoC，總 $30，總 40 hours
→ $0.0075/LoC，0.6 min/LoC
→ 20000 行外推：$150，200 hours = 25 個工作天
（但實務不會線性，複雜度上升 → +40%，多 agent overhead +30%，故 real ~$270，~35 天）
```
