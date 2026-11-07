# 宿主最小技能使用驗收：Claude Code（2026-11-08）

結果：**通過**。一個真的載入本 fork plugin 的 Claude Code 非互動 session 依序觸發了 `product-marketing` 與 `copywriting`，產出背景文件與首頁主視覺文案。範圍只涵蓋這兩個 skill，不是全部 52 個，也不涵蓋其他宿主或任何產品 CLI（見 `REVIEW.md` 〈尚未宣稱範圍〉）。規格出處：`docs/DECISIONS.md` 2026-11-08。

## 執行方式

- 版本：Claude Code 2.1.310（`claude --version`）；session 預設模型 `claude-opus-5-5`；本 fork `main` `a431d303740367b9aa8f1d4162d95d824916962d`（工作樹，驗收當下無未提交的 `skills/` 變更）。
- 指令（cwd 為不含任何專案檔的暫存空目錄，避免宿主讀到本 repo 的 `AGENTS.md`；提示詞由 stdin 送入，因為 `--allowedTools`／`--add-dir` 會吃掉位置參數）：

```text
claude -p --plugin-dir <repo> --output-format stream-json --verbose --allowedTools "Skill Read Write Edit Glob Grep" --add-dir <repo> < prompt.txt
```

- 提示詞（全文，產品為虛構）：

```text
This is a non-interactive host acceptance run. Do not ask me questions; make reasonable assumptions and state them. Fictional, de-identified product background: "Tidepool" is a self-serve web app that helps 3-15 person bookkeeping firms collect client documents (receipts, bank statements) by emailed upload links, with automatic reminders and a per-client checklist. Pricing: flat USD 49 per month per firm, 14-day free trial, no card required. Audience: firm owners tired of chasing clients over email. Main competitor: shared inbox plus spreadsheet. Brand voice: plain, calm, practical. Tasks, in this order: (1) Use the product-marketing skill: load it with the Skill tool and, following its workflow, write the product marketing context document to .agents/product-marketing.md in the current directory using only the background above (no codebase to scan). (2) Then use the copywriting skill: load it with the Skill tool, read the context document you just wrote, and write homepage hero copy (headline, subhead, primary CTA) for Tidepool. Do not call any ad, email or paid API, and do not use the network. In your final answer print the context document content and the hero copy in full, and list every file you read.
```

- 第一次嘗試（exit 1）：位置參數被 `--allowedTools`／`--add-dir` 吃掉，stderr 為 `Error: Input must be provided either through stdin or as a prompt argument when using --print`，沒有任何模型呼叫，不計入驗收。以上是第二次，exit code 0。

## 技能載入紀錄（stream-json 的實際事件）

| 事件序號 | 事件 | 內容 |
| --- | --- | --- |
| 6 | `system` / `init` | `plugins` 含 `marketing-skills`（`source: marketing-skills@inline`、`version: 2.14.0`、`path` 為本工作樹）；`skills` 列出 53 項 `marketing-skills:` 前綴（回報，未逐一核對與 52 的差異）；`permissionMode: auto`；`cwd` 為暫存空目錄 |
| 10–11 | `tool_use` / `tool_result` | `Skill` `{"skill": "marketing-skills:product-marketing"}` → `Launching skill: marketing-skills:product-marketing` |
| 12 | `user`（技能內容注入） | 開頭 `Base directory for this skill: <repo>/skills/product-marketing`，內容 13182 字元 |
| 17–18 | `tool_use` / `tool_result` | `Bash` 唯讀 `ls -la .agents .claude product-marketing-context.md; pwd`：三者皆不存在（技能 Step 1 的既有檔檢查）。`--allowedTools` 沒列 Bash，`permissionMode: auto` 放行了這個唯讀指令 |
| 22, 24 | `tool_use` / `tool_result` | `Write` `<cwd>\.agents\product-marketing.md` → `File created successfully` |
| 23, 25 | `tool_use` / `tool_result` | `Skill` `{"skill": "marketing-skills:copywriting"}` → `Launching skill: marketing-skills:copywriting` |
| 26 | `user`（技能內容注入） | 開頭 `Base directory for this skill: <repo>/skills/copywriting`，內容 14573 字元 |
| 28–29 | `tool_use` / `tool_result` | `Read` 剛寫的 `.agents/product-marketing.md`（copywriting 的「Before Writing」步驟要求先讀） |
| 30–31 | `tool_use` / `tool_result` | `Read` `skills\copywriting\references\ai-tells.md` |
| 38 | `result` | `subtype: success`、`is_error: false`、`num_turns: 9`、`duration_ms: 86289`、`stop_reason: end_turn` |

沒有任何網路工具呼叫（`server_tool_use`：`web_search_requests` 0、`web_fetch_requests` 0），沒有廣告、郵件或付費 API。

## 被讀取檔案的 SHA

git blob 為 `git hash-object`，與 `HEAD` 上同路徑的 blob 相同（未修改）。SHA-256 為 `sha256sum`。

| 檔案 | git blob | SHA-256 |
| --- | --- | --- |
| `skills/product-marketing/SKILL.md`（經 Skill 工具載入） | `3af463a602aa0233c4d5fc98c23ba13224aa8f6b` | `19ece0fa75c72a5a8b6e90db80f506586f54cc93bae6bffbb1bd2ef4ae7d603c` |
| `skills/copywriting/SKILL.md`（經 Skill 工具載入） | `2453731ab7a5e52535b7cf29beccbebe687d5a62` | `02f0ab1ddd41d95b3c230d4bcff3de6578c8f2e45776c8ef2e4b931636af5bee` |
| `skills/copywriting/references/ai-tells.md`（Read） | `0a93ab3b88fc2c683ff6280db187644a7aa04612` | `b98c3a19b3a75c714d69e80a0076e4c07244b0e833c2ce81ff2631224fb7f7b2` |
| 暫存 cwd 的 `.agents/product-marketing.md`（宿主產出，7789 位元組，不入庫） | 不適用 | `1c63f76f589215618b76c24eadb0fd8dbba3a259191b80d4f789f1b330dabb6c` |

## 輸出全文（`result` 事件的 `result` 欄，已遮罩的節錄）

以下是**已遮罩的節錄**，不是原樣：家目錄與暫存路徑換成 `<repo>`、`<tmp-cwd>` 佔位符；宿主在最前面印的一行招呼來自執行者本機的使用者層設定，與本 fork skill 無關，已移除。其餘文字未改。文案本身是英文，說明段是繁中。表中的雜湊值都是對未遮罩的原檔實算（`skills/` 下三個檔不含這些路徑，宿主產出的背景文件也不含），不受遮罩影響。

````markdown
兩項都做完了。產品行銷背景文件已寫到 `.agents/product-marketing.md`，首頁主視覺文案也寫好了。過程中沒有連網，也沒有呼叫任何廣告、郵件或付費 API。

**我做的假設**（文件裡都標了 *(assumption)*，要再確認）：
- 客戶點上傳連結不用登入或註冊帳號。
- 主要購買者是事務所老闆。
- 不適合的客群是個人記帳師和超過 15 人的大事務所。
- 產品分類用「client document collection」，也就是客戶文件收集。

背景資料裡沒有任何數據、客戶名稱或推薦語，所以文案一個都沒寫，也沒有編造。

## 1. `.agents/product-marketing.md` 全文

```markdown
# Product Marketing Context

**Document version:** v1
**Last updated:** 2026-11-08

> Drafted only from the product brief supplied on 2026-11-08 (no codebase, no customer interviews). Items marked *(assumption)* are inferred and need confirmation. No real metrics, logos, or testimonials exist yet — do not invent them in copy.

## Product Overview
**One-liner:** Tidepool collects client documents for bookkeeping firms, so you stop chasing receipts and bank statements over email.
**What it does:** Firms send each client an emailed upload link. Tidepool sends automatic reminders until the documents arrive and tracks what is still missing on a per-client checklist.
**Product category:** Client document collection for bookkeeping and accounting firms *(assumption: how buyers search — "client document collection", "document request software for bookkeepers")*
**Product type:** Self-serve B2B SaaS (web app)
**Business model:** Flat USD 49 per month per firm. 14-day free trial, no card required.

## Target Audience
**Target companies:** Bookkeeping firms with 3-15 people.
**Decision-makers:** Firm owner (buys and usually also uses it).
**Primary use case:** Getting clients to send the documents the firm needs, on time, without manual follow-up.
**Jobs to be done:**
- Ask each client for the right documents without writing the same email again and again.
- Follow up automatically until the documents arrive.
- See at a glance which clients are missing what.
**Use cases:**
- Month-end close: collect bank statements and receipts from every client.
- Onboarding a new client: request the starting set of documents.
- Year-end / tax season prep *(assumption)*.

## Personas
| Persona | Cares about | Challenge | Value we promise |
|---------|-------------|-----------|------------------|
| Firm owner (decision maker, financial buyer, often user) | Getting work done on time without chasing clients; predictable cost | Hours lost to reminder emails and tracking who sent what | Clients get reminded for you; one checklist shows what is missing; one flat price |
| Bookkeeper on staff (user) *(assumption)* | Having documents in hand when the work starts | Digging through a shared inbox for attachments | Documents arrive in one place, matched to the client |

## Problems & Pain Points
**Core problem:** Clients are slow to send documents, and the firm has to chase them by email.
**Why alternatives fall short:**
- Shared inbox: attachments get buried in threads; no record of what is still missing.
- Spreadsheet: someone has to update it by hand, so it goes stale.
- Manual reminders: someone has to remember to send them, client by client.
**What it costs them:** Staff time spent on follow-up instead of bookkeeping; late closes *(assumption)*.
**Emotional tension:** Tired of chasing clients; awkward about nagging; worry that something was missed.

## Competitive Landscape
**Direct:** Other client document collection tools *(not named in brief — research before naming any)*.
**Secondary:** Shared inbox plus spreadsheet (the main competitor) — falls short because tracking and reminders are manual, and nothing ties a received file to a checklist item.
**Indirect:** Asking clients by phone, or doing nothing and waiting — falls short because it does not scale past a few clients and nothing is recorded.

## Differentiation
**Key differentiators:**
- Emailed upload links: clients upload without setting up an account *(assumption: confirm clients need no login)*.
- Automatic reminders until the documents arrive.
- A per-client checklist that shows what is in and what is missing.
- Flat USD 49 per month per firm, not per user or per client.
**How we do it differently:** Replaces the inbox-and-spreadsheet routine with one link, automatic follow-up, and a live checklist.
**Why that's better:** Less time chasing, fewer missed documents, a clear status for every client.
**Why customers choose us:** Simple to start (self-serve, no card for the trial) and a price that does not grow with headcount.

## Objections
| Objection | Response |
|-----------|----------|
| "My clients won't use another tool." | They click a link in an email and upload. That's it. *(confirm no client login)* |
| "The inbox and spreadsheet work well enough." | They work until someone forgets a follow-up. Tidepool sends the reminders and keeps the list current for you. |
| "Another subscription?" | One flat USD 49 a month for the whole firm. Try it free for 14 days, no card. |

**Anti-persona:** Solo bookkeepers with a handful of clients *(assumption)*; large firms (well over 15 people) that need deep practice-management integrations *(assumption)*; firms that do not collect recurring documents from clients.

## Switching Dynamics
**Push:** Constant chasing of clients by email; documents lost in the inbox; spreadsheet out of date.
**Pull:** Automatic reminders; a checklist that shows what is missing; flat price; free trial with no card.
**Habit:** The inbox-and-spreadsheet routine is familiar and costs nothing extra.
**Anxiety:** Will clients actually use the link? How long does setup take? Is it worth one more tool?

## Customer Language
**How they describe the problem:**
- "chasing clients" (from the brief)
- "tired of chasing clients over email" (from the brief)
- More verbatim phrases needed — collect from trial users and sales calls.
**How they describe us:**
- None yet.
**Words to use:** chase, remind, upload link, checklist, missing, receipts, bank statements, clients, firm
**Words to avoid:** "revolutionize", "seamless", "AI-powered", "platform", "solution", "effortless", "game-changer" — they clash with the plain, calm voice and are vague.
**Glossary:**
| Term | Meaning |
|------|---------|
| Upload link | The emailed link a client uses to send documents |
| Reminder | Automatic follow-up email sent until documents arrive |
| Checklist | Per-client list of requested documents and their status |

## Brand Voice
| Attribute | Means | Doesn't mean | Example line |
|-----------|-------|--------------|--------------|
| Plain | Short, everyday words; say what it does | Dumbed down or slangy | "Send a link. Tidepool sends the reminders." *(draft line)* |
| Calm | Steady, no urgency tricks or hype | Flat or dull | "Your clients will get there. We'll keep reminding them." *(draft line)* |
| Practical | Lead with the task and the result | Feature dumps | "See who's missing what, per client." *(draft line)* |

**Tone by context:**
- Support: Patient, step-by-step, no blame.
- Launch: Say what's new and what it saves you; no fanfare.
- Errors: Say what happened and what to do next.
- Sales: Honest fit check; point out the free trial.
- Social: Light, practical tips for running a firm.
**Terms we own:** none yet.
**Never use (and why):** hype words listed above — they undercut calm and plain.

## Proof Points
**Metrics:** None yet.
**Customers:** None yet.
**Testimonials:** None yet — do not fabricate.
**Value themes:**
| Theme | Proof |
|-------|-------|
| Stop chasing clients | Automatic reminders (product capability) |
| Know what's missing | Per-client checklist (product capability) |
| Simple, predictable cost | Flat USD 49/month per firm; 14-day trial, no card |

## Goals
**Business goal:** Grow paying firms through self-serve signups *(assumption)*.
**Conversion action:** Start the 14-day free trial (no card required).
**Current metrics:** Unknown.

## Learnings
*Decisions and tested lessons. Newest first. Keep it to about 20 active entries.*
| Date | Learning | Evidence | Applies to | Status |
|------|----------|----------|------------|--------|

## Changelog
*Newest first. One line per revision: what changed and why.*
- v1 (2026-11-08) — Initial context, drafted from the product brief only.
```

## 2. 首頁主視覺文案

這次屬於從零寫起：只有背景資料，沒有現成草稿。Learnings 一節是空的，所以沒有已測試過的角度要避開。

**Headline:** Stop chasing clients for receipts and bank statements.

**Subhead:** Send each client an upload link by email. Tidepool reminds them until the documents arrive, and a checklist shows what's still missing for every client.

**Primary CTA:** Start my free trial
**CTA 下方小字:** 14 days free. No card required. Then USD 49/month for your whole firm.

**這樣寫的理由**
- 標題用的是背景資料裡客戶自己的說法「chasing clients」，再點名具體文件，讀者看得到畫面。共用信箱加試算表這種做法講不出這句話。
- 副標照「做法 → 自動提醒 → 看到缺什麼」的順序寫。沒有用破折號，也沒有「not X, but Y」或「No X, no Y」這類一看就像 AI 寫的句型。
- 免卡片只在按鈕旁邊提一次，價格也放在這裡，用來回應「又多一筆訂閱」的疑慮。

**備選版本**
- 標題 B：Your clients send their documents. Tidepool does the reminding. 語氣更平靜，但痛點比較不明顯。
- 標題 C：Know which clients are missing what, without another email. 主打檢查清單，適合重視進度追蹤的老闆。
- CTA B：Try Tidepool free for 14 days，把試用天數直接放進按鈕。

## 讀過的檔案
- `<repo>/skills/product-marketing/SKILL.md`（用 Skill 工具載入）
- `<repo>/skills/copywriting/SKILL.md`（用 Skill 工具載入）
- `<tmp-cwd>/.agents/product-marketing.md`（我剛寫的背景文件）
- `<repo>/skills/copywriting/references/ai-tells.md`（交稿前的 AI 腔自我檢查）

開工前也確認過 `.agents/`、`.claude/`、`product-marketing-context.md` 都不存在。這只是列出目錄，沒有讀任何檔案內容。

**下一步：** 確認上面標了 assumption 的項目，尤其是「客戶免登入」。如果不成立，「點連結就能上傳」的說法就要改。
````

## 判讀

- 通過條件（`docs/DECISIONS.md` 2026-11-08 的驗收規格）逐項：虛構去識別背景（是）；依序套用 `product-marketing` 與 `copywriting`（是，事件 10 與 23）；保存載入紀錄、輸出全文與被讀檔案 SHA（本檔）；不呼叫廣告、郵件或付費 API（是）。
- 技能行為與其文字相符：product-marketing 先檢查既有 context 檔再寫入 `.agents/product-marketing.md`；copywriting 先讀該檔再寫稿，並讀了 `references/ai-tells.md`。輸出標出假設、沒有編造數據或推薦語。
- 這份證據只證明 Claude Code 能經 `--plugin-dir` 載入並觸發這兩個 skill。沒有證明其餘 skill、Codex／Cursor 宿主、`/plugin` 互動安裝路徑，或任何產品 CLI。
