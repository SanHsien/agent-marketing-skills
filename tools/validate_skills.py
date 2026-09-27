#!/usr/bin/env python3
"""Validate every skills/*/SKILL.md against the Agent Skills frontmatter contract.

This is a Windows-friendly replacement for validate-skills.sh. Errors fail the
gate; warnings are printed and ignored. Product skills stay English; this
script does not translate or rewrite them.

    python tools/validate_skills.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")


def _reconfigure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def extract_frontmatter(text: str) -> str | None:
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    return parts[1]


def field_value(frontmatter: str, name: str) -> str:
    pattern = re.compile(
        rf"^{re.escape(name)}:\s*(?:\"([^\"]*)\"|'([^']*)'|(.*))\s*$",
        re.M,
    )
    match = pattern.search(frontmatter)
    if not match:
        return ""
    return next(group for group in match.groups() if group is not None).strip()


def audit_skill(skill_dir: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    skill_file = skill_dir / "SKILL.md"
    skill_name = skill_dir.name
    if not skill_file.is_file():
        return ["Missing SKILL.md"], warnings

    text = skill_file.read_text(encoding="utf-8")
    frontmatter = extract_frontmatter(text)
    if frontmatter is None or not frontmatter.strip():
        return ["Missing YAML frontmatter (---)"], warnings

    name_in_file = field_value(frontmatter, "name")
    if not name_in_file:
        errors.append("Missing 'name' field in frontmatter")
    elif name_in_file != skill_name:
        errors.append(
            f"Name mismatch: directory={skill_name!r} but frontmatter={name_in_file!r}"
        )
    elif not NAME_RE.fullmatch(name_in_file):
        errors.append(
            f"Invalid name format: {name_in_file!r} (lowercase alphanumeric + hyphens)"
        )
    elif not 1 <= len(name_in_file) <= 64:
        errors.append(f"Name length invalid: {len(name_in_file)} chars (must be 1-64)")

    description = field_value(frontmatter, "description")
    if not description:
        errors.append("Missing 'description' field in frontmatter")
    elif not 1 <= len(description) <= 1024:
        errors.append(
            f"Description length invalid: {len(description)} chars (must be 1-1024)"
        )
    else:
        lowered = description.lower()
        if not any(token in lowered for token in ("when", "mention", "use")):
            warnings.append("Description lacks clear trigger phrases")

    if re.search(r"^version:", frontmatter, re.M):
        errors.append("'version' is top-level (should be under 'metadata:')")

    line_count = text.count("\n") + (0 if text.endswith("\n") else 1)
    if line_count > 500:
        warnings.append(f"SKILL.md is {line_count} lines (should be <500)")

    return errors, warnings


def iter_skill_dirs(root: Path = SKILLS_DIR) -> list[Path]:
    if not root.is_dir():
        return []
    return sorted(path for path in root.iterdir() if path.is_dir())


def main() -> int:
    _reconfigure_stdio()
    skill_dirs = iter_skill_dirs()
    if not skill_dirs:
        print("找不到 skills/ 目錄")
        return 1

    issues = 0
    warnings = 0
    passed = 0
    for skill_dir in skill_dirs:
        skill_errors, skill_warnings = audit_skill(skill_dir)
        name = skill_dir.name
        if skill_errors:
            issues += 1
            print(f"FAIL {name}")
            for item in skill_errors:
                print(f"  Error: {item}")
            for item in skill_warnings:
                print(f"  Warning: {item}")
        elif skill_warnings:
            warnings += 1
            print(f"WARN {name}")
            for item in skill_warnings:
                print(f"  Warning: {item}")
        else:
            passed += 1
            print(f"OK   {name}")

    print()
    print(f"Passed: {passed}; warnings: {warnings}; issues: {issues}")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
