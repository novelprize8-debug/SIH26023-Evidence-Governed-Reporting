import json
from pathlib import Path

EVIDENCE_PATH = Path("data/processed/evidence.jsonl")

SOURCE_DOCUMENT = "Lok Sabha Unstarred Question No. 3757 - Ministry of Coal"
SOURCE_PUBLISHER = "Lok Sabha / Ministry of Coal"

records = [
    {
        "evidence_id": "PAR-Q3757-MCL-NC-OC-2023-24",
        "entity": "MCL",
        "metric": "Raw Coal Production",
        "value": 205.643,
        "unit": "Million Tonnes",
        "period": "2023-24",
        "mining_method": "OC",
        "coal_type": "Non-Coking",
        "status": "reported",
        "source_document": SOURCE_DOCUMENT,
        "source_publisher": SOURCE_PUBLISHER,
        "publication_date": "2024-12-18",
        "version": "reported",
        "page": 2,
        "table": "Annexure A",
        "source_location": "MCL Non-Coking Coal - Open Cast Mines",
        "extraction_method": "source_verified_manual",
        "notes": "Value verified from the official Parliamentary answer."
    },
    {
        "evidence_id": "PAR-Q3757-MCL-NC-UG-2023-24",
        "entity": "MCL",
        "metric": "Raw Coal Production",
        "value": 0.456,
        "unit": "Million Tonnes",
        "period": "2023-24",
        "mining_method": "UG",
        "coal_type": "Non-Coking",
        "status": "reported",
        "source_document": SOURCE_DOCUMENT,
        "source_publisher": SOURCE_PUBLISHER,
        "publication_date": "2024-12-18",
        "version": "reported",
        "page": 2,
        "table": "Annexure A",
        "source_location": "MCL Non-Coking Coal - Underground Mines",
        "extraction_method": "source_verified_manual",
        "notes": "Value verified from the official Parliamentary answer."
    },
    {
        "evidence_id": "PAR-Q3757-MCL-NC-TOTAL-2023-24",
        "entity": "MCL",
        "metric": "Raw Coal Production",
        "value": 206.099,
        "unit": "Million Tonnes",
        "period": "2023-24",
        "mining_method": None,
        "coal_type": "Non-Coking",
        "status": "derived",
        "source_document": SOURCE_DOCUMENT,
        "source_publisher": SOURCE_PUBLISHER,
        "publication_date": "2024-12-18",
        "version": "derived",
        "page": 2,
        "table": "Annexure A",
        "source_location": "MCL Non-Coking Coal - Open Cast + Underground",
        "extraction_method": "deterministic_sum",
        "notes": "Derived as 205.643 + 0.456. The total is not treated as directly printed in the Parliamentary source."
    }
]

# Load existing evidence IDs
existing_ids = set()

if EVIDENCE_PATH.exists():
    with open(EVIDENCE_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    existing_ids.add(json.loads(line)["evidence_id"])
                except Exception:
                    pass

added = 0

with open(EVIDENCE_PATH, "a", encoding="utf-8") as f:
    for record in records:
        if record["evidence_id"] not in existing_ids:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
            added += 1

print("Parliament evidence records added:", added)
print("Total evidence IDs now:", len(existing_ids) + added)