[English](CHANGELOG.en.md) | 中文版

# 變更紀錄

格式參考 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.1.0/)，新的在上面。
本檔只記錄**本 fork 的維護歷史**（2026-08-27 起）；上游
[`coreyhaines31/marketingskills`](https://github.com/coreyhaines31/marketingskills)
的產品演進見其自身歷史與 [`docs/UPSTREAM.md`](docs/UPSTREAM.md) 的審查清冊。
逐筆採用／略過的理由記在 [`docs/DECISIONS.md`](docs/DECISIONS.md)。

---

## 2026-09-11（批次審查）

### 同步

- **ai-seo 2.5.0（上游 commit `5b2c000`，cherry-pick）。** ChatGPT 5.6 後 listicle／comparison
  引用率下滑的 format-volatility 指引與新 reference，純產品內容與版本號更新，無 fork 檔案衝突。

### 略過

- **Converly 二次上架（`d4ff28a`）與 Ploy 上架三部曲（`4fbe11f`／`88de9fd`／`5cd4a7e`）。**
  上游付款清償後恢復贊助商揭露，但那是上游與廠商的商業關係，不是本 fork 的；維持既有的贊助商
  CTA 略過政策。7 個仍是 open 的上游 PR（#572、#573、#575、#580、#581、#582、#583）暫緩到合併
  後再審。理由見 [`docs/DECISIONS.md`](docs/DECISIONS.md)。

## 2026-09-11

### 變更

- **SkillSpector pin 前進到 2.11.2（`75bd6f3`）。** 精確 fingerprint 依設計綁定掃描器版本，升版後全數重產：40 筆換雜湊、理由逐字保留，5 筆在 2.11.2 下已不再產生的移除。以與 CI 位元組相同的 LF 暫存驗證，50 個 skill 全數通過，突變測試仍會擋下。細節見 [`docs/DECISIONS.md`](docs/DECISIONS.md)。

### 修復

- **本機 gate 在 CRLF checkout 上永遠假紅。** 早於 `.gitattributes` 的 checkout 把文字檔留成 CRLF，而精確 fingerprint 雜湊檔案內容，所以 baseline 裡的 finding 在本機全被報成新的。自我掃描改掃 `tools/stage_scan_input.py` 產生的暫存：取 git 看得到的檔案（已追蹤加尚未提交、不含 gitignore），index 為 LF 的文字檔還原成 LF，binary、`eol=crlf` 與未追蹤檔逐位元組複製。在 466 個 CRLF 檔的本機 checkout 上 50 個 skill 全數通過。

## 2026-08-27（覆核）

### 修復

- **Windows CI checkout。** 上游 `CLAUDE.md` 是 git symlink；在 `core.symlinks=false` 的 Windows 上被存成「以檔案正文為 target」的 `120000` blob，runner 回 `Filename too long`。改存一般檔，並加測試擋住再出現 symlink。
- **相對連結逃出工作樹。** `check_links.py` 現在拒絕解析到 repo 根目錄以外的路徑。
- **Issue／PR 導流。** `ISSUE_TEMPLATE/config.yml` 改連本 fork 的 `CONTRIBUTING.md`，並保留上游產品貢獻連結。skill request 與產品 skill PR 模板標明不要開到這個 fork。
- **上游 validate-skill workflow。** `validate-skill.yml` 加上與 `sync-skills.yml`／`release.yml` 相同的官方 repo 閘門。

### 新增

- **`REVIEW.md`。** 第一次專案覆核快照。

## 2026-08-27

### 新增

- **`fork` Windows-first 維護骨架。** `AGENTS.md`、`CLAUDE.md`、`FORK.md`、`NOTICE.md`、
  `CONTRIBUTING.md`、`SECURITY.md`、`CODE_OF_CONDUCT.md`、`docs/`、`tools/` 維護腳本、
  `tests/`、`.github/` 的 CI／CodeQL／Dependabot／上游檢查／相依新鮮度。
  CI 跑 Ubuntu 3.9–3.14 與 Windows 3.14：pytest、ruff（E9+F）、`validate_skills.py`、
  `node --check`、相對連結檢查。
- **公開入口只留繁中與英文。** `README.md` 改繁中主檔、`README.en.md` 為英文鏡像。
  來源與授權 credit 保留，作者宣傳與贊助 CTA 不轉載。

### 變更

- `sync-skills.yml` 與 `release.yml` 加上只在上游官方 repo 執行的閘門，避免覆寫繁中 README
  或在本 fork 自動發產品 release。
