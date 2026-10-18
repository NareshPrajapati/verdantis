"""Load JSON and CSV input files into records."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


def load_json_records(path: Path) -> list[Any]:
    """Load records from a JSON file."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except UnicodeDecodeError as error:
        raise ValueError("The JSON file must use UTF-8 encoding.") from error
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON at line {error.lineno}, column {error.colno}: " f"{error.msg}") from error

    if not isinstance(data, list):
        raise ValueError("JSON input must contain a list of records.")

    return data


def load_csv_records(path: Path) -> list[dict[str, Any]]:
    """Load records from a CSV file."""
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)
            if reader.fieldnames is None:
                raise ValueError("CSV input must contain a header row.")
            return list(reader)
    except UnicodeDecodeError as error:
        raise ValueError("The CSV file must use UTF-8 encoding.") from error
    except csv.Error as error:
        raise ValueError(f"Invalid CSV input: {error}") from error


def load_records(path: Path) -> list[Any]:
    """Load records from a JSON or CSV file based on the file extension."""
    if not path.exists():
        raise ValueError(f"Input file does not exist: {path}")
    if not path.is_file():
        raise ValueError(f"Input path is not a file: {path}")

    if path.suffix.lower() == ".json":
        return load_json_records(path)
    if path.suffix.lower() == ".csv":
        return load_csv_records(path)

    raise ValueError("Unsupported input format. Use a .json or .csv file.")
