"""AI-assisted stub for formatting-only description suggestions."""

from __future__ import annotations

from typing import Any

from ..models import ReviewCandidate
from ..utils import build_candidate


def normalized_description_suggestion(
    record: dict[str, Any],
) -> list[ReviewCandidate]:
    """Simulate an AI-assisted, formatting-only description suggestion."""
    raw_description = record.get("item_description")

    if not isinstance(raw_description, str) or not raw_description.strip():
        return []

    suggested_description = " ".join(raw_description.split())

    if suggested_description == raw_description:
        return []

    return [
        build_candidate(
            record=record,
            issue_type="normalized_description_suggestion",
            severity="low",
            confidence=0.90,
            explanation=("A formatting-only description suggestion is available: " f"'{suggested_description}'."),
            suggested_action=("Compare the suggested description with the source record and " "approve or reject it."),
            source="ai_assisted_stub",
        )
    ]
