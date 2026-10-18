"""Shared helpers for normalizing values and building findings."""

from __future__ import annotations

import re
from typing import Any

from .models import ReviewCandidate


def clean(value: Any) -> str:
    """Convert null or scalar values to trimmed text."""
    return "" if value is None else str(value).strip()


def normalized_token(value: Any) -> str:
    """Normalize an identifier for comparison without changing source data."""
    return re.sub(r"[^A-Z0-9]", "", clean(value).upper())


def extract_words(value: Any) -> set[str]:
    """Extract lowercase words for simple heuristic matching."""
    return set(re.findall(r"[a-z0-9]+", clean(value).lower()))


def build_candidate(
    record: dict[str, Any],
    issue_type: str,
    severity: str,
    confidence: float,
    explanation: str,
    suggested_action: str,
    source: str,
    related_item_ids: tuple[str, ...] = (),
) -> ReviewCandidate:
    """Build a review candidate from a record and issue details."""
    return ReviewCandidate(
        item_id=clean(record.get("item_id")) or "<missing>",
        issue_type=issue_type,
        severity=severity,
        confidence=confidence,
        explanation=explanation,
        suggested_action=suggested_action,
        source=source,
        related_item_ids=related_item_ids,
    )
