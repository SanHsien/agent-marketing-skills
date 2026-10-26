from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import validate_skills  # noqa: E402


def test_audit_flags_missing_skill_file(tmp_path: Path) -> None:
    skill_dir = tmp_path / "cro"
    skill_dir.mkdir()
    errors, _warnings = validate_skills.audit_skill(skill_dir)
    assert errors
    assert "Missing SKILL.md" in errors[0]


def test_audit_flags_name_mismatch(tmp_path: Path) -> None:
    skill_dir = tmp_path / "cro"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text(
        "---\nname: ads\ndescription: When the user wants ads.\n---\n\n# Ads\n",
        encoding="utf-8",
    )
    errors, _warnings = validate_skills.audit_skill(skill_dir)
    assert any("Name mismatch" in item for item in errors)


def test_audit_accepts_quoted_description(tmp_path: Path) -> None:
    skill_dir = tmp_path / "cro"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text(
        '---\nname: cro\ndescription: "When the user wants CRO, mention conversion."\n---\n\n# CRO\n',
        encoding="utf-8",
    )
    errors, warnings = validate_skills.audit_skill(skill_dir)
    assert errors == []
    assert warnings == []


def _write_skill(tmp_path: Path, name: str, text: str) -> Path:
    skill_dir = tmp_path / name
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text(text, encoding="utf-8")
    return skill_dir


def test_dashes_inside_a_frontmatter_value_do_not_end_the_frontmatter(tmp_path: Path) -> None:
    """Only a line that is exactly `---` closes the block.

    Splitting on the first `---` anywhere cut the frontmatter off in the middle of a
    description, so every field after it (here a top-level `version:`) was never audited.
    """
    skill_dir = _write_skill(
        tmp_path,
        "cro",
        "---\nname: cro\ndescription: Use when the user asks --- anything about CRO.\n"
        "version: 1.0.0\n---\n\n# CRO\n",
    )
    errors, _warnings = validate_skills.audit_skill(skill_dir)
    assert any("'version' is top-level" in item for item in errors)


def test_frontmatter_requires_the_closing_delimiter_on_its_own_line() -> None:
    extract = validate_skills.extract_frontmatter
    assert extract("---\nname: a\ndescription: Use it\n") is None
    crlf = extract("---\r\nname: a\r\n---\r\nbody\r\n")
    assert crlf is not None and crlf.strip() == "name: a"
    dashed = extract("---\nname: a\ndescription: x --- y\n---\nbody\n")
    assert dashed is not None and dashed.strip().endswith("x --- y")
