"""Factual, repeatable validation checks."""

from __future__ import annotations

from typing import Any

from ..config import CORE_REQUIRED_FIELDS, SUPPORTED_UOMS
from ..models import ReviewCandidate
from ..utils import build_candidate, clean


def deterministic_checks(record: dict[str, Any]) -> list[ReviewCandidate]:
    """Run factual, repeatable validation checks."""
    findings: list[ReviewCandidate] = []

    missing_fields = sorted(field for field in CORE_REQUIRED_FIELDS if not clean(record.get(field)))

    if missing_fields:
        findings.append(
            build_candidate(
                record=record,
                issue_type="malformed_or_incomplete_row",
                severity="high" if "item_id" in missing_fields else "medium",
                confidence=1.0,
                explanation=("Required values are missing or blank: " f"{', '.join(missing_fields)}."),
                suggested_action=(
                    "Ask the source owner to complete the missing values and " "review the row before approval."
                ),
                source="deterministic_rule",
            )
        )

    manufacturer = clean(record.get("manufacturer"))
    part_number = clean(record.get("manufacturer_part_number"))

    if manufacturer and not part_number:
        findings.append(
            build_candidate(
                record=record,
                issue_type="missing_part_number",
                severity="medium",
                confidence=0.95,
                explanation=("Manufacturer is present, but manufacturer part number is missing."),
                suggested_action=("Request the manufacturer part number from the source owner."),
                source="deterministic_rule",
            )
        )

    unit_of_measure = clean(record.get("unit_of_measure")).upper()
    if unit_of_measure and unit_of_measure not in SUPPORTED_UOMS:
        findings.append(
            build_candidate(
                record=record,
                issue_type="unsupported_unit_of_measure",
                severity="medium",
                confidence=0.98,
                explanation=(f"Unit of measure '{unit_of_measure}' is not present in the " "configured allow-list."),
                suggested_action=("Verify the value against the approved unit-of-measure catalogue."),
                source="deterministic_rule",
            )
        )

    return findings
