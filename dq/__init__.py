"""Generate explainable data-quality candidates for human review."""

from __future__ import annotations

from .analyzer import analyze_records
from .loaders import load_records
from .models import ReviewCandidate
from .output import write_output

__all__ = ["ReviewCandidate", "analyze_records", "load_records", "write_output"]
