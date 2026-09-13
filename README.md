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

目前倉庫收錄 **50** 個產品 skill。說明欄是上游的觸發語（英文），安裝後由宿主用來決定何時呼叫。

<!-- SKILLS:START -->
| Skill | Description |
|-------|-------------|
| [ab-testing](skills/ab-testing/) | When the user wants to plan, design, or implement an A/B test or experiment, or build a growth experimentation program.... |
| [ad-creative](skills/ad-creative/) | When the user wants to generate, iterate, or scale ad creative — headlines, descriptions, primary text, or full ad... |
| [ads](skills/ads/) | When the user wants help with paid advertising campaigns on Google Ads, Meta (Facebook/Instagram), LinkedIn, Twitter/X,... |
| [ai-seo](skills/ai-seo/) | When the user wants to optimize content for AI search engines, get cited by LLMs, or appear in AI-generated answers.... |
| [analytics](skills/analytics/) | When the user wants to set up, improve, or audit analytics tracking and measurement. Also use when the user mentions... |
| [aso](skills/aso/) | When the user wants to audit or optimize an App Store or Google Play listing. Also use when the user mentions 'ASO... |
| [attribution](skills/attribution/) | When the user wants to figure out which marketing actually drives conversions and revenue, choose or interpret an... |
| [churn-prevention](skills/churn-prevention/) | When the user wants to reduce churn, build cancellation flows, set up save offers, recover failed payments, or... |
| [co-marketing](skills/co-marketing/) | When the user wants to find co-marketing partners, plan joint campaigns, or brainstorm partnership opportunities. Use... |
| [cold-email](skills/cold-email/) | Write B2B cold emails and follow-up sequences that get replies. Use when the user wants to write cold outreach emails,... |
| [community-marketing](skills/community-marketing/) | Build and leverage online communities to drive product growth and brand loyalty. Use when the user wants to create a... |
| [competitor-profiling](skills/competitor-profiling/) | When the user wants to research, profile, or analyze competitors from their URLs. Also use when the user mentions... |
| [competitors](skills/competitors/) | When the user wants to create competitor comparison or alternative pages for SEO and sales enablement. Also use when... |
| [content-strategy](skills/content-strategy/) | When the user wants to plan a content strategy, decide what content to create, or figure out what topics to cover. Also... |
| [copy-editing](skills/copy-editing/) | When the user wants to edit, review, or improve existing marketing copy, or refresh outdated content. Also use when the... |
| [copywriting](skills/copywriting/) | When the user wants to write, rewrite, or improve marketing copy for any page — including homepage, landing pages,... |
| [cro](skills/cro/) | When the user wants to optimize, improve, or increase conversions on any marketing page or form — including homepage,... |
| [customer-research](skills/customer-research/) | When the user wants to conduct, analyze, or synthesize customer research. Use when the user mentions "customer... |
| [directory-submissions](skills/directory-submissions/) | When the user wants to submit their product to startup, SaaS, AI, agent, MCP, no-code, or review directories for... |
| [emails](skills/emails/) | When the user wants to create or optimize an email sequence, drip campaign, automated email flow, or lifecycle email... |
| [events](skills/events/) | When the user wants to plan, run, sponsor, speak at, or get pipeline from events — webinars, conferences, trade shows,... |
| [free-tools](skills/free-tools/) | When the user wants to plan, evaluate, or build a free tool for marketing purposes — lead generation, SEO value, or... |
| [image](skills/image/) | When the user wants to create, generate, edit, or optimize images for marketing — blog heroes, social graphics, product... |
| [influencer-marketing](skills/influencer-marketing/) | When the user wants to run influencer, creator, or ambassador partnerships to promote their product — finding and... |
| [launch](skills/launch/) | When the user wants to plan a product launch, feature announcement, or release strategy. Also use when the user... |
| [lead-magnets](skills/lead-magnets/) | When the user wants to create, plan, or optimize a lead magnet for email capture or lead generation. Also use when the... |
| [marketing-council](skills/marketing-council/) | When the user wants multiple expert perspectives on a marketing question — a simulated board of advisors staffed by... |
| [marketing-ideas](skills/marketing-ideas/) | When the user needs marketing ideas, inspiration, or strategies for their SaaS or software product. Also use when the... |
| [marketing-loops](skills/marketing-loops/) | When the user wants to set up a recurring, self-running marketing workflow — a repeatable loop an AI agent runs on a... |
| [marketing-plan](skills/marketing-plan/) | When the user needs a comprehensive marketing plan for a client, a company they advise, or their own product. Also use... |
| [marketing-psychology](skills/marketing-psychology/) | When the user wants to apply psychological principles, mental models, or behavioral science to marketing. Also use when... |
| [offers](skills/offers/) | When the user wants to design, construct, or improve an offer — the thing they actually sell — including value framing,... |
| [onboarding](skills/onboarding/) | When the user wants to optimize post-signup onboarding, user activation, first-run experience, or time-to-value. Also... |
| [paywalls](skills/paywalls/) | When the user wants to create or optimize in-app paywalls, upgrade screens, upsell modals, or feature gates. Also use... |
| [popups](skills/popups/) | When the user wants to create or optimize popups, modals, overlays, slide-ins, or banners for conversion purposes. Also... |
| [pricing](skills/pricing/) | When the user wants help with pricing decisions, packaging, or monetization strategy. Also use when the user mentions... |
| [product-marketing](skills/product-marketing/) | When the user wants to create or update their product marketing context document. Also use when the user mentions... |
| [programmatic-seo](skills/programmatic-seo/) | When the user wants to create SEO-driven pages at scale using templates and data. Also use when the user mentions... |
| [prospecting](skills/prospecting/) | When the user wants to find, qualify, and build a list of prospects to reach out to — across B2B SaaS, general B2B, or... |
| [public-relations](skills/public-relations/) | When the user wants help with public relations, earned media, press coverage, journalist outreach, or media strategy... |
| [referrals](skills/referrals/) | When the user wants to create, optimize, or analyze a referral program, affiliate program, or word-of-mouth strategy.... |
| [revops](skills/revops/) | When the user wants help with revenue operations, lead lifecycle management, or marketing-to-sales handoff processes.... |
| [sales-enablement](skills/sales-enablement/) | When the user wants to create sales collateral, pitch decks, one-pagers, objection handling docs, or demo scripts. Also... |
| [schema](skills/schema/) | When the user wants to add, fix, or optimize schema markup and structured data on their site. Also use when the user... |
| [seo-audit](skills/seo-audit/) | When the user wants to audit, review, or diagnose SEO issues on their site. Also use when the user mentions "SEO... |
| [signup](skills/signup/) | When the user wants to optimize signup, registration, account creation, or trial activation flows. Also use when the... |
| [site-architecture](skills/site-architecture/) | When the user wants to plan, map, or restructure their website's page hierarchy, navigation, URL structure, or internal... |
| [sms](skills/sms/) | When the user wants to plan, build, or optimize SMS or MMS marketing — including welcome flows, abandoned cart texts,... |
| [social](skills/social/) | When the user wants help creating, scheduling, or optimizing social media content for LinkedIn, Twitter/X, Instagram,... |
| [video](skills/video/) | When the user wants to create, generate, or produce video content using AI tools or programmatic frameworks. Also use... |
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

### 選項 3：複製資料夾

```powershell
git clone https://github.com/SanHsien/agent-marketing-skills.git
Copy-Item -Recurse agent-marketing-skills\skills\* $HOME\.agents\skills\
```

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
- **SEO 與發現**：`seo-audit`、`ai-seo`、`programmatic-seo`、`site-architecture`、`competitors`、`schema`、`aso`、`content-strategy`
- **付費與分發**：`ads`、`events`、`ad-creative`、`social`
- **衡量與測試**：`analytics`、`ab-testing`、`attribution`
- **留存**：`churn-prevention`
- **增長工程**：`co-marketing`、`free-tools`、`referrals`、`lead-magnets`、`community-marketing`
- **策略與變現**：`marketing-ideas`、`marketing-psychology`、`launch`、`pricing`、`offers`、`marketing-plan`、`marketing-loops`、`marketing-council`
- **業務與 RevOps**：`revops`、`sales-enablement`、`prospecting`、`directory-submissions`、`public-relations`、`competitor-profiling`、`influencer-marketing`

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
