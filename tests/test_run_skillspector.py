from pathlib import Path

import yaml

from tools.run_skillspector import (
    _build_state,
    _exit_code,
    _invoke_graph,
    _merge_scoped_rules,
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
    next(item for item in statuses if item["analyzer_id"] == "meta_analyzer").update(
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
