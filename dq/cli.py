"""Command-line interface for the data-quality assistant."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .analyzer import analyze_records
from .loaders import load_records
from .output import write_output


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate explainable data-quality candidates for human review.")
    parser.add_argument("input", type=Path, help="Input .json or .csv file")
    parser.add_argument("-o", "--output", type=Path, help="Output JSON file")
    return parser.parse_args()


def main() -> int:
    args = parse_arguments()

    try:
        records = load_records(args.input)
        findings = analyze_records(records)
        write_output(findings, args.output)
        return 0
    except (ValueError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
