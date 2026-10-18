# Agentic Coding Lead Assignment - Data Quality Slice

## What this solution demonstrates

A deliberately small Python solution that creates **review candidates**, never automatic corrections. It implements:

1. Missing manufacturer part number
2. Weak/vague description
3. Duplicate item ID and normalized manufacturer/part-number duplicate
4. Category mismatch candidate
5. Unsupported unit of measure
6. Normalized description suggestion (AI-assisted stub)
7. Malformed/incomplete row
8. Severity, confidence, explanation, suggested action, and source on every finding

The boundaries are explicit:

- `deterministic_checks`: factual, repeatable validation
- `heuristic_checks`: lower-confidence review suggestions
- `ai_assisted_stub`: demonstrates where an LLM-backed adapter could later be added
- `duplicate_checks`: cross-record validation
- `analyze_records`: orchestration, with no mutation of source records

## Code layout

The logic lives in the `dq` package. `dq_assistant.py` is a thin entry point that keeps the CLI and the `from dq_assistant import analyze_records` import path working.

```text
dq_assistant.py        CLI entry point (re-exports the public API)
dq/
  config.py            required fields, UOM allow-list, keywords
  models.py            ReviewCandidate dataclass
  utils.py             clean / normalize / build_candidate helpers
  loaders.py           JSON and CSV input loading
  output.py            JSON output writer
  analyzer.py          analyze_records orchestration
  cli.py               argument parsing and main()
  checks/
    deterministic.py   factual, repeatable checks
    heuristic.py       lower-confidence review suggestions
    suggestions.py     AI-assisted formatting stub
    duplicates.py      cross-record duplicate checks
```

## Run

Requires Python 3.10+ and no third-party packages.

```bash
python dq_assistant.py sample_input.json
python dq_assistant.py sample_input.json -o sample_output.json
```

CSV is also supported:

```bash
python dq_assistant.py input.csv -o findings.json
```

## Test

```bash
python -m unittest -v
```

## Assumptions

- JSON input is a list; CSV headers map to the documented field names.
- The UOM allow-list and category keywords are demonstration configuration, not enterprise master data.
- Part numbers are compared case-insensitively after punctuation/space removal.
- Heuristic suggestions use lower confidence and must be reviewed.
- All findings are candidates. No input record is changed.

## One-hour tradeoffs

Included: clear boundaries, seven checks, CLI, JSON/CSV input, malformed input handling, non-mutation, tests, and explainable output.

Deferred: REST API/UI, persistent review decisions, fuzzy/vector duplicate matching, multilingual models, enterprise UOM/category reference data, authentication, authorization, telemetry, and a real LLM integration.

## Safe real-LLM extension

Introduce an `AISuggestionProvider` interface used only after deterministic checks. Send only approved/minimized fields, require schema-constrained JSON, validate issue type/confidence/explanation, apply timeout/retry/rate limits, record model/prompt versions, and label every result `ai_assisted_candidate`. Never let the model write to production. A human must approve/reject/investigate the candidate.

## What I delegated to AI and what I verified

**Delegated:** first-pass scaffolding, edge-case suggestions, and repetitive test drafting.

**Personally verified:** product language remains advisory; original data is not mutated; deterministic and heuristic findings are separated; null/blank handling; duplicate normalization; CLI behavior; and all unit tests.

**Rejected/avoided:** unnecessary web framework, database, autonomous agents, and a real LLM call because they increase risk and do not improve the requested working slice.
