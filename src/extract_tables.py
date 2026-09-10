from pathlib import Path
import json
import pdfplumber

PDF_PATH = Path("data/raw/coal_directory_2024_25.pdf")
OUTPUT_PATH = Path("data/processed/production_tables.json")

TARGET_PAGES = [87, 88, 92]

results = []

with pdfplumber.open(PDF_PATH) as pdf:
    for page_number in TARGET_PAGES:
        page = pdf.pages[page_number - 1]
        tables = page.extract_tables()

        for table_number, table in enumerate(tables, start=1):
            results.append(
                {
                    "source_document": PDF_PATH.name,
                    "page": page_number,
                    "table_number": table_number,
                    "rows": table,
                }
            )

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

OUTPUT_PATH.write_text(
    json.dumps(results, indent=2, ensure_ascii=False),
    encoding="utf-8",
)

print(f"Pages processed: {TARGET_PAGES}")
print(f"Tables extracted: {len(results)}")
print(f"Saved to: {OUTPUT_PATH}")