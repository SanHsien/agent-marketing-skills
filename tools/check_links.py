#!/usr/bin/env python3
"""檢查維護文件之間的相對連結。

本 fork 的公開入口互相連來連去：README、FORK、NOTICE、AGENTS 與 docs。
文件被重新定位或改名時，這些連結會靜靜斷掉。只驗相對連結；外部網址交給人看。
不掃 skills/ 與 tools/integrations/：那些是上游產品，每次同步都會變。

    python tools/check_links.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
LINK_PATTERN = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
IMAGE_PATTERN = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
HTML_SRC_PATTERN = re.compile(r"""(?is)<img[^>]+src=["']([^"']+)["']""")
HTML_HREF_PATTERN = re.compile(r"""(?is)<a\b[^>]*?\bhref=["']([^"']+)["']""")
# `[label]: destination "title"`, but not a footnote definition (`[^1]: text`).
REFERENCE_PATTERN = re.compile(r"(?m)^[ \t]{0,3}\[(?!\^)[^\]]+\]:[ \t]*(<[^>\n]*>|\S+)")
SKIP_PREFIXES = ("http://", "https://", "mailto:", "tel:", "#")

SKIP_NAMES = {
    "upstream-review-report.md",
    "dependency-freshness-report.md",
}


def iter_documents() -> list[Path]:
    documents = []
    documents.extend(ROOT.glob("*.md"))
    documents.extend((ROOT / "docs").glob("*.md"))
    github = ROOT / ".github"
    if github.is_dir():
        documents.extend(github.rglob("*.md"))
    return sorted(
        path
        for path in documents
        if path.is_file() and path.name not in SKIP_NAMES
    )


def _destination(target: str) -> str:
    """The URL part of a link destination, without an optional `"title"`.

    CommonMark allows `[x](path "title")` and `[x](<path with spaces> 'title')`; the
    title is separated from the path by whitespace, so it is never part of the file name.
    """
    target = target.strip()
    if target.startswith("<"):
        end = target.find(">")
        return target[1:end] if end > 0 else target[1:]
    return target.split(None, 1)[0] if target else ""


def _missing_relative(path: Path, target: str) -> str | None:
    target = _destination(target)
    if not target or target.startswith(SKIP_PREFIXES):
        return None
    # Neither the fragment nor a query string (`file.md?plain=1`) names a file.
    file_part = unquote(target.split("#", 1)[0].split("?", 1)[0])
    if not file_part:
        return None
    resolved = (path.parent / file_part).resolve()
    if not resolved.is_relative_to(ROOT):
        return f"{target} → 連結逃出 repo 根目錄"
    if resolved.exists():
        return None
    try:
        shown = resolved.relative_to(ROOT)
    except ValueError:
        shown = resolved
    return f"{target} → 找不到 {shown}"


FENCE_PATTERN = re.compile(r"^[ \t]{0,3}(`{3,}|~{3,})")
# A code span cannot cross a blank line, so a stray backtick cannot swallow a paragraph.
CODE_SPAN_PATTERN = re.compile(r"(?<!`)(`+)(?!`)((?:(?!\n[ \t]*\n).)+?)(?<!`)\1(?!`)", re.S)


def strip_code(text: str) -> str:
    """Remove fenced code blocks and inline code spans.

    Markup shown as an example (`[x](path)` in a backtick span or a fenced block) is not
    a link, so it must not be looked up as one. An unterminated fence runs to the end of
    the file, as in CommonMark.
    """
    kept: list[str] = []
    fence: str | None = None
    for line in text.splitlines(keepends=True):
        marker = FENCE_PATTERN.match(line)
        if fence is None:
            if marker:
                fence = marker.group(1)
            else:
                kept.append(line)
        elif marker and marker.group(1)[0] == fence[0] and len(marker.group(1)) >= len(fence):
            fence = None
    return CODE_SPAN_PATTERN.sub("", "".join(kept))


def check_document(path: Path) -> list[str]:
    problems: list[str] = []
    text = strip_code(path.read_text(encoding="utf-8"))
    seen: set[tuple[int, int]] = set()
    for pattern in (
        LINK_PATTERN,
        IMAGE_PATTERN,
        HTML_SRC_PATTERN,
        HTML_HREF_PATTERN,
        REFERENCE_PATTERN,
    ):
        for match in pattern.finditer(text):
            # `![alt](path)` also matches the plain-link pattern: one destination, one check.
            if match.span(1) in seen:
                continue
            seen.add(match.span(1))
            missing = _missing_relative(path, match.group(1))
            if missing:
                problems.append(missing)
    return problems


def main() -> int:
    documents = iter_documents()
    if not documents:
        print("找不到任何維護用 Markdown 檔")
        return 1

    failures = 0
    for path in documents:
        problems = check_document(path)
        rel = path.relative_to(ROOT)
        if problems:
            failures += 1
            for problem in problems:
                print(f"FAIL {rel}: {problem}")
        else:
            print(f"OK   {rel}")

    print(f"\n共 {len(documents)} 份維護文件，{failures} 份有缺檔。")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
