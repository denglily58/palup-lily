# Agent Army — CI/CD Sub-Agents

**Q6 素材**：Claude Code sub-agent 定義集合，管理 LUNA × Lily 專案的 CI/CD 全流程。

## 分工全景

```
┌─────────────────────────────────────────────────────────┐
│                    git push                              │
└────┬───────────────────────────────────────────────────┘
     │
     ▼  (平行執行)
┌────────────┐  ┌────────────┐  ┌────────────────┐
│ linter     │  │ security   │  │ test-runner    │
│ agent      │  │ agent      │  │ agent          │
└──────┬─────┘  └──────┬─────┘  └──────┬─────────┘
       │                │              │
       └────────────────┼──────────────┘
                        │
                    (若在 main branch)
                        │
                        ▼
                 ┌─────────────┐
                 │ e2e-agent   │
                 └──────┬──────┘
                        │ (全綠)
                        ▼
                 ┌─────────────┐
                 │ deploy-agent│───→ Fly.io backend + Vercel frontend
                 └──────┬──────┘
                        │
                        ▼
                 ┌──────────────────┐
                 │ health-check     │
                 │ -agent           │
                 └──────┬───────────┘
                        │
              ┌─────────┴──────────┐
              │(pass)          (fail)
              ▼                    ▼
        ┌──────────┐        ┌──────────────┐
        │changelog-│        │ rollback-    │
        │agent     │        │ agent        │
        └──────────┘        └──────────────┘

  PR opened → pr-reviewer-agent (自動 review)
```

## 已建立的 stubs（Day 3 進度）

| # | Agent | 檔案 | 狀態 |
|---|---|---|---|
| 1 | linter-agent | `linter-agent.md` | ✅ stub |
| 2 | security-agent | `security-agent.md` | ✅ stub |
| 3 | deploy-agent | `deploy-agent.md` | ✅ stub |
| 4 | test-runner-agent | `test-runner-agent.md` | ⏳ Day 5 |
| 5 | e2e-agent | `e2e-agent.md` | ⏳ Day 5 |
| 6 | health-check-agent | `health-check-agent.md` | ⏳ Day 5 |
| 7 | rollback-agent | `rollback-agent.md` | ⏳ Day 5 |
| 8 | pr-reviewer-agent | `pr-reviewer-agent.md` | ⏳ Day 5 |

## 自動化程度矩陣（Q6 講述用）

| Stage | 全自動 | Alert 提示 | Human 決策 |
|---|---|---|---|
| Lint | ✅ | warning 提示 | 無 |
| Security | ✅ | 高風險強制 block | Merge 決策 |
| Test | ✅ | 失敗 alert | 修 or ignore |
| Deploy | ✅ | 開始/完成通知 | 無 |
| Health check | ✅ | 失敗自動觸發 rollback | 無 |
| Rollback | ✅ | 執行後 alert | 無 |
| Changelog | ✅ | 無 | Release note 潤飾 |
| PR Review | ✅ | 有意見時提示 | Merge 決策 |

**自動化 Level = 4/5**（human-in-the-loop 只在 merge decision + release note 潤飾）

## 命名與格式規範

每個 sub-agent .md 檔結構：
- **YAML frontmatter**：`name / description / tools 白名單 / version / adapted_from`
- **Role 說明**：這個 agent 做什麼、不做什麼
- **When to Trigger**：何時該 spawn
- **Workflow**：實際步驟（bash / API calls）
- **Output Format**：產出的 markdown 模板
- **Critical Rules**：不可違反的原則
- **Downstream**：這個 agent 完成後接誰

## 未來 Day 5 要接上的

Day 5 會把這些 stubs **實際接進 GitHub Actions workflow**：
- `.github/workflows/ci.yml` 觸發 linter/security/test-runner/e2e
- `.github/workflows/deploy.yml` 觸發 deploy → health-check → (fail) rollback
- 用 Claude Code CLI + sub-agent 呼叫實現
