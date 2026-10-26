"""What the relative-link checker must accept and must not let through.

Every document is written under a fake repo root so the checker's own repo is not
involved. A false failure trains people to ignore the gate; a silent pass is a broken
link nobody sees.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import check_links  # noqa: E402


@pytest.fixture()
def root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    fake_root = tmp_path.resolve()
    (fake_root / "target.md").write_text("# target\n", encoding="utf-8")
    monkeypatch.setattr(check_links, "ROOT", fake_root)
    return fake_root


def problems_for(root: Path, text: str) -> list[str]:
    doc = root / "doc.md"
    doc.write_text(text, encoding="utf-8")
    return check_links.check_document(doc)


def test_a_link_title_is_not_part_of_the_path(root: Path) -> None:
    """`[x](target.md "Title")` is ordinary CommonMark and the file exists."""
    assert problems_for(root, '[x](target.md "A title")\n') == []
    assert problems_for(root, "[x](target.md 'A title')\n") == []


def test_a_title_does_not_hide_a_missing_target(root: Path) -> None:
    assert len(problems_for(root, '[x](gone.md "A title")\n')) == 1
