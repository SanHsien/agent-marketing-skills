# 開發環境

維護者與 AI 接手用的開發文件。產品使用方式在 [`README.md`](../README.md)；上游同步在 [`UPSTREAM.md`](UPSTREAM.md)；決策在 [`DECISIONS.md`](DECISIONS.md)。

## 架構

```text
skills/<name>/SKILL.md     產品 skill（英文，以上游為準）
        │
        ├── references/    按需載入的細節
        ├── evals/         上游評測樣本
        └── assets/        模板／靜態檔
        │
        ▼
 安裝到 ~/.agents/skills、~/.claude/skills 或 ~/.cursor/skills 後才真正可被呼叫

tools/clis/*.js            上游零依賴 Node CLI（Node 18+）
tools/integrations/        上游工具整合指南
.claude-plugin/            Claude Code marketplace
```

`skills/`、`tools/clis/`、`tools/integrations/`、`.claude-plugin/` 是要安裝或跟隨上游的產品。其餘檔案是本 fork 的開發與治理骨架，不要一起複製進 skills 目錄。

## 本機開發（Windows）

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements-dev.txt
.venv\Scripts\python -m pip install -r requirements-security.txt
$env:PYTHONUTF8 = "1"
pwsh -NoProfile -File tools\dev_check.ps1
```

先決條件：Python 3.13、Node.js 18+、PowerShell 7。一般測試另在 Ubuntu
覆蓋 Python 3.9–3.14；Windows canonical security gate 固定 Python 3.13，因目前
`yara-python` 尚無 Python 3.14 的 Windows wheel。

只驗證產品入口是否齊全時，確認：

- `skills/cro/SKILL.md`
- `skills/copywriting/SKILL.md`
- `skills/product-marketing/SKILL.md`
- `tools/REGISTRY.md`
- `.claude-plugin/marketplace.json`

不要對真實廣告帳號或客戶網站跑完整行銷作業來當 CI。gate 驗的是規格、語法與維護腳本。

## Canonical gate

`tools\dev_check.ps1` 會依序：

1. `python -m compileall`（`tests` 與 `tools` 底下的 `.py`）
2. `ruff check`（E9 + F）
3. `pytest tests/ -q`
4. `python tools/validate_skills.py`
5. `node --check`（`tools/clis/*.js`）
6. `python tools/check_links.py`
7. 以 `requirements-security.txt` 釘定的 SkillSpector 完整掃描 50 個產品 skill

掃描預設每個靜態分析 300 秒、每個 skill workflow 900 秒；這是大型 reference
skill 在 Windows runner 上完成 bytecode/supply-chain accounting 所需的可重現預算，
不是忽略 timeout。超時仍是 incomplete 並讓 gate 失敗。

完整性 checker 另核對釘定版本的 exact 24-analyzer set 與 100% 元件覆蓋。唯一可接受的
頂層 `partial` 是 nonfatal `reference_unresolved`，且 ledger 與 reference source-line
key set 必須完全對應；更新 SkillSpector pin 時須重新審查並同步 expected analyzer set。

CI 在 Ubuntu 跑 3.9–3.14，並加一個 Windows Python 3.13 job 跑完整 canonical gate。推 `main` 前先跑本機 gate。

## 工具設定

`pyproject.toml` **只放工具設定**，沒有 `[project]` 與 `[build-system]`：本 repo 交付的是 Markdown Agent Skills，不是 Python 套件。改 `ci.yml` 的 ruff 旗標時要同步改 `pyproject.toml`，`tests/test_docs.py::test_tool_config_matches_ci_flags` 會擋住漂移。`.python-version` 釘 3.13，讓 fresh clone 預設可重現 Windows canonical gate；若既有 `.venv` 使用其他支援版本，可用 `-SkillSpectorPython <Python 3.13 路徑>` 指定安全掃描環境。

`.gitattributes` 把行尾釘成 LF。沒有它，全域 `core.autocrlf=true` 會讓工作區變 CRLF，於是 `git status` 顯示檔案 modified 但 `git diff` 是空的。

## 依賴新鮮度

`tools/check_dependency_freshness.py` 把 `requirements-dev.txt` 宣告的每一筆直接依賴拿去對 PyPI 現行版本，`.github/workflows/dependency-freshness.yml` 每月跑一次。紅燈只有兩條誠實出口：`# freshness-hold:`（常態政策）或 `.github/dependency-deferrals.json` 的 `deferredLatest`（會過期）。調高宣告下限來讓報告變綠不是出口。

## 不要做的事

- 不要把產品 `SKILL.md` 改寫成維護索引。
- 不要翻譯 `skills/`。
- 不要在本 fork 啟用 `sync-skills.yml`（它會覆寫繁中 README）或自動發 GitHub Release。
- 不要提交 `.env`、API key 或客戶文案。
- 測試必須是靜態規格檢查，不能打真實第三方行銷 API。
