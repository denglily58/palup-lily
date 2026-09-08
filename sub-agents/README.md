# Agent Army 定義（Q6 素材）

Day 5 會在這個目錄放入所有 CI/CD 相關的 Claude Code sub-agent 定義。

## 目前計畫收錄

| 檔名 | 職責 |
|---|---|
| `linter-agent.md` | 靜態分析（ruff / eslint） |
| `security-agent.md` | 依賴 + 密鑰掃描 |
| `test-runner-agent.md` | 跑 unit + integration |
| `e2e-agent.md` | Playwright e2e |
| `deploy-agent.md` | 部署到 Cloud Run |
| `health-check-agent.md` | 部署後 smoke test |
| `rollback-agent.md` | health check 失敗自動回滾 |
| `changelog-agent.md` | 從 commit 生 CHANGELOG |
| `pr-reviewer-agent.md` | PR 自動 review |

## 每個 sub-agent 檔案格式

```markdown
---
name: <name>
description: <一句話>
tools:
  - Bash
  - Read
  - <只列必要的白名單>
---

# 職責

# 使用時機

# 執行流程

# 產出格式
```

（Day 5 逐檔填入）
