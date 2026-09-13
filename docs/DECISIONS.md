# 維護決策

## 2026-08-27：建立 Windows-first 維護型 fork

**決定**：fork `coreyhaines31/marketingskills`，保留 MIT 與完整歷史，預設分支維持 `main` 以降低與上游同步摩擦。本線聚焦繁中公開入口、Windows 開發 gate、Windows CI，以及逐筆審查的上游追蹤。

**理由**：上游已有 50 個可安裝的行銷 Agent Skills 與零依賴 Node CLI，符合維護者讓 AI 助手處理轉化、文案、SEO 與增長的需求。缺的是 Windows 11 上可重現的開發／驗收骨架，以及繁中入口。直接用上游 repo 難以長期記錄 fork 取捨。授權是 MIT，fork 修改同樣走 MIT。

**限制**：

- 不把 fork 包裝成原創專案，不移除原作者與 MIT 標示。
- `skills/*/SKILL.md` 保持產品規格，不用維護索引覆寫。
- 不把產品 skill 翻譯成繁體；產品語言跟隨上游。
- 上游更新必須逐筆審查。
- 不回貢，除非維護者在當次對話明確同意。

## 2026-08-27：維護線直接推 main

**決定**：fork 維護不再開功能分支。改完在本機跑 gate，通過後直接推 `origin/main`。遠端只留 `main`；`upstream/main` 只追蹤。

**理由**：這是單人維護 fork，分支與 PR 沒有第二審查者，只增加同步成本。

**限制**：

- Dependabot 與外部 fork 仍可能開 PR，讀 diff 後再合併，不自動合併。
- 不推 `upstream`，不 force-push `main`。
- 不刪 `upstream` remote。

## 2026-08-27：不啟用 Dependabot 自動合併

**決定**：Dependabot 只開 PR；CI 與人工讀 diff 通過後才合併。

**理由**：開發依賴只有 pytest / ruff，體積小，但自動合併仍會跳過「讀 diff」這一步。

## 2026-08-27：閘住上游的自動同步與自動發版

**決定**：`.github/workflows/sync-skills.yml` 與 `.github/workflows/release.yml` 加上 `if: github.repository == 'coreyhaines31/marketingskills'`。本 fork 不讓 Coreybot 覆寫繁中 README，也不在版本號變動時自動發 GitHub Release。

**理由**：`sync-skills.yml` 會把技能表寫回 `README.md`，與本 fork 的繁中公開入口衝突。`release.yml` 在 `plugin.json` 版本變動時發 release，本線不代發上游產品版本。

**限制**：上游若重寫這兩支 workflow，merge 時要保留閘門。

## 2026-08-27：閘住上游 validate-skill.yml

**決定**：`.github/workflows/validate-skill.yml` 加上 `if: github.repository == 'coreyhaines31/marketingskills'`。本 fork 的 skill 驗證只走 `tools/validate_skills.py`。

**理由**：該 workflow 用 `ubuntu-slim` 與第三方 `Flash-Brew-Digital/validate-skill@v1`，且沒有 repo 閘門。有人改 `SKILL.md` 時會在本 fork 跑。本線不改寫產品 skill，也不把第三方 action 當 CI 契約。

**限制**：merge 上游時若這支 workflow 被重寫，必須把閘門加回去。

## 2026-08-27：GitHub 貢獻入口改指本 fork，產品 skill 仍導向上游

**決定**：`ISSUE_TEMPLATE/config.yml` 的貢獻連結改為本 fork 的 `CONTRIBUTING.md`，另留一條上游產品貢獻連結。skill request 與產品 skill PR 模板加上「不要開到這個 fork」的說明。

**理由**：訪客在 GitHub 點 Contributing 會進到上游英文指南，誤以為本線收產品 skill PR。本 fork 的貢獻契約已經寫在 `CONTRIBUTING.md`。

**限制**：不改 `.claude-plugin/plugin.json` 的 homepage／repository，不把 `FUNDING.yml` 改掛到維護者。

## 2026-08-27：公開文件只留繁中與英文；README 只留 credit

**決定**：GitHub About 與公開入口只用繁體中文與英文。README 不轉載作者個人頁、機構、課程、贊助 CTA 或官網行銷。來源與授權 credit 留在 README 短段與 `NOTICE.md`。

**理由**：這是維護型 fork，不是原作者的宣傳頁。相關 credit 放 README 短段與 `NOTICE.md` 即可滿足 MIT 標示。

**限制**：上游若把宣傳段落一併推進來，merge 後刪掉／不要合進公開入口。技能目錄表與工具登錄連結可同步。

## 2026-08-27：CLAUDE.md 改存一般檔，不跟上游 symlink

**決定**：本 fork 的 `CLAUDE.md` 以一般檔（mode `100644`）存放 fork 薄入口，不保留上游「symlink → AGENTS.md」。

**理由**：上游 `CLAUDE.md` 是 git symlink。Windows 上 `core.symlinks=false` 時，`git add` 會把檔案正文寫進 symlink blob；GitHub Windows runner checkout 就變成 `unable to create symlink CLAUDE.md: Filename too long`，整個 Windows job 在 checkout 失敗。Ubuntu 不受影響，所以 overlay 推送後只紅 Windows。

**限制**：同步上游時若 `CLAUDE.md` 又變回 symlink，必須再改成一般檔。`tests/test_docs.py::test_tracked_files_are_not_git_symlinks` 會擋住。

## 2026-08-29：上游檢查補上 PR 與 issue 兩個面向

**決定**：`check_upstream_updates.py` 補上以 `--state all` 收集上游 PR／issue 的邏輯，
`upstream-check.yml` 補 `GH_TOKEN: ${{ github.token }}`，新增 `tests/test_upstream_updates.py`。
Baseline 既有的水位不動。

**理由**：`docs/UPSTREAM.md` 早就寫著「四個面向都要看」，`upstream_baseline.json` 也記著
`reviewed_pr_through` 與 `reviewed_issue_through`——但**沒有任何程式讀那兩個欄位**，檢查器只比對
commit 水位。那兩個面向不是「查過沒發現」，是根本沒查，而每週的排程報告長得跟查過一樣綠。
這是艦隊層級的問題：24 個 fork 裡 21 個都這樣（`SanHsien/repo-fleet-ops` 的 `docs/INCIDENTS.md`
第十條）。參考實作是 `SanHsien/harness-guard`。

三個性質，缺一不可：

- **`--state all`**：只查 `open` 看不到「開了又關、沒有合併」的 PR，而那正是「上游拒收、但可能對
  本 fork 有價值」的一類——已合併的遲早會經由 commit 抵達，被關掉的永遠不會。
- **`gh` 失敗時回 `None` 不回 `[]`**，報告寫 `Not checked` 並 **fail closed**（exit 2）。
  「沒查到」和「沒有」在綠色報告裡長得一樣，只有一個是真的。
- **`GH_TOKEN`**：`gh` 在 Actions 裡沒有憑證就列舉不到，配上 fail closed 會讓紅燈的意思變成
  「檢查器壞了」而不是「上游有東西」。

**證據**：落地後實跑 `python tools/check_upstream_updates.py`，三個面向都印出水位與待辦數；
本 repo 的 gate 全綠。

**已知代價**：水位以上真的有東西時，每週的 upstream-check 會回 exit 1。那是它該做的事——先前的
綠燈不是「沒有待辦」，是沒有人看。

**觸發條件**：報告列出項目時逐筆讀 diff、把採用／略過理由寫進本檔，然後才推進 baseline 的水位。


## 2026-08-30：上游 #571 採用（下架未付款夥伴），#570 不引用

commit 水位 `b1aaa36` → `e55de88`；PR 水位 569 → 571；issue 水位維持 569（實查為空）。

### 採用：Converly 下架（上游 PR #571 / commit `e55de88`）

**上游做了什麼**：把 Verified Partner「Converly」設為 `active: false` 並刪掉
`tools/integrations/converly.md`，理由寫在標題裡——**付款未清**。

**為什麼本 fork 也要跟**：本 fork 的 `tools/REGISTRY.md` 原本把 Converly 列在
**Verified Partners** 表，附註「Converly sponsors Marketing Skills」，`Tool Index` 也有一列
指向 `integrations/converly.md`。**本 fork 與 Converly 沒有任何商業關係**，卻在替一個連上游
都因未付款而下架的廠商掛保證。這不是產品偏好問題，是掛了一個沒有依據的背書。

**落地方式**：改 `partners.json` 的 `active: false`、刪 `tools/integrations/converly.md`，
再跑本 repo 自己的 `node scripts/sync-partners.mjs` 重新產生區塊（0 partners）。
`Tool Index` 那一列是 sync 腳本不管的手寫表，另外手動移除——不移的話它會指向剛被刪掉的檔案，
`tools/check_links.py` 會紅。

**與上游的差異**：上游的 README 有 `<!-- PARTNERS:START -->` 區塊要一起改，**本 fork 沒有**
（fork 的 README 早就不轉載上游的贊助商推廣），所以 sync 腳本對 README 報
「missing markers」是預期結果，不是故障。上游同時加的 `.gitignore` `.partners-pending/`
是它的收款流程暫存目錄，本 fork 沒有那個流程，不引用。

**已知的上游不一致**：`partners.json` 保留 converly 條目（`_comment` 說停用要保留歷史），
但 `integration` 欄仍指向已刪除的 `tools/integrations/converly.md`。上游自己也是這個狀態。
條目 `active: false` 時不會被渲染，所以是惰性的，本 fork 維持與上游一致不另行分歧。
**觸發條件**：上游修正該欄位時跟著改。

### 不引用：PR #570「Claude/crypto trading prediction app」

OPEN，內容是往這個 repo 塞一整個加密貨幣交易預測 app（`crypto-trading-app/` 的
`index.html`、`src/App.tsx`、`src/api/binance.ts`、`package-lock.json` 等）。與這個 repo 的
主題（行銷技能庫）無關，上游也沒有合併。

**觸發條件**：上游合併它時再看——那時它就會經由 commit 軸抵達。

## 2026-09-06：安全掃描必須完整，並保留產品語意

**決定**：Windows canonical gate 使用釘定版 SkillSpector，任一適用 analyzer 為
degraded、partial、skipped、failed、unaccounted 或非預期 disabled 都失敗；fresh clone
預設 Python 3.13，因目前 `yara-python` 沒有 Python 3.14 的 Windows wheel。Ubuntu 的一般
測試矩陣仍涵蓋 Python 3.9–3.14。

**產品檔調整**：只做避免靜態解析器誤切語句的等義正規化：將不成對縮寫、部分 code span、
JavaScript template literal 與容易觸發無界迴圈規則的否定句改寫；ASO 評分表移除欄寬填充空白；
creative review 範例保留同一檢測結果，但不重複列出相同污染物名稱。操作步驟、停止條件與產品
能力沒有擴張。所有原先降級的 skill 都以 0 finding、0 limitation 重新掃描。

**baseline 原則**：只保留逐筆審查後的精確 fingerprint；可直接消除的誤判不加入 baseline。
變更產品文案時若 fingerprint 改變，必須重新審查，不可用寬鬆規則整批忽略。

**完整性契約**：gate 核對釘定 `--no-llm` revision 的 exact 24-analyzer set 與 100%
元件覆蓋，缺少或多出 analyzer、未解釋計數、limitation 都失敗。產品說明中的一般文字常被
reference resolver 當成 local path；僅允許 nonfatal `reference_unresolved` 保留頂層
`partial`，而且 ledger 與 `references` 的 source-line key set 必須完全一致。其他 exception
仍 fail closed。

**資源預算**：每個靜態分析預設 300 秒、每個 skill workflow 900 秒。`marketing-plan`
在 120 秒靜態預算下會把 supply-chain bytecode accounting 記為 runtime_limit；提高後的
focused scan 為 0 finding、0 limitation。timeout 仍回 exit 2，不視為通過。

**2026-09-07 pin 修正**：SkillSpector pin 從 `70cd263` 前進到 `185d610`，使 fresh runner
與本機驗證使用同一套可設定 static/workflow resource budget 的實作。先前本機 interpreter
實際由 editable source 載入新版，但 requirements 仍安裝舊 revision；版本字串同為 2.11.0，
不能當成相同 provenance。新 SHA 已確認在 `SanHsien/SkillSpector` 遠端 main，且其 CI、
CodeQL、Scorecard 全綠。

## 2026-09-11：SkillSpector pin 前進到 2.11.2，精確 fingerprint 重產

**決定**：`requirements-security.txt` 從 `185d610`（2.11.0）前進到 `75bd6f3`（`SanHsien/SkillSpector`
合併上游 2.11.2）。`.skillspector-baseline.yaml` 的 40 筆精確 fingerprint 換成新版雜湊、理由逐字保留；
5 筆在 2.11.2 下已不再產生 finding 的 fingerprint 移除；`scoped_rules` 不動。

**理由**：2.11.1／2.11.2 含安全分析修正（finding identity 保留分類與有界證據、隱藏指令偵測、
reference accounting 的 fatal 錯誤）。精確 fingerprint 依 `suppression.finding_fingerprint` 同時雜湊
掃描器版本、元件內容與 finding，所以**任何掃描器升版都會讓全部 fingerprint 失效**，即使 finding 本身
沒變。重產以「CI 等效位元組」為準：把文字檔依 `.gitattributes` 正規化回 index 的 LF 後放到暫存目錄。
在該暫存上，舊 pin 的 50 個 skill 全數 exit 0（證明暫存與 CI 等效）；2.11.2 則是 40 筆一對一漂移、
0 組新增、0 組部分減少，另有 4 組共 5 筆不再產生：`ad-creative` RP1
`references/generative-tools.md` ×2、`ads` MP3 `references/meta-decision-system.md`、
`marketing-loops` EA4 `evals/evals.json`、`revops` RA2 `references/automation-playbooks.md`。
刪掉這 5 筆不是放寬：精確 fingerprint 只對應完整內容雜湊，留著也壓不住別的東西，而它們若再出現，
gate 會紅。

**驗證**：以本 repo 的 `tools/run_skillspector.py`、gate 預設預算（靜態 300 秒、workflow 900 秒、
`PYTHONHASHSEED=0`）在暫存上重掃 50 個 skill 全數 exit 0；analyzer 集合在兩版都是同一組 24 個，
完整性契約不必改。突變：在 `ab-testing` 注入外傳 `os.environ` 並 `eval` 回應的腳本，exit 1。
`tests/test_docs.py` 的 pin 斷言跟著前進，而不是放寬。重產工具逐行保留理由、順序與 `scoped_rules`，
只換 `- hash:` 行與 `scanner_version:`，並刪除上述 5 個區塊。

**本機注意**：這份 checkout 的文字檔是 CRLF（早於 `.gitattributes`），index 與 CI 則是 LF；gate 直接
掃工作區，證據雜湊因此不同，本機會把 baseline 裡的 finding 報成新的——與掃描器版本無關。這是本機
假紅，不是 baseline 問題；要在本機得到與 CI 相同的結果，需以 LF 正規化後的內容掃描。

## 2026-09-11：本機自我掃描改掃 index 行尾的暫存

**決定**：`tools/dev_check.ps1` 的 SkillSpector 自我掃描不再直接掃 `skills/`，改掃
`tools/stage_scan_input.py` 在暫存目錄產生的副本；上一節「本機注意」描述的假紅由此解決。

**理由**：重新 checkout 或 `git add --renormalize` 也能消掉 CRLF，但它只修這台機器，下一個早於
`.gitattributes` 的 clone 又會紅，而且改工作區是破壞性操作。暫存讓 gate 的輸入跟 CI 一致，工作區不動。
範圍：`git ls-files --cached --others --exclude-standard -- skills`，也就是已追蹤加尚未提交、不含
gitignore 的檔案，所以新 skill 在提交前就會被掃到。只有 index 為 `i/lf` 且屬性沒要求 `eol=crlf`
的檔案才把 CRLF 換成 LF；binary、`eol=crlf` 與未追蹤檔逐位元組複製，不替尚未進 index 的檔案猜行尾。
skill 目錄名稱保留，`scoped_rules` 照樣對得上。

**驗證**：`tests/test_stage_scan_input.py` 在拋棄式 git repo 上驗證 CRLF 還原、binary 與 `eol=crlf`
不動、未追蹤與 gitignore、pathspec／exclude、CLI 輸出，共 6 項；拿掉 CRLF 替換那一行，還原測試會失敗。
本機 checkout 仍有 466 個 CRLF 檔，gate 暫存 278 個檔、正規化 278 個，50 個 skill 全數通過。

## 2026-09-11：批次審查 — 5 個已合併 commit ＋ 12 個 PR

commit 水位 `e55de88` → `5b2c000`；PR 水位 571 → 583；issue 水位維持 569（`--strict` 實查無新項目）。

### 略過：Converly 二次上架（上游 commit `d4ff28a` / PR #574）—維持與 #571 相反方向的一致立場

**上游做了什麼**：Aaron Beashel 補完款項與上架表單，`partners.json` 的 converly 條目 `active` 改回
`true`，README／REGISTRY 的 Verified Partners 區塊與 Tool Index 列復原，`tools/integrations/converly.md`
從 `.partners-pending/` 復原。commit 訊息明講「the inverse of the #571 unpublish」。

**為什麼不跟進（即使 #571 下架的理由——未付款——已經不成立）**：`#571` 決策條目寫的下架理由有兩層，
「未付款」只是觸發點，真正的立場是「**本 fork 與 Converly 沒有任何商業關係，卻在替一個廠商掛保證**」。
`d4ff28a` 復原的免責聲明字句是「Converly sponsors Marketing Skills」——這是上游與 Converly 之間的贊助
關係揭露，不是本 fork 的。付款清償只讓上游那筆揭露變得準確，不會讓本 fork 平白多出一個商業關係。
`FORK.md`／`docs/UPSTREAM.md` 既有規則本來就是「作者宣傳、贊助 CTA、個人事業連結略過」，贊助商揭露卡片
正是這一類。維持略過，不是重新評估後撤回，是同一條規則第二次套用到同一個廠商。

**落地**：不 cherry-pick。`partners.json` 的 converly 條目維持本 fork既有的 `active: false`；不新增
`tools/integrations/converly.md`；README／REGISTRY 不變。

**觸發條件**：無——這不是「等上游狀態變化再看」的暫緩，是本 fork 對贊助商內容的一貫政策，除非維護者明確
決定要跟進贊助揭露。

### 略過：Ploy Skill Partner 上架三部曲（上游 commit `4fbe11f`／`88de9fd`／`5cd4a7e`，PR #576–#578）

**上游做了什麼**：`4fbe11f` 以 `active:false` 暫存 Ploy（等上架包裹），`88de9fd` 在款項清償後轉為
`active:true` 並補上 README／REGISTRY／`tools/integrations/ploy.md`（同樣帶 `?ref=` 導流連結與
「Ploy sponsors...」性質的贊助商卡片），`5cd4a7e` 把 `category` 欄修成網站上分類格線用的正式名稱
（純上游站台顯示邏輯，`categoryShort` 不受影響）。

**為什麼略過**：與 Converly 同一類——這是上游與 Ploy 的付費 Skill Partner 關係揭露，不是本 fork 的。
即使 `5cd4a7e` 是單純的分類字串修正也一併略過，因為它修正的是 `88de9fd` 這個本 fork 本來就不採用的
條目；沒有 `88de9fd` 的內容，`5cd4a7e` 沒有東西可修。

**落地**：三個 commit 都不 cherry-pick；本 fork 的 `partners.json` 不含 ploy 條目。

**觸發條件**：同 Converly——這是政策性略過，不是等待中的暫緩。

### 採用：ai-seo 2.5.0 — ChatGPT 5.6 format-volatility 指引（上游 commit `5b2c000` / PR #579）

**上游做了什麼**：`skills/ai-seo/SKILL.md` 改寫 Content Types 段落並新增
`references/format-volatility.md`（ChatGPT 5.6 後 listicle／comparison 引用率分別下滑
50.5%／32.1%、`site:`／official 檢索上升的資料與應對），`evals/evals.json` 新增第 10 筆
eval，`VERSIONS.md`／`.claude-plugin/plugin.json`／`.claude-plugin/marketplace.json` 版本號
從 2.11.0 前進到 2.11.1（ai-seo 2.4.0 → 2.5.0）。

**為什麼採用**：純產品 skill 內容與版本號更新，不碰 README／REGISTRY／partners、不碰三支加了
repo 閘門的 workflow，與繁中入口、Windows gate、測試都沒有衝突。`AGENTS.md` 的邊界寫明產品
`skills/` 以上游為準。

**落地**：`git cherry-pick -x 5b2c000`（不用 `git merge`，因為同一段上游歷史裡夾著上面兩組略過
的贊助商 commit；逐筆 cherry-pick 才能只拿 ai-seo 這一筆）。乾淨套用，無衝突。

**觸發條件**：無，已完成。

### 暫緩：7 個尚未合併的上游 PR（#572、#573、#575、#580、#581、#582、#583）

逐筆讀過 diff；全部維持 OPEN，上游尚未定案（`#581` 自己說「20 commits, one per file...happy
to squash」，內容還可能變動）。依審查清冊的既定原則——不採用未合併的 open PR，除非它修的是本 fork
自己的工具能證明存在的缺陷——逐一記錄：

- **#572** `fix(ai-seo): distinguish search and training crawlers`：改 `skills/ai-seo/SKILL.md`
  與兩份 references，屬產品內容修正，非本 fork 特有缺陷。暫緩。
- **#573** `feat: analysis-discipline hardening from Magister benchmark evidence (2.11.1)`：
  改 4 個 skill 的 SKILL.md，屬產品內容擴充。暫緩。
- **#575** `feat: add no-slop skill (2.12.0)`：新增整個 `skills/no-slop/`，屬產品新增。暫緩。
- **#580** `fix: make standalone skill tool links portable`：把 `skills/ai-seo`／
  `skills/churn-prevention`／`skills/emails` 裡 `../../tools/...` 相對連結換成絕對
  GitHub blob URL，理由是「只複製 skill 資料夾時相對連結會斷」。
- **#581** `fix(skills): portable tools links...(fixes #524)`：同一類修正，範圍擴大到 20 個
  skill 檔共 105 個連結。
  **#580／#581 為什麼不算「本 fork 自己的工具能證明存在的缺陷」**：`tools/check_links.py` 檔頭
  明寫「不掃 skills/ 與 tools/integrations/：那些是上游產品」，程式也只 glob repo 根目錄、
  `docs/`、`.github/` 的 `.md`。本 fork 現有的連結檢查工具**完全不驗證這類連結**，所以無法用
  它證明這是本 fork 目前展示得出來的缺陷；只是上游自陳的已知問題，尚未合併。暫緩到合併之後
  再走一般產品同步流程。
- **#582** `feat: add md2video-audio skill`：新增含 Python 腳本的整個技能，屬產品新增；若合併，
  下次審查要另外評估 `.py` 腳本是否落入 Windows gate 的 SkillSpector 掃描範圍。暫緩。
- **#583** `fix: repair internal documentation links`：改 `scripts/sync-partners.mjs`、
  `skills/ad-creative`、`skills/ads` 的一份 reference 與 `tools/PARTNERS.md`。同樣是上游
  自己（非本 fork 工具）發現並待合併的連結修正。暫緩。

**觸發條件**：任一 PR 合併後，經由 commit 軸抵達，下次批次審查照一般流程逐筆判斷；若上游關閉
不合併，則比照 `#570` 的處理方式不再引用。
