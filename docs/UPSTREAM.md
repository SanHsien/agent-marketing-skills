# 上游維護

## Remote

- Fork：`origin` → `https://github.com/SanHsien/agent-marketing-skills.git`
- 原作者：`upstream` → `https://github.com/coreyhaines31/marketingskills.git`
- 追蹤分支：`main`

## 檢查新提交

```powershell
git fetch upstream main
python tools\check_upstream_updates.py --strict
```

工具以 `tools/upstream_baseline.json` 的 `reviewed_through` 為起點，列出所有未審查提交。
有新提交或檢查失敗時，`--strict` 回傳非零；排程 workflow 也會因此明確失敗。

## 審查清冊

每次只做一次批次審查：

1. 讀 commit 主旨與變更檔案（open PR 必須讀 diff，禁止只憑標題結案）。
2. 判斷是否與繁中 README、Windows gate 或測試衝突。
3. 可直接同步的提交用 merge；只需要部分修正時 cherry-pick 或最小重做。
4. 跑 `pwsh -NoProfile -File tools\dev_check.ps1`。
5. 在 `docs/DECISIONS.md` 記錄採用／略過理由（須引用具體檔案與衝突點）。
6. 驗證完成後才把 baseline 推進到已審查的完整 40 字元 SHA。

Baseline 代表「已審查」，不代表「全部已合併」。

README 衝突的解法：上游新英文產品說明翻進 `README.md`，並同步 `README.en.md`。作者宣傳、贊助 CTA、個人事業連結略過。技能目錄表可同步。來源與授權 credit 留在 README 與 `NOTICE.md`。

`sync-skills.yml`、`release.yml` 與 `validate-skill.yml` 已加上 `github.repository == 'coreyhaines31/marketingskills'`。merge 上游時若這三支 workflow 被重寫，必須把閘門加回去。本 fork 的 skill 驗證走 `tools/validate_skills.py`（在 `ci.yml` / `dev_check.ps1`）。

## 2026-08-27：fork 起點

本 fork 自上游 `main` `b1aaa3619e747f4a836c61e03084c4a531de1262`
（`Merge pull request #569 from coreyhaines31/docs/partner-program-rules`）建立。此 SHA 設為第一個 `reviewed_through`。
之後的上游 commit 才需要進入審查清冊。

水位：

- PR：已看到 **#569**（`reviewed_pr_through`）
- issue：編號與 PR 共用，水位同為 **569**（`reviewed_issue_through`）
- commit baseline：`b1aaa36`（完整 SHA 見 `tools/upstream_baseline.json`）
- 下次只看編號更大的，或已評估項目是否出現新 commit／新 head

## 2026-09-11：批次審查（commit 水位推進到 `5b2c000`）

- PR：已看到 **#583**（`reviewed_pr_through`）
- issue：維持 **569**（`--strict` 實查無新項目）
- commit baseline：`5b2c000`（完整 SHA 見 `tools/upstream_baseline.json`）
- 採用：`5b2c000`（ai-seo 2.5.0，cherry-pick）
- 略過：`d4ff28a`（Converly 二次上架）、`4fbe11f`／`88de9fd`／`5cd4a7e`（Ploy 上架三部曲）——
  贊助商 CTA，維持既有政策
- 暫緩（open PR，未合併）：#572、#573、#575、#580、#581、#582、#583
- 理由見 `docs/DECISIONS.md` 2026-09-11 條目

## 2026-09-15：PR #586–#588 判讀

- PR：已看到 **#588**（`reviewed_pr_through`）
- commit 與 issue 水位不動（`--strict` 實查皆無新項目）
- 不引用：#586 Glasser 整合指南、#587 AIPM registry 徽章——第三方廠商導流，維持既有政策
- 暫緩至合併：#588 CLI 目錄補完（純文件對齊，非本 fork 可證缺陷）
- 理由見 `docs/DECISIONS.md` 2026-09-15 條目
