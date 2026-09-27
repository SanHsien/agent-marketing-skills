# Repository review（Windows-first）

- Review date: 2026-08-27
- Review baseline: 見本檔「已修」對應 commit；R-05／R-07 維持不改
- Upstream reviewed through: `b1aaa3619e747f4a836c61e03084c4a531de1262`
- Upstream watermarks: PR / issue `reviewed_pr_through` / `reviewed_issue_through` = **569**
- Primary environment: Windows 11、PowerShell、Python 3.14（本機）、CI Ubuntu 3.9–3.14、Windows 3.14、Node.js 22
- Status: 維護骨架可用；產品 `skills/`、`tools/clis/`、`tools/integrations/`、`.claude-plugin/` 未改寫；fork 可修的 R-01～R-04、R-06 已修

## 結論

這個 fork 適合作為 Windows 本機安裝、並追蹤上游行銷 Agent Skills 的維護線。產品是 50 個英文 skill 與 64 支零依賴 Node CLI；沒有獨立行銷引擎。

2026-08-27 覆核列出的 R-01～R-07，**fork 能修的都修了**（R-01～R-04、R-06）。**沒有**改寫產品 skill、**沒有**改 `.claude-plugin/plugin.json`、**沒有**把 `FUNDING.yml` 改掛到維護者、**沒有**回貢。

Windows CI 在 overlay 首推（`ff62783`）因 `CLAUDE.md` 仍是 git symlink 而在 checkout 失敗；已改存一般檔，測試會擋住再出現 `120000` blob。

## 已修 findings

| ID | 嚴重度 | Finding | 修復 |
|---|---|---|---|
| R-01 | P1 | 上游 `CLAUDE.md` 是 git symlink。Windows `core.symlinks=false` 時，`git add` 把檔案正文寫進 symlink target；GitHub Windows runner 回 `unable to create symlink CLAUDE.md: Filename too long`，整個 job 停在 checkout。 | 改存 mode `100644` 一般檔。`tests/test_docs.py::test_tracked_files_are_not_git_symlinks` 掃描 `git ls-files -s`，禁止 `120000`。見 [`docs/DECISIONS.md`](docs/DECISIONS.md)。 |
| R-02 | P2 | `tools/check_links.py` 對相對路徑只做 `.exists()`，解析到 repo 根目錄以外的路徑不會被拒絕。 | `_missing_relative` 用 `resolved.is_relative_to(ROOT)`；失敗記「連結逃出 repo 根目錄」。`test_check_links_rejects_path_outside_repo` 鎖行為。 |
| R-03 | P3 | `AGENTS.md` 文件責任清單沒有 `REVIEW.md`。 | 補上「風險快照，不是 bug log」，並把本檔列入文件責任。 |
| R-04 | P3 | `.github/ISSUE_TEMPLATE/config.yml` 的 Contributing 連結仍指向上游，GitHub 訪客會以為本線收產品 skill。 | 貢獻連結改為本 fork [`CONTRIBUTING.md`](CONTRIBUTING.md)；另留上游產品貢獻連結。skill request 與產品 skill PR 模板標明不要開到這個 fork。`test_issue_contact_links_point_at_this_fork` 鎖行為。 |
| R-06 | P3 | 上游 `.github/workflows/validate-skill.yml` 使用 `ubuntu-slim`，且沒有本 fork 的 repo 閘門。 | 加上 `github.repository == 'coreyhaines31/marketingskills'`。本線 skill 驗證仍只走 `tools/validate_skills.py`。`test_upstream_workflows_have_repo_guard` 掃全部非 fork 自有 workflow。 |

## 刻意不修

| ID | 嚴重度 | Finding | 理由 |
|---|---|---|---|
| R-05 | P3 | `.claude-plugin/plugin.json` 的 `homepage`／`repository` 仍是 `coreyhaines31/marketingskills`。 | 產品 plugin 清單。改掛 `SanHsien/agent-marketing-skills` 會把 fork 包裝成第二個官方 marketplace，違反 overlay。 |
| R-07 | P3 | `.github/FUNDING.yml` 仍是 Corey 的贊助帳號。 | 不把贊助改掛到 fork 維護者。贊助入口留在上游；本線 README 也不轉載贊助 CTA。 |

## 本輪實證

### 本機（修完後）

```text
pwsh -NoProfile -File tools\dev_check.ps1
→ compileall / ruff E9+F / pytest / validate_skills / node --check / check_links 全綠
→ 35 passed
→ 50 skills 通過；warnings 0
→ 64 支 CLI `node --check`
→ 21 份維護文件（含 REVIEW.md），0 斷連結
→ git ls-files -s CLAUDE.md → 100644（不再是 120000）
```

### GitHub Actions（overlay 首推 `ff62783`，修 finding 前）

| Workflow | 結果 | 說明 |
|---|---|---|
| [CI](https://github.com/SanHsien/agent-marketing-skills/actions/runs/33086866547) | failure | Ubuntu py3.9–3.14 全綠。Windows `test (windows / py3.14)` 在 [checkout](https://github.com/SanHsien/agent-marketing-skills/actions/runs/33086866547/job/98568765997) 失敗：`Filename too long`（R-01）。 |
| [CodeQL](https://github.com/SanHsien/agent-marketing-skills/actions/workflows/codeql.yml) | success | JavaScript/TypeScript 與 Python `security-extended` |
| [Upstream check](https://github.com/SanHsien/agent-marketing-skills/actions/workflows/upstream-check.yml) | success | |
| [Dependency freshness](https://github.com/SanHsien/agent-marketing-skills/actions/workflows/dependency-freshness.yml) | success | |

### GitHub Actions（本輪 `88fbe4e`，修完後）

| Workflow | 結果 | 說明 |
|---|---|---|
| [CI](https://github.com/SanHsien/agent-marketing-skills/actions/runs/33088005679) | success | Ubuntu py3.9–3.14 與 Windows `test (windows / py3.14)` 全綠。 |

## 已檢查、不列為 finding

- 產品現況：50 個 `skills/*/` 目錄、64 支 `tools/clis/*.js`；frontmatter 驗證通過。
- Fork overlay Python（`tools/check_*.py`、`tools/validate_skills.py`）無 `os.system`、`shell=True`、`eval(`、`exec(`、`pickle`。`check_upstream_updates.py` 以 argv 列表呼叫 `git`。
- CLI 憑證只讀 `process.env.*`，倉庫沒有提交 `.env`（`git ls-files` 為 0）。
- `sync-skills.yml`、`release.yml` 與 `validate-skill.yml` 仍有 `github.repository == 'coreyhaines31/marketingskills'`。
- 公開入口只留繁中／英文；README 保留來源與 MIT credit，不轉載作者宣傳與贊助 CTA。
- CodeQL / CI checkout 已 pin SHA，且 `persist-credentials: false`。
- `gh repo set-default --view` 為 `SanHsien/agent-marketing-skills`。不對上游開 PR、不 push `upstream`。
- Dependabot 不自動合併，合理。

## 尚未宣稱範圍

- **沒有**用真實客戶落地頁、廣告帳號或 API key 跑任何產品 CLI。
- **沒有**在 Claude Code / Codex / Cursor 實際安裝並觸發全部 50 個 skill。
- **沒有**對 `tools/integrations/` 做 HTTP 探活。
- `dev_check.ps1` **不含** Bandit；CodeQL 是獨立 workflow。
- **不宣稱**本 fork 有自己的 GitHub Release；產品版本仍跟隨上游 `.claude-plugin/plugin.json`（目前 `2.11.0`）。
- **不宣稱**上游 `validate-skill.yml`（`ubuntu-slim` + 第三方 action）已在本 fork 跑過；本線只閘住它，驗證走 `validate_skills.py`。
