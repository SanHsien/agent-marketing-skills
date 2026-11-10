<div align="center">

# Marketing Skills

### 給 AI Agent 的行銷技能包：CRO、文案、SEO、分析與增長工程

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Platform: Claude Code](https://img.shields.io/badge/Platform-Claude%20Code-f97316.svg)](https://code.claude.com/)
[![Platform: Codex](https://img.shields.io/badge/Platform-Codex-10a37f.svg)](https://developers.openai.com/codex/skills)
[![Platform: Cursor](https://img.shields.io/badge/Platform-Cursor-000000.svg)](https://cursor.com/)
[![CI](https://github.com/SanHsien/agent-marketing-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/SanHsien/agent-marketing-skills/actions/workflows/ci.yml)

<p>
  <a href="README.md"><strong>繁體中文</strong></a> ·
  <a href="README.en.md">English</a>
</p>

</div>

> **這是源自 [`coreyhaines31/marketingskills`](https://github.com/coreyhaines31/marketingskills) 的 Windows-first 維護型 fork**，沿用 MIT 授權與完整 Git 歷史。產品 Skills、CLI 與整合指南跟隨上游；本維護線補上繁中入口、Windows 開發／驗收 gate，以及逐筆審查的上游追蹤。差異見 [`FORK.md`](FORK.md)，同步策略見 [`docs/UPSTREAM.md`](docs/UPSTREAM.md)。

給技術行銷與創辦人用的 Agent Skills：讓編碼用的 AI 助手能做轉化優化、文案、SEO、分析與增長工程。相容 [Agent Skills 規格](https://agentskills.io)，可在 Claude Code、OpenAI Codex、Cursor、Windsurf 等宿主使用。

## Skills 怎麼一起運作

`product-marketing` 是基礎——其他 skill 會先讀它，了解產品、受眾與定位，再動手。

```
                            ┌──────────────────────────────────────┐
                            │          product-marketing           │
                            │    (read by all other skills first)  │
                            └──────────────────┬───────────────────┘
                                               │
    ┌──────────────┬─────────────┬─────────────┼─────────────┬──────────────┬──────────────┐
    ▼              ▼             ▼             ▼             ▼              ▼              ▼
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────┐ ┌──────────┐ ┌─────────────┐ ┌───────────┐
│  SEO &   │ │   CRO    │ │Content & │ │  Paid &    │ │ Growth & │ │  Sales &    │ │ Strategy  │
│ Content  │ │          │ │   Copy   │ │Measurement │ │Retention │ │    GTM      │ │           │
└──────────┘ └──────────┘ └──────────┘ └────────────┘ └──────────┘ └─────────────┘ └───────────┘
```

各 skill 的 **Related Skills** 一節有完整依賴圖。

## 可用 Skills

本倉庫收錄的產品 skill 清單如下。說明欄是上游的觸發語（英文），安裝後由宿主用來決定何時呼叫。

<!-- SKILLS:START -->
| Skill | Description |
|-------|-------------|
| [ab-testing](skills/ab-testing/) | When the user wants to plan, run, or read A/B tests, or asks a judgement call on one: is the result real, can we stop,... |
| [ad-creative](skills/ad-creative/) | When the user wants to write or judge ad creative, or asks which ad, hook, or angle to run or kill: headlines, primary... |
| [ads](skills/ads/) | When the user wants to plan, run, or fix paid ads on Google, Meta, and LinkedIn, or asks a judgement call on them: are... |
| [ai-seo](skills/ai-seo/) | When the user wants to get cited and recommended in AI answers (ChatGPT, Perplexity, AI Overviews), or asks why AI... |
| [analytics](skills/analytics/) | When the user wants to set up or audit analytics, or asks whether a metric or number is calculated right, what to... |
| [aso](skills/aso/) | When the user wants to audit or optimize an App Store or Google Play listing, or asks which title, keywords, or... |
| [attribution](skills/attribution/) | When the user wants to work out which marketing drives revenue, or asks whether a channel is really working, which... |
| [churn-prevention](skills/churn-prevention/) | When the user wants to reduce churn, or asks why customers cancel, whether to offer a discount or pause: cancellation... |
| [co-marketing](skills/co-marketing/) | When the user wants co-marketing partners or joint campaigns, or asks whether a partner fits, a size mismatch matters,... |
| [cold-email](skills/cold-email/) | When the user wants to write or run B2B cold outbound, or asks whether an opener, reason to reach out, or email works... |
| [community-marketing](skills/community-marketing/) | When the user wants to build or grow an online community, or asks whether a community is worth it, where to host it, or... |
| [competitor-profiling](skills/competitor-profiling/) | When the user wants to research competitors into dated profiles, or asks what a rival charges, claims, or is doing, or... |
| [competitors](skills/competitors/) | When the user wants to create or audit comparison and alternative pages ('X vs Y', 'X alternative', 'best X... |
| [content-strategy](skills/content-strategy/) | When the user wants to plan content, or asks which topic or piece to prioritize, what to write about, or why posts... |
| [conversion-tracking](skills/conversion-tracking/) | When the user wants to set up, audit, or fix conversion tracking to Google Ads, Meta, GA4, LinkedIn, and TikTok, or... |
| [copy-editing](skills/copy-editing/) | When the user wants to edit, tighten, proofread, or refresh existing copy, or asks whether to keep, cut, or change a... |
| [copywriting](skills/copywriting/) | When the user wants to write or rewrite page copy (homepage, landing, pricing, feature), or asks which headline,... |
| [cro](skills/cro/) | When the user wants more conversions from a page or form, or asks why a page isn't converting, what to change first, or... |
| [customer-research](skills/customer-research/) | When the user wants to run or synthesize customer research, or asks what customer quotes, reviews, or feedback really... |
| [directory-submissions](skills/directory-submissions/) | When the user wants to list a product in startup, SaaS, AI, MCP, and review directories, or asks which directories are... |
| [emails](skills/emails/) | When the user wants to create or improve automated email sequences, or asks what to send, when, or whether an email or... |
| [events](skills/events/) | When the user wants to plan, run, sponsor, or speak at events, or asks whether an event or booth is worth the money:... |
| [free-tools](skills/free-tools/) | When the user wants to plan or build a free tool as marketing, or asks whether a tool idea is worth building or which... |
| [image](skills/image/) | When the user wants to create, generate, edit, or optimize marketing images, or asks which approach to take (generate,... |
| [influencer-marketing](skills/influencer-marketing/) | When the user wants creator, influencer, or ambassador partnerships, or asks which creators fit, what to pay, which... |
| [launch](skills/launch/) | When the user wants to plan a product or feature launch, or asks whether it's ready, when to announce, or how to get... |
| [lead-magnets](skills/lead-magnets/) | When the user wants to plan or improve a lead magnet, or asks what to give away for emails or how much to ask in return... |
| [link-building](skills/link-building/) | When the user wants backlinks and mentions that lift rankings and AI citations, or asks how to get sites to link or... |
| [marketing-council](skills/marketing-council/) | When the user wants several expert takes on a marketing decision, or asks what a famous marketer would say about it: a... |
| [marketing-ideas](skills/marketing-ideas/) | When the user wants marketing ideas or growth tactics for a software product, or asks what to try to get attention or... |
| [marketing-loops](skills/marketing-loops/) | When the user wants a recurring marketing job an AI agent runs on a cadence or trigger, or asks what a weekly or daily... |
| [marketing-plan](skills/marketing-plan/) | When the user wants a full marketing or go-to-market plan for a client, an advised company, or their own product, or... |
| [marketing-psychology](skills/marketing-psychology/) | When the user wants to apply psychology to marketing, or asks why buyers behave or value things as they do, or whether... |
| [offers](skills/offers/) | When the user wants to design or improve the offer itself, or asks why it isn't selling or how to add urgency honestly:... |
| [onboarding](skills/onboarding/) | When the user wants better onboarding and activation, or asks why new users don't stick or what the first session... |
| [paywalls](skills/paywalls/) | When the user wants to create or improve in-app paywalls and upgrade moments, or asks when or how hard to ask free... |
| [popups](skills/popups/) | When the user wants to create or improve popups, modals, slide-ins, sticky bars, and banners, or asks whether one will... |
| [pricing](skills/pricing/) | When the user wants to set pricing and packaging, or asks what to charge, whether to raise prices, or how to move... |
| [product-marketing](skills/product-marketing/) | When the user wants to create or update the product marketing context doc (.agents/product-marketing.md), or asks what... |
| [programmatic-seo](skills/programmatic-seo/) | When the user wants SEO pages at scale from templates and data, or asks whether a page set will rank or look thin:... |
| [prospecting](skills/prospecting/) | When the user wants to find and qualify prospects for outbound, or asks who to target first, which signal to... |
| [public-relations](skills/public-relations/) | When the user wants press and media coverage, or asks what to say to a reporter, whether a story is newsworthy, or how... |
| [referrals](skills/referrals/) | When the user wants referral and affiliate programs or word of mouth, or asks what to reward, how much to pay, or which... |
| [reverse-engineer-marketing](skills/reverse-engineer-marketing/) | When the user wants to know how another company grew and what to copy, or asks what a competitor did and when: a dated... |
| [revops](skills/revops/) | When the user wants to design revenue operations, or asks when a lead is ready for sales or why sales and marketing... |
| [sales-enablement](skills/sales-enablement/) | When the user wants sales collateral, or asks what to give a champion or rep, or how to answer an objection or make the... |
| [schema](skills/schema/) | When the user wants to add, fix, or validate schema markup (JSON-LD), or asks which type fits a page or whether some... |
| [seo-audit](skills/seo-audit/) | When the user wants to audit or diagnose SEO, or asks why traffic dropped, a page won't rank, or whether a setup like... |
| [signup](skills/signup/) | When the user wants better signup, registration, and trial start flows, or asks which fields or steps to cut or whether... |
| [site-architecture](skills/site-architecture/) | When the user wants to plan or restructure a website, or asks which pages they need or where something belongs:... |
| [sms](skills/sms/) | When the user wants SMS, MMS, or WhatsApp marketing, or asks whether texting is worth it or a message is allowed:... |
| [social](skills/social/) | When the user wants organic social content for LinkedIn, X, Instagram, TikTok, or Facebook, or asks what to post, which... |
| [video](skills/video/) | When the user wants to create video with AI tools or code, or asks which approach to use (screen recording, AI avatar,... |
<!-- SKILLS:END -->

## 安裝 Skills（本機呼叫）

把 `skills/` 底下的產品目錄放到 Agent Skills 目錄。根目錄其餘檔案是本 fork 的開發與治理骨架，不要一起複製進去。

| 宿主 | 建議路徑 |
| --- | --- |
| Codex | `~\.agents\skills\` |
| Claude Code | `~\.claude\skills\` |
| Cursor | `~\.cursor\skills\` |

### 選項 1：CLI 安裝

```powershell
npx skills add SanHsien/agent-marketing-skills
npx skills add SanHsien/agent-marketing-skills --skill cro copywriting
```

CLI 會偵測已安裝的宿主。若在 Agent session 內非互動執行、卻只裝到 `.agents/skills/`（Claude Code 不讀那裡），請明確指定：

```powershell
npx skills add SanHsien/agent-marketing-skills -a claude-code
```

### 選項 2：Claude Code Plugin

```text
/plugin marketplace add SanHsien/agent-marketing-skills
/plugin install marketing-skills
```

`/plugin` 只在互動式 Claude Code CLI 裡可用；網頁版、GitHub Actions 等非互動環境請改用：

```powershell
claude plugin marketplace add SanHsien/agent-marketing-skills
claude plugin install marketing-skills@marketingskills
```

### 選項 3：Codex Plugin

```powershell
codex plugin marketplace add SanHsien/agent-marketing-skills
```

接著在 Codex session 內執行 `/plugins`，選 **marketing-skills** 安裝全部 skill；之後要更新用 `codex plugin marketplace upgrade`。

### 選項 4：複製資料夾

```powershell
git clone https://github.com/SanHsien/agent-marketing-skills.git
Copy-Item -Recurse agent-marketing-skills\skills\* $HOME\.agents\skills\
```

想讓 Agent 讀你的行銷帳號資料，照 [`tools/SETUP.md`](tools/SETUP.md) 的引導流程建立最小權限憑證，並先取得一筆唯讀結果。

開發與驗收指令見 [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md)。維護者 clone：

```powershell
git clone https://github.com/SanHsien/agent-marketing-skills.git
cd agent-marketing-skills
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements-dev.txt
.venv\Scripts\python -m pip install -r requirements-security.txt
pwsh -NoProfile -File tools\dev_check.ps1
```

## 使用方式

安裝後直接問行銷問題即可：

```text
幫我優化這個落地頁的轉化
→ 使用 cro

幫我的 SaaS 寫首頁文案
→ 使用 copywriting

設定註冊的 GA4 追蹤
→ 使用 analytics

做一組 5 封歡迎信
→ 使用 emails
```

也可以直接呼叫：`/cro`、`/emails`、`/seo-audit`。

## 分類

- **轉化優化**：`cro`、`signup`、`onboarding`、`popups`、`paywalls`
- **內容與文案**：`copywriting`、`copy-editing`、`cold-email`、`emails`、`social`、`image`
- **SEO 與發現**：`seo-audit`、`ai-seo`、`programmatic-seo`、`site-architecture`、`competitors`、`link-building`、`schema`、`aso`、`content-strategy`
- **付費與分發**：`ads`、`events`、`ad-creative`、`social`
- **衡量與測試**：`analytics`、`ab-testing`、`attribution`、`conversion-tracking`
- **留存**：`churn-prevention`
- **增長工程**：`co-marketing`、`free-tools`、`referrals`、`lead-magnets`、`community-marketing`
- **策略與變現**：`marketing-ideas`、`marketing-psychology`、`launch`、`pricing`、`offers`、`marketing-plan`、`marketing-loops`、`marketing-council`
- **業務與 RevOps**：`revops`、`sales-enablement`、`prospecting`、`directory-submissions`、`public-relations`、`competitor-profiling`、`reverse-engineer-marketing`、`influencer-marketing`

工具登錄見 [`tools/REGISTRY.md`](tools/REGISTRY.md)；合作夥伴規則見 [`tools/PARTNERS.md`](tools/PARTNERS.md)。那些是上游產品檔，本 fork 不代為背書任何廠商。

## 從 v1.x 升到 v2.0

v2.0 重新命名 17 個 skill，並把 `page-cro` 與 `form-cro` 合併成 `cro`。若你裝過 v1.x，升級後安裝目錄會留下舊名資料夾，請自行清掉後重裝。完整對照表見 [`README.en.md`](README.en.md#upgrading-from-v1x-to-v20)。產品脈絡檔在 v2.0 改為 `.agents/product-marketing.md`。

## 倉庫結構

```text
agent-marketing-skills/
├── README.md              ← 繁中公開入口（本 fork）
├── README.en.md           ← English version
├── LICENSE                ← MIT
├── skills/                ← 產品 Agent Skills（不要改寫成維護索引）
├── tools/clis/            ← 上游零依賴 Node.js CLI
├── tools/integrations/    ← 上游工具整合指南
├── .claude-plugin/        ← Claude Code marketplace
├── AGENTS.md / FORK.md    ← 本 fork 維護規則
├── docs/                  ← 開發、上游審查、決策
└── tools/*.py / *.ps1     ← Windows gate 與上游檢查
```

## 來源與授權

本倉庫 fork 自 [`coreyhaines31/marketingskills`](https://github.com/coreyhaines31/marketingskills)，沿用 MIT License。產品 Skills、CLI 與整合指南為上游原作。完整標示見 [`LICENSE`](LICENSE) 與 [`NOTICE.md`](NOTICE.md)。

本 fork 的維護變更記在 [`CHANGELOG.md`](CHANGELOG.md)；與上游的關係與差異見 [`FORK.md`](FORK.md)。
