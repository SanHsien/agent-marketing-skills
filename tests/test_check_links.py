"""What the relative-link checker must accept and must not let through.

Every document is written under a fake repo root so the checker's own repo is not
involved. A false failure trains people to ignore the gate; a silent pass is a broken
link nobody sees.
"""

from __future__ import annotations

import os
import subprocess
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


def test_a_broken_reference_style_definition_is_reported(root: Path) -> None:
    """`[ref]: gone.md` is a link too; only inline links were being looked up."""
    problems = problems_for(root, "See [the guide][ref].\n\n[ref]: gone.md\n")
    assert len(problems) == 1 and "gone.md" in problems[0]
    assert problems_for(root, "See [the guide][ref].\n\n[ref]: target.md \"Title\"\n") == []
    assert problems_for(root, "[ref]: https://example.com/x\n") == []


def test_a_footnote_definition_is_not_a_link(root: Path) -> None:
    assert problems_for(root, "Text[^1].\n\n[^1]: Some explanation, not a path.\n") == []


def test_a_broken_html_anchor_href_is_reported(root: Path) -> None:
    problems = problems_for(root, '<a href="gone.md">x</a>\n')
    assert len(problems) == 1 and "gone.md" in problems[0]
    assert problems_for(root, '<a href="target.md">x</a> <a href="#top">y</a>\n') == []


def test_summary_survives_a_console_that_cannot_encode_chinese() -> None:
    """The report is Traditional Chinese; a legacy-codepage console must not crash it.

    Run as a child process with an ASCII stdout, which is what a redirected pipe on a
    machine without UTF-8 mode looks like. The gate's verdict must come from the links,
    not from whether the terminal can print the summary line.
    """
    env = {**os.environ, "PYTHONUTF8": "0", "PYTHONIOENCODING": "ascii"}
    result = subprocess.run(
        [sys.executable, str(Path(check_links.__file__))],
        capture_output=True,
        env=env,
        cwd=check_links.ROOT,
    )
    assert result.returncode == 0, result.stderr.decode("utf-8", "replace")
    assert "維護文件".encode("utf-8") in result.stdout


@pytest.mark.parametrize(
    "target",
    [
        "ftp://example.com/file.txt",
        "data:text/plain;base64,aGk=",
        "javascript:void(0)",
        "//cdn.example.com/logo.png",
        "HTTPS://example.com/Upper",
    ],
)
def test_urls_with_any_scheme_are_not_repository_paths(root: Path, target: str) -> None:
    """Only http(s), mailto and tel were skipped; every other URL was looked up as a file."""
    assert problems_for(root, f"[x]({target})\n") == []
