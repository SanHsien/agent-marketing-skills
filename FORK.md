# Fork 維護說明

本 repo fork 自 [`coreyhaines31/marketingskills`](https://github.com/coreyhaines31/marketingskills)，
沿用 MIT License 與完整 Git 歷史。

## 為什麼維護 fork

- 保留原作者持續更新的行銷 Agent Skills（CRO、文案、SEO、分析、增長）。
- 採 Windows-first 維護：Windows 11 + PowerShell 是主要開發、除錯與完整驗收環境。
- 公開入口改以繁體中文為主，英文鏡像放 `README.en.md`。
- 建立可重現的 Windows 開發 gate、Windows CI job，以及逐筆審查的上游追蹤。
- 產品 Skills 仍可直接安裝到 `.agents/skills/`、`~/.claude/skills/` 或 `~/.cursor/skills/`。

**回貢判準：修的是上游的 bug 就送回去；這裡獨創的文件／Windows 維護骨架留在這裡。**

## 與上游的差異

| 項目 | 說明 |
|---|---|
| `README.md` | 繁中主檔；英文鏡像在 `README.en.md` |
| `AGENTS.md` / `CLAUDE.md` | 本 fork 的 AI 維護單一真相源 |
| `NOTICE.md` / `FORK.md` | 來源、授權與同步說明 |
| `tools/dev_check.ps1` | Windows 本機一鍵 gate |
| `tools/validate_skills.py` | 產品 skill frontmatter 驗證（Windows 可跑，不依賴 bash） |
| `.github/workflows/ci.yml` | Ubuntu 3.9–3.14 + Windows Python 3.13：pytest / ruff / skill 驗證 / CLI 語法 / 連結 / SkillSpector 安全掃描 |
| `.github/workflows/upstream-check.yml` | 每週對 `upstream/main` 做未審查 commit 檢查 |
| `sync-skills.yml` / `release.yml` / `validate-skill.yml` | 加上只在官方 `coreyhaines31/marketingskills` 執行的 guard |
| `docs/DECISIONS.md`、`docs/UPSTREAM.md`、`docs/DEVELOPMENT.md` | fork 維護文件 |
| `REVIEW.md` | 風險快照，不是每個一般 bug 的流水帳 |

產品 `skills/`、`tools/clis/`、`tools/integrations/`、`.claude-plugin/` 以上游為準，除非有已記錄的 fork 修正。

## 分支與 remote

- `origin/main`：SanHsien 維護線，也是唯一長期分支。
- 日常修改直接推 `origin/main`。只有需要他人審查或高風險改動時才開 branch → PR。
- `upstream/main`：Corey Haines 原始專案，只追蹤、不推送。
- Dependabot 或外部 fork 的變更同樣走 PR，讀 diff 並通過 CI 後再合併。

不要 `git push upstream`。同步方式見 [`docs/UPSTREAM.md`](docs/UPSTREAM.md)。

上游更新英文 `README.md` 時，把新產品說明翻進本 fork 的繁中 `README.md`，並同步 `README.en.md`。作者宣傳、贊助 CTA 與個人事業連結略過。

## 換一台電腦怎麼開發

```powershell
git clone https://github.com/SanHsien/agent-marketing-skills.git
cd agent-marketing-skills
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements-dev.txt
.venv\Scripts\python -m pip install -r requirements-security.txt
pwsh -NoProfile -File tools\dev_check.ps1
```

只想安裝 Skills、不開發時：把 `skills/` 底下各目錄複製到宿主的 skills 目錄，或用：

```powershell
npx skills add SanHsien/agent-marketing-skills
```
