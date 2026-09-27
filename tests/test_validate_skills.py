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
