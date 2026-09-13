English | [中文版](CHANGELOG.md)

# Changelog

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); newest first.
This file records **this fork's maintenance history** only (from 2026-08-27). The product
history of upstream
[`coreyhaines31/marketingskills`](https://github.com/coreyhaines31/marketingskills) lives in
its own history and in the review ledger at [`docs/UPSTREAM.md`](docs/UPSTREAM.md). Per-commit
adopt/skip reasoning is recorded in [`docs/DECISIONS.md`](docs/DECISIONS.md).

---

## 2026-09-11 (batch review)

### Synced

- **ai-seo 2.5.0 (upstream commit `5b2c000`, cherry-picked).** Format-volatility guidance and a
  new reference for the post-ChatGPT-5.6 drop in listicle/comparison citation share; pure product
  content and version bump, no fork-file conflicts.

### Skipped

- **Converly re-onboarding (`d4ff28a`) and the Ploy onboarding trio (`4fbe11f`/`88de9fd`/`5cd4a7e`).**
  Upstream restored the sponsor disclosure once payment cleared, but that's upstream's commercial
  relationship with the vendor, not this fork's; the existing sponsor-CTA skip policy stands. Seven
  upstream PRs are still open (#572, #573, #575, #580, #581, #582, #583) and deferred until merged.
  Reasoning in [`docs/DECISIONS.md`](docs/DECISIONS.md).

## 2026-09-11

### Changed

- **SkillSpector pin moved to 2.11.2 (`75bd6f3`).** Exact fingerprints are bound to the scanner version by design, so all of them were regenerated: 40 hashes replaced with every reason kept verbatim, and 5 entries that 2.11.2 no longer produces removed. Verified on an LF staging copy byte-identical to CI: all 50 skills pass, and the mutation probe is still caught. Details in [`docs/DECISIONS.md`](docs/DECISIONS.md).

### Fixed

- **The local gate was always red on a CRLF checkout.** A checkout made before `.gitattributes` keeps text files as CRLF, and exact fingerprints hash file content, so every baselined finding looked new locally. The self-scan now scans a staging copy made by `tools/stage_scan_input.py`: the files git sees (tracked plus not yet committed, without gitignored ones), with text files whose index copy is LF restored to LF, and binary, `eol=crlf` and untracked files copied byte for byte. On the local checkout with 466 CRLF files, all 50 skills pass.

## 2026-08-27 (review)

### Fixed

- **Windows CI checkout.** Upstream `CLAUDE.md` is a git symlink. With `core.symlinks=false` on Windows, `git add` stored the file body as the symlink target, and the runner failed with `Filename too long`. It is now a regular file, with a test that blocks git symlinks.
- **Relative links escaping the worktree.** `check_links.py` now rejects paths that resolve outside the repository root.
- **Issue/PR routing.** `ISSUE_TEMPLATE/config.yml` now links this fork's `CONTRIBUTING.md` and keeps a separate upstream product-contribution link. Skill-request and product-skill PR templates say not to open those against this fork.
- **Upstream validate-skill workflow.** `validate-skill.yml` now has the same official-repo gate as `sync-skills.yml` and `release.yml`.

### Added

- **`REVIEW.md`.** First project-review snapshot.

## 2026-08-27

### Added

- **Windows-first maintenance overlay.** `AGENTS.md`, `CLAUDE.md`, `FORK.md`, `NOTICE.md`,
  `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `docs/`, maintenance scripts under
  `tools/`, `tests/`, and GitHub workflows for CI, CodeQL, Dependabot, upstream review, and
  dependency freshness. CI runs Ubuntu 3.9–3.14 plus Windows Python 3.14: pytest, ruff (E9+F),
  `validate_skills.py`, `node --check`, and relative-link checks.
- **Public entry in Traditional Chinese and English only.** `README.md` is the Chinese
  primary file; `README.en.md` is the English mirror. Source and license credit stay;
  author promotion and sponsorship CTAs do not.

### Changed

- `sync-skills.yml` and `release.yml` now run only on the upstream official repository, so
  this fork cannot overwrite the Traditional Chinese README or auto-publish product releases.
