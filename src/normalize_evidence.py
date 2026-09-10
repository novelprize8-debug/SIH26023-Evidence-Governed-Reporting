from pathlib import Path
import json
import uuid

INPUT_PATH = Path("data/processed/production_tables.json")
OUTPUT_PATH = Path("data/processed/evidence.jsonl")

COLUMN_MAP = {
    3: ("2022-23", "Coking"),
    4: ("2022-23", "Non-Coking"),
    5: ("2022-23", "Total"),
    6: ("2023-24", "Coking"),
    7: ("2023-24", "Non-Coking"),
    8: ("2023-24", "Total"),
    9: ("2024-25", "Coking"),
    10: ("2024-25", "Non-Coking"),
    11: ("2024-25", "Total"),
}


def clean_value(value):
    if value is None:
        return None

    value = str(value).replace("\n", " ").strip()

    if not value:
        return None

    try:
        return float(value)
    except ValueError:
        return None


data = json.loads(INPUT_PATH.read_text(encoding="utf-8"))

evidence_records = []

table = next(item for item in data if item["page"] == 88)

current_state = None

for row in table["rows"][4:]:
    if not row or len(row) < 11:
        continue

    state = row[0].strip() if row[0] else None
    company = row[1].strip() if row[1] else None

    if state:
        current_state = state

    if not company:
        continue

    for column_number, (period, metric_type) in COLUMN_MAP.items():
        value = clean_value(row[column_number - 1])

        if value is None:
            continue

        evidence_records.append(
            {
                "evidence_id": str(uuid.uuid4()),
                "entity": company,
                "metric": "Raw Coal Production",
                "value": value,
                "unit": "Million Tonnes",
                "period": period,
                "mining_method": None,
                "coal_type": metric_type,
                "status": "reported",
                "source_document": "coal_directory_2024_25.pdf",
                "source_publisher": "Ministry of Coal",
                "page": 88,
                "table": "Table 3.12",
                "source_location": "PDF page 88, Table 3.12",
                "extraction_method": "pdfplumber",
                "notes": f"State: {current_state}",
            }
        )

with OUTPUT_PATH.open("w", encoding="utf-8") as f:
    for record in evidence_records:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

print(f"Evidence records created: {len(evidence_records)}")
print(f"Saved to: {OUTPUT_PATH}")