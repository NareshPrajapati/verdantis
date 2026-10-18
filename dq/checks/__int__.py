"""Individual data-quality check groups."""

from __future__ import annotations

from .deterministic import deterministic_checks
from .duplicates import duplicate_checks
from .heuristic import heuristic_checks
from .suggestions import normalized_description_suggestion

__all__ = [
    "deterministic_checks",
    "duplicate_checks",
    "heuristic_checks",
    "normalized_description_suggestion",
]
