# Git Workflow — LUNA × Lily

**Chosen: GitHub Flow** (single main + feature branches + PR + auto-deploy).

## Why GitHub Flow (not Git Flow / Trunk / GitLab Flow)

- **Scale**: solo dev, single deployment target → don't need Git Flow's `develop`/`release`/`hotfix` complexity
- **Cadence**: continuous deploy on merge → matches Trunk-based intent without needing feature flags
- **Discipline**: PR review gate + CI required → matches Agent Army (pr-reviewer-agent, linter-agent, etc.)

## Rules

1. **`main` is always deployable** — never push broken code
2. **New work opens a feature branch**: `feature/<short-name>` or `fix/<bug>` or `docs/<what>`
3. **Open a Pull Request** — even solo, forces self-review + triggers pr-reviewer-agent
4. **CI must be green** before merge:
   - `linter-agent` ✅
   - `security-agent` ✅
   - `test-runner-agent` ✅
5. **Merge to main** triggers deploy pipeline:
   - `deploy-agent` (Fly.io + Vercel)
   - `health-check-agent` (5 smoke tests)
   - `rollback-agent` if health check fails

## Branch Protection (recommended)

Enable on GitHub → Settings → Branches → Add rule for `main`:

- [x] Require pull request before merging
- [x] Require status checks to pass:
  - `linter-agent` / `security-agent` / `test-runner-agent`
- [x] Require branches to be up to date before merging
- [ ] Restrict pushes (leave off for solo dev; enable if team)

## Take-home Scope Note

Take-home has 1 deployment target (`main` → Fly.io + Vercel, called "prod" for URL naming but really a demo env — see `spec.md` "Demo/Staging env with prod-grade CI/CD").

For scale to real 3-env (dev / staging / prod), see `product-vision.md` Phase 1.

## Commit Message Convention

`type: short summary`

**Types**: `feat / fix / docs / chore / refactor / test / perf / style`

Examples (from repo history):
- `feat(v0.3): order/return tools via Gemini function calling + CHANGELOG`
- `chore: CI/CD workflows + fly.toml + vercel.json for deploy`
- `docs: log Day 4 + Day 5 execution in process-log`

## Trunk-based Fallback (if solo push discipline breaks)

If solo work makes PR overhead annoying, minimally:
- Still open PR (auto-merge is fine)
- Never disable CI
- Never `--no-verify` commits

The pipeline is your safety net — bypassing it defeats the purpose.
