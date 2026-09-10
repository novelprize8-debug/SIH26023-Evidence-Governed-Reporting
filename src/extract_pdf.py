from pathlib import Path
from pypdf import PdfReader

PDF_PATH = Path("data/raw/coal_directory_2024_25.pdf")
OUTPUT_PATH = Path("data/processed/coal_directory_2024_25.txt")

reader = PdfReader(PDF_PATH)

print(f"Total pages: {len(reader.pages)}")

text_parts = []

for page_number, page in enumerate(reader.pages, start=1):
    text = page.extract_text() or ""
    text_parts.append(f"\n--- PAGE {page_number} ---\n{text}")

full_text = "\n".join(text_parts)

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH.write_text(full_text, encoding="utf-8")

print(f"Extracted characters: {len(full_text):,}")
print(f"Saved to: {OUTPUT_PATH}")