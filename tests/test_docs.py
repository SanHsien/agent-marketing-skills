from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import check_links  # noqa: E402
import validate_skills  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def test_every_skill_directory_has_valid_frontmatter() -> None:
    skill_dirs = validate_skills.iter_skill_dirs()
    assert len(skill_dirs) >= 40
    failures = []
    for skill_dir in skill_dirs:
        errors, _warnings = validate_skills.audit_skill(skill_dir)
        if errors:
            failures.append(f"{skill_dir.name}: {errors}")
    assert failures == []


def test_product_cli_scripts_exist() -> None:
    clis = list((ROOT / "tools" / "clis").glob("*.js"))
    assert len(clis) >= 50


def test_plugin_manifest_exists() -> None:
    plugin = ROOT / ".claude-plugin" / "plugin.json"
    marketplace = ROOT / ".claude-plugin" / "marketplace.json"
    assert plugin.is_file()
    assert marketplace.is_file()
    text = plugin.read_text(encoding="utf-8")
    assert '"name": "marketing-skills"' in text


def test_maintainer_markdown_links_resolve() -> None:
    failures = 0
    for path in check_links.iter_documents():
        problems = check_links.check_document(path)
        failures += len(problems)
        for problem in problems:
            print(f"{path}: {problem}")
    assert failures == 0


def test_ci_covers_python_314_and_uses_scanner_compatible_windows() -> None:
    workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert '"3.14"' in workflow
    assert "windows / py3.13" in workflow
    assert "python -m pip install -r requirements-security.txt" in workflow


def test_fresh_clone_docs_install_the_pinned_security_scanner() -> None:
    assert (ROOT / ".python-version").read_text(encoding="utf-8").strip() == "3.13"
    for relative_path in (
        "AGENTS.md",
        "README.md",
        "README.en.md",
        "FORK.md",
        "docs/DEVELOPMENT.md",
    ):
        text = (ROOT / relative_path).read_text(encoding="utf-8")
        assert "requirements-security.txt" in text, relative_path


def test_security_scanner_pin_supports_configurable_resource_budgets() -> None:
    requirement = (
        "skillspector @ git+https://github.com/SanHsien/SkillSpector.git@"
        "82bbe8bd88a624d13849ed29757ac568e5341732"
    )
    assert requirement in (ROOT / "requirements-security.txt").read_text(
        encoding="utf-8"
    )


def test_canonical_gate_has_realistic_full_scan_budgets() -> None:
    dev_check = (ROOT / "tools" / "dev_check.ps1").read_text(encoding="utf-8")
    assert "[int]$SkillSpectorMaxStaticSeconds = 300" in dev_check
    assert "[int]$SkillSpectorMaxWorkflowSeconds = 900" in dev_check


def test_canonical_gate_uses_a_deterministic_python_hash_seed() -> None:
    dev_check = (ROOT / "tools" / "dev_check.ps1").read_text(encoding="utf-8")
    assert '$previousPythonHashSeed = $env:PYTHONHASHSEED' in dev_check
    assert '$env:PYTHONHASHSEED = "0"' in dev_check
    assert '$env:PYTHONHASHSEED = $previousPythonHashSeed' in dev_check


def test_upstream_workflows_have_repo_guard() -> None:
    fork_owned = {
        "ci.yml",
        "upstream-check.yml",
        "codeql.yml",
        "dependency-freshness.yml",
    }
    workflows = ROOT / ".github" / "workflows"
    scanned = 0
    for path in sorted(workflows.glob("*.yml")):
        if path.name in fork_owned:
            continue
        scanned += 1
        text = path.read_text(encoding="utf-8")
        assert "github.repository == 'coreyhaines31/marketingskills'" in text, path.name
    assert scanned >= 3


def test_issue_contact_links_point_at_this_fork() -> None:
    text = (ROOT / ".github" / "ISSUE_TEMPLATE" / "config.yml").read_text(
        encoding="utf-8"
    )
    assert "SanHsien/agent-marketing-skills/blob/main/CONTRIBUTING.md" in text
    assert "coreyhaines31/marketingskills/blob/main/CONTRIBUTING.md" in text


def test_public_docs_are_traditional_chinese_and_english_only() -> None:
    assert not (ROOT / "README.ja.md").exists()
    for name in ("README.md", "README.en.md"):
        text = (ROOT / name).read_text(encoding="utf-8")
        assert "README.ja.md" not in text


def test_readme_keeps_credit_without_author_promotion() -> None:
    banned = (
        "conversionfactory.co",
        "swipefiles.com",
        "magistermarketing.com",
        "codingformarketers.com",
        "corey.co?ref=",
        "marketing-skills.com/sponsorship",
        "vercel.com/oss/program-badge",
        "Become a partner",
    )
    zh = (ROOT / "README.md").read_text(encoding="utf-8")
    en = (ROOT / "README.en.md").read_text(encoding="utf-8")
    for name, text in (("README.md", zh), ("README.en.md", en)):
        for needle in banned:
            assert needle not in text, f"{name} still promotes {needle}"
        assert "coreyhaines31/marketingskills" in text
        assert "NOTICE.md" in text
        assert "MIT" in text
    assert "SanHsien/agent-marketing-skills" in zh
    assert r"~\.agents\skills" in zh
    assert "npx skills add SanHsien/agent-marketing-skills" in zh
    assert "npx skills add SanHsien/agent-marketing-skills" in en


def test_bilingual_pairs_cross_link_each_other() -> None:
    for zh_name, en_name in (("README.md", "README.en.md"), ("CHANGELOG.md", "CHANGELOG.en.md")):
        zh = ROOT / zh_name
        en = ROOT / en_name
        assert zh.is_file(), f"missing {zh_name}"
        assert en.is_file(), f"missing {en_name}"
        assert en_name in zh.read_text(encoding="utf-8"), f"{zh_name} does not link {en_name}"
        assert zh_name in en.read_text(encoding="utf-8"), f"{en_name} does not link {zh_name}"


def test_changelog_records_fork_history_not_upstream_product_history() -> None:
    text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    assert "docs/UPSTREAM.md" in text
    assert "docs/DECISIONS.md" in text
    assert "coreyhaines31/marketingskills" in text


def test_tool_config_matches_ci_flags() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    ci = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert 'target-version = "py39"' in pyproject
    assert "--target-version py39" in ci
    assert 'select = ["E9", "F"]' in pyproject
    assert "--select E9,F" in ci
    assert not re.search(r"^\[project\]", pyproject, re.M)
    assert not re.search(r"^\[build-system\]", pyproject, re.M)


def test_line_endings_are_pinned_to_lf() -> None:
    attrs = (ROOT / ".gitattributes").read_text(encoding="utf-8")
    assert "* text=auto eol=lf" in attrs
    for suffix in ("*.md", "*.py", "*.ps1", "*.js"):
        assert suffix in attrs


def test_gitignore_covers_secrets_and_reports() -> None:
    text = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert ".env" in text
    assert ".venv/" in text
    assert "upstream-review-report.md" in text


def test_review_md_is_a_risk_snapshot() -> None:
    review = (ROOT / "REVIEW.md").read_text(encoding="utf-8")
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "Windows-first" in review
    assert "R-01" in review
    assert "風險快照" in agents
    assert "`REVIEW.md`" in agents


def test_tracked_files_are_not_git_symlinks() -> None:
    result = subprocess.run(
        ["git", "ls-files", "-s"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    symlinks = [
        line.split("\t", 1)[-1]
        for line in result.stdout.splitlines()
        if line.startswith("120000 ")
    ]
    assert symlinks == [], f"git symlink 會讓 Windows checkout 失敗: {symlinks}"


def test_check_links_rejects_path_outside_repo(tmp_path: Path) -> None:
    doc = tmp_path / "note.md"
    doc.write_text("[here](.)\n", encoding="utf-8")
    problems = check_links.check_document(doc)
    assert any("逃出" in item for item in problems)
