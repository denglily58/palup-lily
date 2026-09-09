# Metrics 追蹤（Q7 答案素材）

> **用途**：作業 Q7「多 Agents 協同執行 20000 行 code 大約要花多少錢多少時間」的實測基礎。
> **策略**：追蹤本專案的實際數字 → 外推 20000 行的估算。
> **維護**：每天結束時更新，Day 6 定稿時計算 unit cost 與外推。

---

## 追蹤欄位

| 欄位 | 說明 |
|---|---|
| 日期 | YYYY-MM-DD |
| 該日主要工作 | 一句話 |
| 產出 LoC | `git diff --stat` 或 `cloc` 算 |
| Model | Opus 4.7 / Sonnet 4.6 / Haiku 4.5（多 model 分開列） |
| Tokens | input / output 分開 |
| 花費 USD | 累計 |
| 純 dev 時間 | Lily 陪跑分鐘 vs. Claude 執行分鐘 |
| 使用工具 | Superpowers skills / Gstack skills / sub-agents 列名 |

---

## 自動收集機制（Day 3 起）

- FastAPI middleware：每次 `/chat` 完成後 insert 一筆到 Supabase `chat_logs` 表
- 欄位：`timestamp / endpoint / session_id / input_tokens / output_tokens / latency_ms / model / cost_estimate`
- Day 6 收尾用 SQL 一次拿全部聚合數字

### Gemini 3.6 Flash 定價（2026-09 查）
- 免費層：15 req/min、1500 req/day、1M tokens/min
- 付費層（如超）：$0.075 / 1M input tokens、$0.30 / 1M output tokens

**Demo 期間預估**：<$0 → 完全在免費層內

---

## 逐日紀錄

### Day 1 — 2026-09-08

| 項目 | 值 |
|---|---|
| 主要工作 | 需求收斂、spec 撰寫、process-log 撰寫、垂直領域選定 |
| 產出 LoC | 0（尚未寫 code） |
| 產出 Markdown 行數 | ~500 行（spec + process-log + metrics + q1-7-draft） |
| Model | Claude Opus 4.7 (1M context) |
| Tokens | 待從 Claude Code UI 看實際數字 |
| 花費 | 待估 |
| Lily 陪跑時間 | 待統計 |
| 使用工具 | Claude Code、WebSearch、Memory、TaskCreate |

### Day 2 — 待填
### Day 3 — 待填
### Day 4 — 待填
### Day 5 — 待填
### Day 6 — 待填
### Day 7 — 待填

---

## Day 6 外推計算（模板）

```
平均 $ / LoC = 總 $ / 總 LoC = ?
平均 min / LoC = 總分鐘 / 總 LoC = ?

20000 行外推：
- 錢：$ / LoC × 20000 = $ ?
- 時間：min / LoC × 20000 = ? min = ? hours = ? days
```

## 外推時要註明的變數

1. **從零 vs. brownfield**：從零寫比較貴（多 exploration）
2. **有無詳細 spec**：spec 越完整，token 越省
3. **Model 選擇**：Opus 貴但少錯、Sonnet CP 值高、Haiku 便宜適合 low-stakes
4. **複雜度**：CRUD × 1x / 演算法 × 2-3x / 分散式 × 5x+
5. **多 agent 開銷**：orchestration + 溝通 tokens 佔比
6. **Human-in-the-loop 頻率**：越多 review 越貴但錯越少
7. **Cache 命中率**：prompt caching 命中省 90% cost
