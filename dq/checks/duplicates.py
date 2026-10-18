"""Cross-record checks for duplicate item IDs and business keys."""

from __future__ import annotations

from typing import Any

from ..models import ReviewCandidate
from ..utils import build_candidate, clean, normalized_token


def duplicate_checks(
    records: list[dict[str, Any]],
) -> list[ReviewCandidate]:
    """Detect duplicate item IDs and matching manufacturer-part-number pairs."""
    findings: list[ReviewCandidate] = []
    seen_item_ids: dict[str, str] = {}
    seen_business_keys: dict[tuple[str, str], str] = {}

    for record in records:
        item_id = clean(record.get("item_id"))
        item_key = normalized_token(item_id)

        if item_key:
            previous_item_id = seen_item_ids.get(item_key)
            if previous_item_id:
                findings.append(
                    build_candidate(
                        record=record,
                        issue_type="duplicate_item_id",
                        severity="high",
                        confidence=1.0,
                        explanation=("Item ID matches another uploaded row with item ID " f"'{previous_item_id}'."),
                        suggested_action=(
                            "Investigate both rows and retain, merge, or reject " "them only after human review."
                        ),
                        source="deterministic_rule",
                        related_item_ids=(previous_item_id,),
                    )
                )
            else:
                seen_item_ids[item_key] = item_id

        manufacturer_key = normalized_token(record.get("manufacturer"))
        part_number_key = normalized_token(record.get("manufacturer_part_number"))

        if manufacturer_key and part_number_key:
            business_key = (manufacturer_key, part_number_key)
            previous_item_id = seen_business_keys.get(business_key)

            if previous_item_id:
                findings.append(
                    build_candidate(
                        record=record,
                        issue_type="potential_duplicate",
                        severity="medium",
                        confidence=0.92,
                        explanation=(
                            "Manufacturer and normalized manufacturer part number " "match another uploaded item."
                        ),
                        suggested_action=(
                            "Compare the candidate records and determine whether " "they represent the same item."
                        ),
                        source="deterministic_rule",
                        related_item_ids=(previous_item_id,),
                    )
                )
            else:
                seen_business_keys[business_key] = item_id or "<missing>"

    return findings
