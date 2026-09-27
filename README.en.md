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

This repository currently ships **50** product skills. The descriptions below are upstream trigger phrases used for discovery.

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
- **SEO & discovery**: `seo-audit`, `ai-seo`, `programmatic-seo`, `site-architecture`, `competitors`, `schema`, `aso`, `content-strategy`
- **Paid & distribution**: `ads`, `events`, `ad-creative`, `social`
- **Measurement**: `analytics`, `ab-testing`, `attribution`
- **Retention**: `churn-prevention`
- **Growth**: `co-marketing`, `free-tools`, `referrals`, `lead-magnets`, `community-marketing`
- **Strategy**: `marketing-ideas`, `marketing-psychology`, `launch`, `pricing`, `offers`, `marketing-plan`, `marketing-loops`, `marketing-council`
- **Sales & RevOps**: `revops`, `sales-enablement`, `prospecting`, `directory-submissions`, `public-relations`, `competitor-profiling`, `influencer-marketing`

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
