"""Command-line entry point for the data-quality assistant.

The implementation lives in the ``dq`` package. This script keeps the
``python dq_assistant.py`` usage and the ``dq_assistant`` import path working.
"""

from __future__ import annotations

from dq import ReviewCandidate, analyze_records, load_records, write_output
from dq.cli import main

__all__ = ["ReviewCandidate", "analyze_records", "load_records", "write_output", "main"]


if __name__ == "__main__":
    raise SystemExit(main())
