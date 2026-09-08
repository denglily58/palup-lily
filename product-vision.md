# LUNA Botanica × Lily — Product Vision

**Purpose**：完整產品願景 + 3-phase roadmap。面試講「demo 之外還想做什麼」時翻這份。
**當前 demo 範圍請看** `spec.md`。

---

## 一句話定位

**Lily = Shopify Plus 品牌用的 AI 業務員 + 客服 + 內勤分析師（同一個大腦、C+B 雙人格）**

- **C 端（Lily-C）**：24/7 專業級品牌代言人 — 推薦、售後、多語、handoff
- **B 端（Lily-B）**：對話式 AI 分析師 — 把買家訊號即時翻譯成商業洞察 + 可 pin 自訂 dashboard
- **關鍵**：兩端同一大腦、資料互通。讓品牌從「賣東西」升級為「懂顧客」

---

## 差異化（vs 通用 chatbot / vs Zendesk-like）

| 維度 | 通用 chatbot | Zendesk 客服 | **Lily** |
|---|---|---|---|
| 是否會「賣」 | ❌ | ❌ | ✅ 業務+客服合一 |
| 品牌 tone 一致 | ⚠️ 通用 | ⚠️ 需 script | ✅ 品牌客製 |
| 對內勤有洞察 | ❌ | ⚠️ 靜態報表 | ✅ 即時 conversational BI |
| 需求缺口捕捉 | ❌ | ❌ | ✅ 自動化 |
| Pin 自訂 dashboard | ❌ | ❌ | ✅ |
| 端到端閉環 | ❌ | ❌ | ✅ 買家對話 → 內勤洞察 → 商品/採購決策 |

---

## 完整產品願景（12-24 個月後）

### C 端 Lily-C

| 功能 | Demo 版 | 成熟 |
|---|---|---|
| 主動 greet + 商品推薦 | ✅ 3 支 + 引評論 | ✅ + 拍臉分析膚色 + 記歷史 |
| 引評論 | ✅ 靜態摘要 | ✅ + real-time 語意搜尋 |
| 物流 ETA | ✅ | ✅ + 真物流 API |
| Upsell / 加購 | ✅ | ✅ + 個人化 offer |
| 誠實不會 → 記缺口 | ✅ | ✅ + 通知採購 |
| **訂單查詢** | ✅ 淺實作 | ✅ + 改地址、取消、退款 |
| **退貨啟動** | ✅ 淺實作 | ✅ + 真接物流商 + 條碼 |
| **多語** | ✅ 中/英 | ✅ 7 語 + 專業校對 + 多幣別 |
| **真人 handoff** | ✅ 進 B 端 inbox | ✅ + 真接 Zendesk / 內建 IM |
| Cart-in-chat 結帳 | ❌ | ✅ 對話內結帳 |
| 語音 / 拍照選色 | ❌ | ✅ |
| Post-purchase 回訪 | ❌ | ✅ 鼓勵留評 |

### B 端 Lily-B / Dashboard

| 功能 | Demo | 成熟 |
|---|---|---|
| 4 starter widgets | ✅ | ✅ 即時更新 |
| Chat 問數據 | ✅ 1-2 scripted | ✅ 無限深挖 |
| Pin 存卡片 | ✅ | ✅ 真存帳號 + 排序 |
| 商業指標 | ✅ 對話/轉單/營收 | ✅ + 毛利/LTV/CAC/留存 |
| 需求缺口 | ✅ Top 3 | ✅ + 自動採購建議 |
| Handoff inbox | ✅ | ✅ + SLA 追蹤 |
| 客群分析 / 情緒 / 急迫度 | ❌ | ✅ |
| 異常告警推 Slack | ❌ | ✅ |
| 內容生成（SEO / 廣告文） | ❌ | ✅ |
| 多帳號 / RBAC | ❌ | ✅ |
| 匯出 Excel / BI | ❌ | ✅ |

### 架構

| 層 | Demo | 成熟 |
|---|---|---|
| Agent 數 | 2（Lily-C + Lily-B） | 10+ 專業 agent |
| Multi-LLM 路由 | 單 Gemini | Cost-aware（Haiku 分類 / Sonnet 對話 / Opus 分析） |
| Memory | 對話內 | 長期 per customer |
| 多 tenant | 單店 | 多 merchant |
| 整合 | Mock Shopify | 真 Shopify Plus + Klaviyo + Slack + IG DM + WhatsApp |
| Guardrails | 基本 | Prompt injection defense + 內容審查 |
| Compliance | 無 | SOC 2 / GDPR / CCPA |
| CI/CD | 8 sub-agents | 8 + eval pipeline + A/B testing |

---

## 3-Phase Post-Demo Roadmap

### Phase 1（0-2 個月）— MVP → Beta
- 真接 Shopify Plus API（商品/訂單/退貨/物流）
- 客戶長期記憶（每人對話歷史 + 偏好）
- Eval pipeline（自動評估答案品質）
- 品牌 tone 客製（onboarding wizard）
- 第一個 pilot 品牌上線

### Phase 2（3-6 個月）— Beta → GA
- 多語（EN / JP / CN / KR / ES / DE / FR）
- 語音輸入 + 拍照選色
- 真人 handoff 接 Zendesk / Intercom
- 多通道（IG DM / WhatsApp / LINE）
- Cart-in-chat 結帳
- 客群分析 / 情緒偵測

### Phase 3（6-12 個月）— Enterprise
- 多 tenant SaaS
- Klaviyo / Slack / Amplitude 整合
- SOC 2 + GDPR compliance
- 內容生成（SEO / 廣告文）
- RBAC 多帳號
- Enterprise SSO
- 匯出 Excel / BI 工具

---

## Success Metrics Vision

**Merchant 端 KPI（愛用度）**
- Merchant 每天登入 dashboard 次數
- Pin widget 數量（自訂化程度）
- Chat 追問頻率（探索深度）
- 存活月數（retention）

**Merchant 端 KPI（業務價值）**
- 對話 → 轉單率
- 平均 AoV 提升幅度
- 需求缺口被採納率
- 客服人力節省時數

**買家端 KPI（體驗）**
- 對話滿意度（thumbs up rate）
- Handoff 前 Lily 解決率
- 幻覺率（客訴中 AI 錯誤佔比）

---

## 面試講述模板

### 若被問「demo 之外你會怎麼往下做」

「Demo 是最小可用的 slice。Phase 1 我會先把 seed data 換成真 Shopify Plus API，加客戶長期記憶跟 eval pipeline —— 這是所有升級的地基。Phase 2 是**廣度擴張**（多語、多通道、handoff 真接第三方），把品牌能觸及的客群變大。Phase 3 才是**enterprise 化**（多 tenant、整合、compliance），這是變成 SaaS 生意的必經之路。」

### 若被問「Lily 的差異化是什麼」

「跟 Zendesk 這類客服工具比，Lily 會**賣東西**；跟通用 chatbot 比，Lily **只服務一個品牌**、tone 客製；跟純 dashboard 比，Lily 是 **conversational BI + 端到端閉環**（買家問的問題自動翻譯成商業洞察）。Shopify Plus 品牌值錢的地方就是這個閉環。」

### 若被問「為什麼選 Shopify Plus 不是 SMB」

「Plus 品牌客單價高、對話量大、對品牌 tone 敏感、有付費能力。SMB 用免費 chatbot 就行；Plus 需要能懂品牌、能上洞察、能救 escalation 的專業助理。這也是 PalUp 的 Aria 選擇的市場。」

### 若被問「為什麼 demo 用 Gemini 不是 Claude」

「Agent 架構應該 LLM-agnostic —— 是 Q2 我提到的『供應商鎖定』痛點。Demo 用 Gemini 免費層驗證架構是可插拔的，production 只要改一個 config 就能換成 Claude。開發過程我全程用 Claude Code + Superpowers + Gstack + Agency-Agents，這才是核心 Claude 生態的展現。」
