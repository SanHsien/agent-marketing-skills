# Marketing Skills

<p>
  <a href="README.md">繁體中文</a> ·
  <a href="README.en.md"><strong>English</strong></a>
</p>

[![CI](https://github.com/SanHsien/agent-marketing-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/SanHsien/agent-marketing-skills/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

Marketing skills for AI agents: conversion optimization, copywriting, SEO, analytics, and growth engineering. Works with Claude Code, OpenAI Codex, Cursor, Windsurf, and any agent that supports the [Agent Skills spec](https://agentskills.io).

> **This is a Windows-first maintenance fork of [`coreyhaines31/marketingskills`](https://github.com/coreyhaines31/marketingskills).** It keeps the MIT license and full git history. Product behaviour follows upstream; this line adds Traditional Chinese docs, a Windows development gate, and commit-by-commit upstream review. See [`FORK.md`](FORK.md) and [`docs/UPSTREAM.md`](docs/UPSTREAM.md).

## How skills work together

The `product-marketing` skill is the foundation — every other skill checks it first to understand your product, audience, and positioning.

See each skill's **Related Skills** section for the full dependency map.

## Available skills

This repository ships the product skills listed below. The descriptions below are upstream trigger phrases used for discovery.

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

## Install the skills

Copy the product directories under `skills/` into an Agent Skills folder. Do not copy `docs/`, `tests/`, or this fork's Python/PowerShell maintenance tools.

Typical locations: `~/.agents/skills/`, `~/.claude/skills/`, or `~/.cursor/skills/`.

```powershell
npx skills add SanHsien/agent-marketing-skills
npx skills add SanHsien/agent-marketing-skills --skill cro copywriting
```

Claude Code plugin:

```text
/plugin marketplace add SanHsien/agent-marketing-skills
/plugin install marketing-skills
```

`/plugin` works only in an interactive Claude Code CLI session. On the web, in GitHub Actions or other non-interactive environments, use:

```powershell
claude plugin marketplace add SanHsien/agent-marketing-skills
claude plugin install marketing-skills@marketingskills
```

Codex plugin:

```powershell
codex plugin marketplace add SanHsien/agent-marketing-skills
```

Then run `/plugins` inside a Codex session and pick **marketing-skills**; `codex plugin marketplace upgrade` picks up later releases.

To let your agent read your marketing accounts, follow the guided connection workflow in [`tools/SETUP.md`](tools/SETUP.md) for scoped credentials and a first read-only result.

Maintainer setup (Windows):

```powershell
git clone https://github.com/SanHsien/agent-marketing-skills.git
cd agent-marketing-skills
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements-dev.txt
.venv\Scripts\python -m pip install -r requirements-security.txt
pwsh -NoProfile -File tools\dev_check.ps1
```

Details: [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md).

## Usage

Once installed, ask for marketing help in plain language:

```text
"Help me optimize this landing page for conversions"
→ Uses cro

"Write homepage copy for my SaaS"
→ Uses copywriting

"Set up GA4 tracking for signups"
→ Uses analytics
```

You can also invoke skills directly: `/cro`, `/emails`, `/seo-audit`.

## Skill categories

- **Conversion**: `cro`, `signup`, `onboarding`, `popups`, `paywalls`
- **Content & copy**: `copywriting`, `copy-editing`, `cold-email`, `emails`, `social`, `image`
- **SEO & discovery**: `seo-audit`, `ai-seo`, `programmatic-seo`, `site-architecture`, `competitors`, `link-building`, `schema`, `aso`, `content-strategy`
- **Paid & distribution**: `ads`, `events`, `ad-creative`, `social`
- **Measurement**: `analytics`, `ab-testing`, `attribution`, `conversion-tracking`
- **Retention**: `churn-prevention`
- **Growth**: `co-marketing`, `free-tools`, `referrals`, `lead-magnets`, `community-marketing`
- **Strategy**: `marketing-ideas`, `marketing-psychology`, `launch`, `pricing`, `offers`, `marketing-plan`, `marketing-loops`, `marketing-council`
- **Sales & RevOps**: `revops`, `sales-enablement`, `prospecting`, `directory-submissions`, `public-relations`, `competitor-profiling`, `reverse-engineer-marketing`, `influencer-marketing`

The tool registry is [`tools/REGISTRY.md`](tools/REGISTRY.md). Partner rules live in [`tools/PARTNERS.md`](tools/PARTNERS.md). Those are upstream product files; this fork does not endorse vendors.

## Upgrading from v1.x to v2.0

v2.0 renames 17 skills and consolidates `page-cro` + `form-cro` into `cro`. After upgrading, remove stale v1 folders from the install directory, then reinstall. The product context file moved to `.agents/product-marketing.md`.

| Old | New |
|-----|-----|
| `ab-test-setup` | `ab-testing` |
| `analytics-tracking` | `analytics` |
| `aso-audit` | `aso` |
| `competitor-alternatives` | `competitors` |
| `email-sequence` | `emails` |
| `form-cro` | merged into `cro` |
| `free-tool-strategy` | `free-tools` |
| `launch-strategy` | `launch` |
| `onboarding-cro` | `onboarding` |
| `page-cro` | `cro` |
| `paid-ads` | `ads` |
| `paywall-upgrade-cro` | `paywalls` |
| `popup-cro` | `popups` |
| `pricing-strategy` | `pricing` |
| `product-marketing-context` | `product-marketing` |
| `referral-program` | `referrals` |
| `schema-markup` | `schema` |
| `signup-flow-cro` | `signup` |
| `social-content` | `social` |

## Repository structure

```text
agent-marketing-skills/
├── README.md              ← Traditional Chinese public entry (this fork)
├── README.en.md           ← English version
├── LICENSE                ← MIT
├── skills/                ← Product Agent Skills
├── tools/clis/            ← Upstream zero-dependency Node.js CLIs
├── tools/integrations/    ← Upstream integration guides
├── .claude-plugin/        ← Claude Code marketplace
├── AGENTS.md / FORK.md    ← Fork maintenance rules
├── docs/                  ← Development, upstream review, decisions
└── tools/*.py / *.ps1     ← Windows gate and upstream checks
```

## Source and license

This repository is a fork of [`coreyhaines31/marketingskills`](https://github.com/coreyhaines31/marketingskills) and remains MIT. The product skills, CLIs, and integration guides are upstream work. See [`LICENSE`](LICENSE) and [`NOTICE.md`](NOTICE.md).

This fork's maintenance changes are recorded in [`CHANGELOG.en.md`](CHANGELOG.en.md); its relationship to and differences from upstream are in [`FORK.md`](FORK.md).
