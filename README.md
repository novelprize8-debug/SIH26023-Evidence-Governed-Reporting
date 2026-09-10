# SIH 26023 — Evidence-Governed Reporting Intelligence

A local MVP for controlled coal-production reporting for CMPDI/CIL. It answers only from the supplied verified evidence corpus; it does not use an LLM to create facts.

## Exact commands

```powershell
.\.venv\Scripts\python.exe -m src.app
```

Open `http://127.0.0.1:8000`.

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

## Evidence controls

The system parses a question, retrieves `data/processed/evidence.jsonl`, displays the source/page/table/evidence ID/extraction method for every number, and performs calculations with Python `Decimal`. Parliament OC + UG totals are always visibly **DERIVED**, with their input evidence IDs; they are never represented as directly reported. It exposes rather than suppresses disagreement, and returns `insufficient_evidence` or `needs_clarification` when necessary.

## Demonstration

Ask `How much raw coal did MCL produce in 2023-24?` The directly reported Coal Directory answer is **206.099 Million Tonnes**. The UI additionally displays **DERIVED — 205.643 + 0.456 = 206.099 Million Tonnes** from Lok Sabha Q3757 and a cross-source consistency result for the comparable non-coking scope.

## Limitations

The parser deliberately supports the seeded MCL production corpus and aliases configured in `src/query_parser.py`. This is local-only: no authentication, uploads, OCR workflow, roles, or external document refresh. New evidence must be verified before ingestion.
