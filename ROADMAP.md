# 路線圖

> 本 repo 後續工作的單一真相源。做完一項，就在同一個 commit 刪掉那一列；新工作只加在這裡。
> 現況段的數字是 2026-10-29 依 `main` `67905a4dc762` 查的快照，開工前先重查 GitHub。

## 現況

本 repo 是行銷 Agent Skills 與零依賴 Node.js CLI 的 Windows 維護線，CLI 契約測試模擬網路，不以真實 API 作 CI（`AGENTS.md`〈專案定位〉、〈技術與資料流〉）。2026-10-29 快照 open PR、安全告警均為 0，CI、CodeQL、Dependency freshness、Upstream check 最近結果為 success；Regression Tests、Release、Sync Skills 與 Validate Agent Skill 因上游 repo 閘門 skipped，issue 因停用而未查到（2026-10-29 `gh` 查詢，`67905a4dc762`）。產品技能清單目前收錄 52 個，中英入口改以清單導向呈現，實際宿主觸發與真實 API 使用不在既有驗收範圍（深掃上游審查報告，2026-10-28；`README.md`、`README.en.md`；`REVIEW.md:83-90`）。

## 近期：可以直接動手

| 項目 | 為什麼 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
| 補一個宿主的最小技能使用驗收 | 靜態驗證與 CLI mock 測試不能證明技能安裝後真的被觸發 | 維護者選定一個宿主，用一份去識別產品背景走 `product-marketing` 與一個相關 skill；記錄實際讀取、輸出與 SHA，不觸發廣告、郵件或付費 API | 維護者 | `REVIEW.md:83-90`；`README.md`〈Skills 怎麼一起運作〉；`AGENTS.md` 的資料邊界 |

## 中期：等條件成立再做

| 項目 | 觸發條件 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
| 增量審查上游與既有工具指南 | 超過 baseline 水位、已審 PR head 改變，或上游 #904 合併 | 逐檔分類並保留 fork 遮蔽、Windows gate 與 workflow 閘門；記錄採用／略過；`pwsh -NoProfile -File tools/dev_check.ps1` 含 Node 契約與掃描通過才更新水位 | Codex | `tools/upstream_baseline.json`；`docs/DECISIONS.md:421-453`；上游 #904 |
| 擴充敏感輸出遮蔽契約 | 實際回應帶有未涵蓋的敏感鍵，或需要處理物件鍵名內的秘密 | 先用假秘密重現，定義敏感鍵與值的遮蔽範圍；重疊值、巢狀資料、錯誤訊息與輸出測試通過，合法非敏感值不被誤遮 | Claude Opus | 深掃報告（2026-10-26）〈刻意不修〉；`tools/clis/_safe-output.js:1-32`；`18c2b89` |
| 單一產品 CLI 的唯讀真實服務驗收 | 維護者有具體工具需求並授權帳號讀取 | 先讀對應指南與最小查詢範圍，只呼叫一次必要唯讀端點；確認欄位、錯誤碼與輸出遮蔽；不記錄憑證，不衍生廣告／郵件寫入 | 維護者 | `REVIEW.md:85-87`；`tools/clis/README.md`；`AGENTS.md` 的客戶與帳號資料限制 |

## 刻意不做

| 不做什麼 | 理由 | 什麼情況下重新考慮 |
| --- | --- | --- |
| 啟用本 fork 的上游發布、同步與打包 workflows | skipped 是既定 repo 閘門，不是檢查壞掉；見 `AGENTS.md`〈硬性邊界〉與 `FORK.md` | 維護者決定建立自己的發布線，先定義產物、權限與驗收 |
| 轉載新增廠商導流卡片或 REGISTRY 夥伴列 | 政策性不引用，不是等候採用；理由見 `docs/DECISIONS.md:405-419,449-453` | 維護者明確改變廠商內容政策；上游合併本身不構成條件 |
| 為轉綠廣泛放寬 SkillSpector、或把產品全文翻成繁體 | 精準 finding／partial 例外綁內容，產品語言跟隨上游；見 `docs/DECISIONS.md:393-403,437-443`、`AGENTS.md` | 有可重現掃描誤判時只重審該項；產品語言需求另由維護者決定 |

## 維護方式

每週按 baseline 與已審 head 增量審查；沒有共同祖先沿用既有三方套用方法，不改寫歷史，水位代表已審而非全數合併。
每月查 Dependency freshness、`gh pr list --repo SanHsien/agent-marketing-skills` 與安全告警；修改 CLI 跑相關 mock 契約，掃描指紋變動逐筆重審；其他文件只連結本路線圖。
