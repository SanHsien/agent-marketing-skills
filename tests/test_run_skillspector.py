import hashlib
from pathlib import Path

import pytest
import yaml

from tools.run_skillspector import (
    _build_state,
    _exit_code,
    _invoke_graph,
    _merge_scoped_rules,
    _reviewed_partials,
)


EXPECTED_ANALYZERS = {
    "artifact_integrity",
    "behavioral_ast",
    "behavioral_taint_tracking",
    "bundled_execution_surface",
    "mcp_least_privilege",
    "mcp_rug_pull",
    "mcp_tool_poisoning",
    "meta_analyzer",
    "static_patterns_agent_snooping",
    "static_patterns_anti_refusal",
    "static_patterns_data_exfiltration",
    "static_patterns_deserialization",
    "static_patterns_excessive_agency",
    "static_patterns_harmful_content",
    "static_patterns_memory_poisoning",
    "static_patterns_output_handling",
    "static_patterns_privilege_escalation",
    "static_patterns_prompt_injection",
    "static_patterns_rogue_agent",
    "static_patterns_ssrf",
    "static_patterns_supply_chain",
    "static_patterns_system_prompt_leakage",
    "static_patterns_tool_misuse",
    "static_yara",
    "semantic_developer_intent",
    "semantic_quality_policy",
    "semantic_security_discovery",
}
DISABLED_WITHOUT_LLM = {
    "meta_analyzer",
    "semantic_developer_intent",
    "semantic_quality_policy",
    "semantic_security_discovery",
}


class _FakeGraph:
    def __init__(self) -> None:
        self.calls = []

    def invoke(self, state, config=None):
        self.calls.append((state, config))
        return {"ok": True}


def test_graph_is_invoked_sequentially():
    graph = _FakeGraph()
    result = _invoke_graph(graph, {"input_path": "skill"})
    assert result == {"ok": True}
    assert graph.calls == [
        ({"input_path": "skill"}, {"max_concurrency": 1})
    ]


def test_scoped_rules_only_apply_to_the_current_skill():
    baseline = {
        "rules": [{"id": "GLOBAL", "reason": "global"}],
        "scoped_rules": [
            {
                "skill": "ads",
                "id": "MP3",
                "path": "references/meta-decision-system.md",
                "message": "*Swap rules*",
                "reason": "ads terminology",
            },
            {
                "skill": "events",
                "id": "E4",
                "path": "SKILL.md",
                "message": "*Capture context*",
                "reason": "event follow-up terminology",
            },
        ],
        "fingerprints": [],
    }

    merged = _merge_scoped_rules(baseline, "ads")

    assert "scoped_rules" not in merged
    assert merged["rules"] == [
        {"id": "GLOBAL", "reason": "global"},
        {
            "id": "MP3",
            "path": "references/meta-decision-system.md",
            "message": "*Swap rules*",
            "reason": "ads terminology",
        },
    ]


def test_reviewed_unstable_findings_have_exact_skill_scopes():
    baseline = yaml.safe_load(
        (Path(__file__).parents[1] / ".skillspector-baseline.yaml").read_text(
            encoding="utf-8"
        )
    )
    expected = {
        ("ad-creative", "RP1", "references/generative-tools.md", None),
        ("ads", "MP3", "references/meta-decision-system.md", "*Swap rules*"),
        ("ai-seo", "RP1", "SKILL.md", None),
        ("ai-seo", "RP1", "evals/evals.json", None),
        ("directory-submissions", "RA2", "references/directory-list.md", "*plist*"),
        ("events", "E4", "SKILL.md", "*Capture context*"),
        ("marketing-loops", "EA4", "evals/evals.json", "*loop forever*"),
        ("revops", "RA2", "references/automation-playbooks.md", "*Create task for*"),
    }
    actual = {
        (rule["skill"], rule["id"], rule["path"], rule.get("message"))
        for rule in baseline.get("scoped_rules", [])
    }

    assert actual == expected
    assert all(rule.get("reason", "").strip() for rule in baseline["scoped_rules"])


def _completed_analyzer(analyzer_id):
    return {
        "analyzer_id": analyzer_id,
        "status": "completed",
        "planned_work": 1,
        "completed": 1,
        "partial": 0,
        "skipped": 0,
        "failed": 0,
        "unaccounted": 0,
    }


def _complete_report(*, issues=None):
    statuses = [_completed_analyzer(item) for item in sorted(EXPECTED_ANALYZERS)]
    for item in statuses:
        if item["analyzer_id"] in DISABLED_WITHOUT_LLM:
            item.update(
                status="disabled",
                planned_work=0,
                completed=0,
                reason_code="disabled_by_configuration",
            )
    return {
        "execution_successful": True,
        "issues": [] if issues is None else issues,
        "analysis_completeness": {
            "total_components": 1,
            "scanned_components": 1,
            "coverage_percent": 100.0,
            "is_complete": True,
            "status": "complete",
            "execution_successful": True,
            "fully_inspected_files": 1,
            "partially_inspected_files": 0,
            "entirely_uninspected_files": 0,
            "ledger_exceptions": [],
            "scope_exclusions": [],
            "analyzer_statuses": statuses,
            "references": [],
        },
    }


def test_build_state_injects_workflow_budget():
    calls = {}

    def scan_state(
        input_path, output_format, no_llm, baseline=None, show_suppressed=False
    ):
        calls["scan_state"] = (
            input_path,
            output_format,
            no_llm,
            baseline,
            show_suppressed,
        )
        return {"input_path": input_path}

    def budget_factory(*, max_seconds):
        calls["budget"] = max_seconds
        return {"max_seconds": max_seconds}

    state = _build_state(
        scan_state,
        budget_factory,
        input_path="skill",
        output_format="json",
        baseline="baseline.yaml",
        max_workflow_seconds=300,
    )

    assert calls == {
        "scan_state": ("skill", "json", True, "baseline.yaml", True),
        "budget": 300,
    }
    assert state["workflow_resource_budget"] == {"max_seconds": 300}


def test_exit_code_fails_closed_on_incomplete_scan():
    assert _exit_code({"execution_successful": False, "issues": []}) == 2


def test_exit_code_fails_closed_on_degraded_analyzer():
    report = _complete_report()
    report["analysis_completeness"]["analyzer_statuses"][-2].update(
        status="degraded", completed=1, partial=1
    )
    assert _exit_code(report) == 2


def test_exit_code_fails_closed_on_unexpected_disabled_analyzer():
    report = _complete_report()
    report["analysis_completeness"]["analyzer_statuses"][-2].update(
        status="disabled", planned_work=0, completed=0
    )
    assert _exit_code(report) == 2


def test_exit_code_fails_closed_on_semantic_analyzer_that_ran_without_llm():
    report = _complete_report()
    row = next(
        item
        for item in report["analysis_completeness"]["analyzer_statuses"]
        if item["analyzer_id"] == "semantic_security_discovery"
    )
    row.update(status="completed", planned_work=1, completed=1)
    row.pop("reason_code")
    assert _exit_code(report) == 2


def test_exit_code_fails_closed_on_missing_semantic_analyzer_row():
    report = _complete_report()
    statuses = report["analysis_completeness"]["analyzer_statuses"]
    report["analysis_completeness"]["analyzer_statuses"] = [
        item for item in statuses if item["analyzer_id"] != "semantic_quality_policy"
    ]
    assert _exit_code(report) == 2


def test_exit_code_fails_closed_on_missing_expected_analyzer():
    report = _complete_report()
    report["analysis_completeness"]["analyzer_statuses"].pop()
    assert _exit_code(report) == 2


def test_exit_code_fails_closed_on_unaccounted_partial_completeness():
    report = _complete_report()
    report["analysis_completeness"].update(status="partial", is_complete=False)
    assert _exit_code(report) == 2


def test_exit_code_fails_closed_on_partial_reference_in_complete_report():
    report = _complete_report()
    report["analysis_completeness"]["references"] = [
        {
            "source_path": "SKILL.md",
            "line": 12,
            "target_path": None,
            "status": "missing",
            "disposition": "partial",
        }
    ]
    assert _exit_code(report) == 2


def test_exit_code_accepts_accounted_nonfatal_unresolved_reference():
    report = _complete_report()
    report["analysis_completeness"].update(
        status="partial",
        is_complete=False,
        ledger_exceptions=[
            {
                "outcome": "partial",
                "phase": "reference_resolution",
                "reason_code": "reference_unresolved",
                "path": "SKILL.md",
                "start_line": 12,
                "end_line": 12,
                "fatal": False,
            }
        ],
        references=[
            {
                "source_path": "SKILL.md",
                "line": 12,
                "target_path": None,
                "status": "missing",
                "disposition": "partial",
            },
            {
                "source_path": "SKILL.md",
                "line": 12,
                "target_path": None,
                "status": "missing",
                "disposition": "partial",
            },
        ],
    )
    assert _exit_code(report) == 0


def test_exit_code_fails_closed_on_unmatched_unresolved_reference():
    report = _complete_report()
    report["analysis_completeness"].update(
        status="partial",
        is_complete=False,
        ledger_exceptions=[
            {
                "outcome": "partial",
                "phase": "reference_resolution",
                "reason_code": "reference_unresolved",
                "path": "SKILL.md",
                "start_line": 12,
                "end_line": 12,
                "fatal": False,
            }
        ],
    )
    assert _exit_code(report) == 2


def test_exit_code_distinguishes_findings_from_clean_scan():
    assert _exit_code(_complete_report(issues=[{}])) == 1
    assert _exit_code(_complete_report()) == 0


def test_exit_code_accepts_explicit_binary_scope_exclusion():
    report = _complete_report()
    report["analysis_completeness"]["scope_exclusions"] = [
        {
            "outcome": "out_of_scope",
            "reason_code": "binary_content",
            "path": "assets/example.png",
            "analyzers": ["static_patterns_tool_misuse"],
        }
    ]
    analyzer = next(
        item
        for item in report["analysis_completeness"]["analyzer_statuses"]
        if item["analyzer_id"] == "static_patterns_tool_misuse"
    )
    analyzer.update(planned_work=2, completed=1, failed=1)
    assert _exit_code(report) == 0


# ── Reviewed static parse limits ──────────────────────────────────────────────
#
# A bounded static parser can stop inside one oversized expression. The scanner then
# reports that analyzer as degraded and the file as partially inspected, which this
# gate treats as incomplete. A maintainer may review that file by hand and record a
# reviewed partial; the exemption is pinned to the file's SHA-256, so any edit to the
# file reopens it.

PARTIAL_PATH = "assets/review.html"
PARTIAL_ANALYZER = "static_patterns_tool_misuse"
REVIEWED = frozenset({(PARTIAL_PATH, PARTIAL_ANALYZER, "static_parse_limit")})


def _report_with_static_partial(*, analyzer=PARTIAL_ANALYZER, path=PARTIAL_PATH):
    report = _complete_report()
    completeness = report["analysis_completeness"]
    completeness.update(
        total_components=2,
        scanned_components=1,
        fully_inspected_files=1,
        partially_inspected_files=1,
        coverage_percent=50.0,
        is_complete=False,
        status="partial",
        limitations=[f"Analyzer {analyzer} status: degraded."],
        ledger_exceptions=[
            {
                "outcome": "partial",
                "phase": "static",
                "reason_code": "static_parse_limit",
                "path": path,
                "start_line": None,
                "end_line": None,
                "fatal": False,
                "analyzers": [analyzer],
            }
        ],
    )
    row = next(
        item for item in completeness["analyzer_statuses"] if item["analyzer_id"] == analyzer
    )
    row.update(status="degraded", planned_work=2, completed=1, partial=1)
    return report


def test_exit_code_fails_closed_on_unreviewed_static_parse_limit():
    assert _exit_code(_report_with_static_partial()) == 2


def test_exit_code_accepts_reviewed_static_parse_limit():
    assert _exit_code(_report_with_static_partial(), REVIEWED) == 0


def test_reviewed_static_parse_limit_does_not_hide_findings():
    report = _report_with_static_partial()
    report["issues"] = [{}]
    assert _exit_code(report, REVIEWED) == 1


def test_reviewed_partial_for_another_analyzer_does_not_apply():
    report = _report_with_static_partial(analyzer="static_patterns_prompt_injection")
    assert _exit_code(report, REVIEWED) == 2


def test_reviewed_partial_for_another_file_does_not_apply():
    report = _report_with_static_partial(path="assets/other.html")
    assert _exit_code(report, REVIEWED) == 2


def test_reviewed_partial_still_requires_the_degraded_counts_to_add_up():
    report = _report_with_static_partial()
    row = next(
        item
        for item in report["analysis_completeness"]["analyzer_statuses"]
        if item["analyzer_id"] == PARTIAL_ANALYZER
    )
    row.update(skipped=1)
    assert _exit_code(report, REVIEWED) == 2


def test_reviewed_partial_rejects_unexplained_limitations():
    report = _report_with_static_partial()
    report["analysis_completeness"]["limitations"].append("Something else went wrong.")
    assert _exit_code(report, REVIEWED) == 2


def _baseline_with_partial(sha256, *, skill="demo"):
    return {
        "version": 2,
        "reviewed_partials": [
            {
                "skill": skill,
                "path": PARTIAL_PATH,
                "analyzer": PARTIAL_ANALYZER,
                "reason_code": "static_parse_limit",
                "sha256": sha256,
                "reason": "Reviewed by hand: renders embedded JSON only.",
            }
        ],
    }


def test_reviewed_partials_bind_to_the_file_content(tmp_path):
    skill = tmp_path / "demo"
    (skill / "assets").mkdir(parents=True)
    target = skill / PARTIAL_PATH
    target.write_bytes(b"<html>reviewed</html>")
    digest = hashlib.sha256(target.read_bytes()).hexdigest()

    assert _reviewed_partials(_baseline_with_partial(digest), skill) == REVIEWED

    target.write_bytes(b"<html>edited after review</html>")
    assert _reviewed_partials(_baseline_with_partial(digest), skill) == frozenset()


def test_reviewed_partials_only_apply_to_their_skill(tmp_path):
    skill = tmp_path / "demo"
    (skill / "assets").mkdir(parents=True)
    (skill / PARTIAL_PATH).write_bytes(b"x")
    digest = hashlib.sha256(b"x").hexdigest()
    assert _reviewed_partials(_baseline_with_partial(digest, skill="other"), skill) == frozenset()


def test_reviewed_partials_require_a_reason(tmp_path):
    baseline = _baseline_with_partial("0" * 64)
    baseline["reviewed_partials"][0]["reason"] = "  "
    with pytest.raises(ValueError):
        _reviewed_partials(baseline, tmp_path / "demo")


def test_reviewed_partials_never_reach_the_scanner():
    merged = _merge_scoped_rules(_baseline_with_partial("0" * 64), "demo")
    assert "reviewed_partials" not in merged


def test_reviewed_partial_explains_only_its_own_partial_unit():
    report = _report_with_static_partial()
    row = next(
        item
        for item in report["analysis_completeness"]["analyzer_statuses"]
        if item["analyzer_id"] == PARTIAL_ANALYZER
    )
    row.update(planned_work=3, completed=1, partial=2)
    assert _exit_code(report, REVIEWED) == 2

def test_reviewed_partial_accepts_the_reference_coverage_row_it_causes():
    report = _report_with_static_partial()
    report["analysis_completeness"]["analyzer_statuses"].append(
        _completed_analyzer("reference_coverage")
    )
    assert _exit_code(report, REVIEWED) == 0


def test_reference_coverage_row_without_a_reviewed_partial_fails_closed():
    report = _complete_report()
    report["analysis_completeness"]["analyzer_statuses"].append(
        _completed_analyzer("reference_coverage")
    )
    assert _exit_code(report) == 2


def test_reviewed_partial_can_list_several_analyzers(tmp_path):
    skill = tmp_path / "demo"
    (skill / "assets").mkdir(parents=True)
    (skill / PARTIAL_PATH).write_bytes(b"x")
    baseline = _baseline_with_partial(hashlib.sha256(b"x").hexdigest())
    entry = baseline["reviewed_partials"][0]
    del entry["analyzer"]
    entry["analyzers"] = [PARTIAL_ANALYZER, "static_patterns_ssrf"]
    entry["reason_code"] = "obfuscated_instruction_text"
    assert _reviewed_partials(baseline, skill) == frozenset(
        {
            (PARTIAL_PATH, PARTIAL_ANALYZER, "obfuscated_instruction_text"),
            (PARTIAL_PATH, "static_patterns_ssrf", "obfuscated_instruction_text"),
        }
    )


def test_reviewed_partial_rejects_an_empty_analyzer_list(tmp_path):
    baseline = _baseline_with_partial("0" * 64)
    entry = baseline["reviewed_partials"][0]
    del entry["analyzer"]
    entry["analyzers"] = []
    with pytest.raises(ValueError):
        _reviewed_partials(baseline, tmp_path / "demo")


def test_exit_code_accepts_accounted_nonfatal_missing_reference():
    report = _complete_report()
    report["analysis_completeness"].update(
        status="partial",
        is_complete=False,
        ledger_exceptions=[
            {
                "outcome": "partial",
                "phase": "reference_resolution",
                "reason_code": "reference_missing",
                "path": "SKILL.md",
                "start_line": 12,
                "end_line": 12,
                "fatal": False,
            }
        ],
        references=[
            {
                "source_path": "SKILL.md",
                "line": 12,
                "target_path": None,
                "status": "missing",
                "disposition": "partial",
            },
            {
                "source_path": "SKILL.md",
                "line": 12,
                "target_path": None,
                "status": "missing",
                "disposition": "partial",
            },
        ],
    )
    assert _exit_code(report) == 0


def test_exit_code_rejects_unknown_reference_reason():
    report = _complete_report()
    report["analysis_completeness"].update(
        status="partial",
        is_complete=False,
        ledger_exceptions=[
            {
                "outcome": "partial",
                "phase": "reference_resolution",
                "reason_code": "reference_bogus",
                "path": "SKILL.md",
                "start_line": 12,
                "end_line": 12,
                "fatal": False,
            }
        ],
        references=[
            {
                "source_path": "SKILL.md",
                "line": 12,
                "target_path": None,
                "status": "missing",
                "disposition": "partial",
            },
            {
                "source_path": "SKILL.md",
                "line": 12,
                "target_path": None,
                "status": "missing",
                "disposition": "partial",
            },
        ],
    )
    assert _exit_code(report) == 2


def test_exit_code_accepts_explicit_binary_scope_exclusion_counted_as_completed():
    report = _complete_report()
    report["analysis_completeness"]["scope_exclusions"] = [
        {
            "outcome": "out_of_scope",
            "reason_code": "binary_content",
            "path": "assets/example.png",
            "analyzers": ["static_patterns_tool_misuse"],
        }
    ]
    analyzer = next(
        item
        for item in report["analysis_completeness"]["analyzer_statuses"]
        if item["analyzer_id"] == "static_patterns_tool_misuse"
    )
    analyzer.update(planned_work=2, completed=2, failed=0)
    assert _exit_code(report) == 0


# ── Reviewed static parse limits ──────────────────────────────────────────────
#
# A bounded static parser can stop inside one oversized expression. The scanner then
# reports that analyzer as degraded and the file as partially inspected, which this
# gate treats as incomplete. A maintainer may review that file by hand and record a
# reviewed partial; the exemption is pinned to the file's SHA-256, so any edit to the
# file reopens it.

PARTIAL_PATH = "assets/review.html"
PARTIAL_ANALYZER = "static_patterns_tool_misuse"
REVIEWED = frozenset({(PARTIAL_PATH, PARTIAL_ANALYZER, "static_parse_limit")})
