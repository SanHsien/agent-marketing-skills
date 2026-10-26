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


def test_a_query_string_is_not_part_of_the_path(root: Path) -> None:
    """GitHub serves `target.md?plain=1`; the query selects a view, not a file."""
    assert problems_for(root, "[x](target.md?plain=1)\n") == []
    assert problems_for(root, "[x](target.md?plain=1#top)\n") == []


def test_a_query_string_does_not_hide_a_missing_target(root: Path) -> None:
    assert len(problems_for(root, "[x](gone.md?plain=1)\n")) == 1


def test_links_inside_code_are_examples_not_links(root: Path) -> None:
    """A doc that shows `[x](gone.md)` as markup is not claiming that file exists."""
    text = (
        "Write `[x](gone.md)` like this:\n\n"
        "```md\n[x](gone.md)\n```\n\n"
        "~~~\n![i](gone.png)\n~~~\n"
    )
    assert problems_for(root, text) == []


def test_code_stripping_does_not_swallow_real_links_around_it(root: Path) -> None:
    text = "```\n[x](inside.md)\n```\n\n[ok](target.md) and [bad](gone.md) and `code`\n"
    problems = problems_for(root, text)
    assert len(problems) == 1 and "gone.md" in problems[0]


def test_a_code_span_inside_link_text_still_checks_the_target(root: Path) -> None:
    assert len(problems_for(root, "[`name`](gone.md)\n")) == 1
    assert problems_for(root, "[`name`](target.md)\n") == []


def test_a_stray_backtick_does_not_hide_links_in_other_paragraphs(root: Path) -> None:
    text = "a stray ` backtick here\n\n[bad](gone.md)\n\nand another ` one\n"
    problems = problems_for(root, text)
    assert len(problems) == 1 and "gone.md" in problems[0]


def test_a_missing_image_is_reported_once(root: Path) -> None:
    """`![i](gone.png)` also looks like a plain link; it is one problem, not two."""
    assert len(problems_for(root, "![alt](gone.png)\n")) == 1


def test_two_separate_links_to_one_missing_file_are_both_reported(root: Path) -> None:
    assert len(problems_for(root, "[a](gone.md)\n\n[b](gone.md)\n")) == 2
