"""Orchestrate all checks over input records."""

from __future__ import annotations

from typing import Any, Iterable

from .checks import deterministic_checks, duplicate_checks, heuristic_checks
from .models import ReviewCandidate
from .utils import build_candidate


def analyze_records(records: Iterable[Any]) -> list[dict[str, Any]]:
    """Return structured findings without mutating input records."""
    valid_records: list[dict[str, Any]] = []
    findings: list[ReviewCandidate] = []

    for row_number, value in enumerate(records, start=1):
        if not isinstance(value, dict):
            findings.append(
                build_candidate(
                    record={"item_id": f"<row:{row_number}>"},
                    issue_type="malformed_row",
                    severity="high",
                    confidence=1.0,
                    explanation=(f"Row {row_number} is not a JSON object or tabular record."),
                    suggested_action=("Fix the input structure and upload the row again."),
                    source="deterministic_rule",
                )
            )
            continue

        record = dict(value)
        valid_records.append(record)
        findings.extend(deterministic_checks(record))
        findings.extend(heuristic_checks(record))

    findings.extend(duplicate_checks(valid_records))
    return [finding.to_dict() for finding in findings]
