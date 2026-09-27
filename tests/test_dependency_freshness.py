"""Contract tests for the dependency freshness check.

The check is only useful if a red line means "someone has to look". Two things
can make that false: a false alarm that fires every month until people stop
reading the report, and a silencing move that hides a real gap. These tests pin
both edges -- the declared-precision comparison, and the two documented exits
(hold and deferral) with the deferral expiring by itself.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import check_dependency_freshness as checker  # noqa: E402


def test_comparison_uses_the_precision_the_declaration_states() -> None:
    # `>=7` says nothing about the minor, so 7.4.0 must not be a monthly alarm.
    assert not checker.is_newer_version("7.4.0", "7")
    assert checker.is_newer_version("8.0.0", "7")
    assert checker.is_newer_version("7.4.0", "7.3")
    assert not checker.is_newer_version("7.3.2", "7.3")


def test_prerelease_suffix_does_not_count_as_newer() -> None:
    assert not checker.is_newer_version("7.0.0rc1", "7.0.0")


def test_hold_marker_is_read_off_the_declaring_line() -> None:
    packages = checker.parse_requirements(
        "pytest>=8.3  # freshness-hold: pytest 9 requires Python 3.10, CI still tests 3.9\n"
        "ruff>=0.16\n",
        "requirements-dev.txt",
    )

    holds = {package["name"]: package["hold"] for package in packages}
    assert holds["ruff"] == ""
    assert holds["pytest"].startswith("pytest 9 requires Python 3.10")


def test_a_held_floor_is_reported_but_does_not_ask_for_work(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(checker, "fetch_pypi_version", lambda name: "9.1.0")
    packages = checker.parse_requirements(
        "pytest>=8.3  # freshness-hold: CI still tests 3.9\n", "requirements-dev.txt"
    )

    rows = checker.collect_status(packages, deferrals={})

    assert rows[0]["outdated"] is True
    assert checker.needs_review(rows[0]) is False
    assert "HELD: CI still tests 3.9" in checker.render_markdown(rows)


def test_a_live_deferral_covers_the_row_and_says_what_it_was_reviewed_against(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(checker, "fetch_pypi_version", lambda name: "9.1.0")
    packages = checker.parse_requirements("pytest>=8.3\n", "requirements-dev.txt")

    rows = checker.collect_status(
        packages, deferrals={"pytest": ("9.1", "reviewed 2026-08; wait for the 9.x line to settle")}
    )

    assert checker.needs_review(rows[0]) is False
    assert "DEFERRED at 9.1.0" in checker.render_markdown(rows)


def test_a_deferral_expires_once_pypi_moves_past_the_reviewed_release(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """This is the whole point of `deferredLatest`: it cannot become a mute button."""
    monkeypatch.setattr(checker, "fetch_pypi_version", lambda name: "10.0.0")
    packages = checker.parse_requirements("pytest>=8.3\n", "requirements-dev.txt")

    rows = checker.collect_status(packages, deferrals={"pytest": ("9.1", "not this month")})

    assert checker.needs_review(rows[0]) is True
    assert "REVIEW UPDATE" in checker.render_markdown(rows)


def test_deferral_without_a_reviewed_release_is_ignored(tmp_path: Path) -> None:
    path = tmp_path / "dependency-deferrals.json"
    path.write_text(
        json.dumps(
            {
                "deferrals": {
                    "kept": {"deferredLatest": "9.1", "reason": "reviewed, not now"},
                    "no-release": {"reason": "reviewed, not now"},
                    "no-reason": {"deferredLatest": "9.1"},
                }
            }
        ),
        encoding="utf-8",
    )

    assert checker.load_deferrals(path) == {"kept": ("9.1", "reviewed, not now")}


def test_missing_deferrals_file_is_not_an_error(tmp_path: Path) -> None:
    assert checker.load_deferrals(tmp_path / "nope.json") == {}


def test_report_names_both_exits_so_the_next_person_does_not_invent_a_third() -> None:
    report = checker.render_markdown([])

    assert "freshness-hold:" in report
    assert "dependency-deferrals.json" in report
    assert "mute button" in report
