"""Data structures for review findings."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class ReviewCandidate:
    item_id: str
    issue_type: str
    severity: str
    confidence: float
    explanation: str
    suggested_action: str
    source: str
    related_item_ids: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Convert the review candidate to a dictionary, with related_item_ids as a list."""
        result = asdict(self)
        result["related_item_ids"] = list(self.related_item_ids)
        return result
