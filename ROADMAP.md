# 路線圖

> 本 repo 後續工作的單一真相源。做完一項，就在同一個 commit 刪掉那一列；新工作只加在這裡。
> 本輪現況更新於 2026-11-25，起始 HEAD `5837ec006fa3b5041a606fa08a29b68c55fb5d9b`；上游審查至 `8fd2fcade2fd6629026e9dfe6d133b55b36968b9`。下文 GitHub CI／告警數字仍是標明日期的歷史快照。

## 現況

2026-11-25：已完成 236 個 commit、63 筆 PR、40 筆 issue、59 個分支的決策清冊；本地 Python 3.13／SkillSpector 釘版環境已恢復，採用 22 組 CLI 修正、驗證工具與 Livestorm 名稱修正，產品 skill 與 2.14.28 版本同步依條件暫緩。完整 Windows gate exit 0（53 skill 安全掃描無新增 finding），已審 baseline 推至上述 SHA、PR #1061、issue #1057，並保存 59 個分支 head、25 個 open PR 監看。逐項來源、理由與前後測試見 `docs/DECISIONS.md` 同日條目。本輪只提交目前分支，不推送。

本 repo 是行銷 Agent Skills 與零依賴 Node.js CLI 的 Windows 維護線，CLI 契約測試模擬網路，不以真實 API 作 CI（`AGENTS.md`〈專案定位〉、〈技術與資料流〉）。2026-10-29 快照 open PR、安全告警均為 0，CI、CodeQL、Dependency freshness、Upstream check 最近結果為 success；Regression Tests、Release、Sync Skills 與 Validate Agent Skill 因上游 repo 閘門 skipped，issue 因停用而未查到（2026-10-29 `gh` 查詢，`67905a4dc762`）。產品技能清單目前收錄 53 個，中英入口改以清單導向呈現，宿主觸發只驗過 Claude Code 的 `product-marketing` 與 `copywriting` 兩個 skill（2026-11-08，`docs/host-acceptance/2026-11-08-claude-code.md`）；其餘 skill、其他宿主與真實 API 使用不在既有驗收範圍（深掃上游審查報告，2026-10-28；`README.md`、`README.en.md`；`REVIEW.md:83-90`）。

## 近期：可以直接動手

| 項目 | 為什麼 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
| 依逐項條件接續產品 skill 與工具表同步 | 2026-11-25 已審但未採的 P/F/V 項目，含 #961 的安裝誤判、#1017 的 #948 修正與 #1049 的工具說明；產品仍是原版，不是上游 closed 就算本線已修 | 以目前 fork 的舊內容重現各情境失敗；核對當日官方事實、REGISTRY 連結與夥伴略過政策；套用後重審變動 skill 的精準 finding／partial 雜湊，完整 Windows gate exit 0 才更新產品版本 | Codex | `docs/DECISIONS.md` 2026-11-25 的 P/F/V 與逐項清冊 |
| 上游未合併修正的增量追蹤 | 已審 open PR 的 head／state 改變或合併，尤其 #1031 金額解析、#1032 exa false flags；不因 PR 水位已到 #1061 就漏看 | 檢查器以 monitored 回報變動；只重看變動 diff，採用前跑該項無網路前後測試，不重複審查整批 236 commits | Codex | `tools/upstream_baseline.json` 的 monitored；`docs/DECISIONS.md` 同日條目 |

## 中期：等條件成立再做

| 項目 | 觸發條件 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
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
