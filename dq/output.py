"""Write findings to stdout or a JSON file."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def write_output(findings: list[dict[str, Any]], output_path: Path | None) -> None:
    output = json.dumps(findings, indent=2, ensure_ascii=False)

    if output_path is None:
        print(output)
    else:
        output_path.write_text(output + "\n", encoding="utf-8")
