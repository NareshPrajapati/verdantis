"""Lower-confidence checks that require human review."""

from __future__ import annotations

from typing import Any

from ..config import CATEGORY_KEYWORDS, VAGUE_DESCRIPTIONS
from ..models import ReviewCandidate
from ..utils import build_candidate, clean, extract_words
from .suggestions import normalized_description_suggestion


def heuristic_checks(record: dict[str, Any]) -> list[ReviewCandidate]:
    """Run lower-confidence checks that require human review."""
    findings: list[ReviewCandidate] = []

    description = clean(record.get("item_description"))
    description_words = extract_words(description)

    if description and (description.lower() in VAGUE_DESCRIPTIONS or len(description_words) < 2):
        findings.append(
            build_candidate(
                record=record,
                issue_type="weak_description_candidate",
                severity="low",
                confidence=0.80,
                explanation=(
                    "The description is very short or uses a generic item term " "without distinguishing attributes."
                ),
                suggested_action=("Consider adding attributes such as type, size, material, " "model, or rating."),
                source="heuristic_candidate",
            )
        )

    category = clean(record.get("category")).lower()
    if description and category:
        for expected_category, keywords in CATEGORY_KEYWORDS.items():
            matched_keywords = sorted(description_words & keywords)

            if matched_keywords and category != expected_category:
                findings.append(
                    build_candidate(
                        record=record,
                        issue_type="category_mismatch_candidate",
                        severity="low",
                        confidence=0.70,
                        explanation=(
                            f"Description contains {', '.join(matched_keywords)}, "
                            f"commonly associated with '{expected_category}', while "
                            f"the recorded category is '{category}'."
                        ),
                        suggested_action=("Review the category assignment before approval."),
                        source="heuristic_candidate",
                    )
                )
                break

    findings.extend(normalized_description_suggestion(record))
    return findings
