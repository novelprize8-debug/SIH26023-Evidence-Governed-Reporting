import fitz
import subprocess
from pathlib import Path

PDF_PATH = Path("data/raw/parliament_q3757_2023_24.pdf")
IMAGE_PATH = Path("data/processed/parliament_page2.png")
OCR_BASE = Path("data/processed/parliament_q3757_ocr")

TESSERACT = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")

doc = fitz.open(PDF_PATH)

print("Total pages:", len(doc))

page = doc[1]

print("Rendering page 2...")

pix = page.get_pixmap(
    matrix=fitz.Matrix(3, 3),
    alpha=False
)

IMAGE_PATH.parent.mkdir(parents=True, exist_ok=True)

pix.save(str(IMAGE_PATH))

print("Saved image:", IMAGE_PATH)
print("Image size:", pix.width, "x", pix.height)

print("Running Tesseract...")

result = subprocess.run(
    [
        str(TESSERACT),
        str(IMAGE_PATH),
        str(OCR_BASE),
        "--psm", "6"
    ],
    capture_output=True,
    text=True
)

print("Tesseract return code:", result.returncode)

if result.stderr:
    print("Tesseract messages:")
    print(result.stderr)

OCR_PATH = Path(str(OCR_BASE) + ".txt")

if OCR_PATH.exists():
    text = OCR_PATH.read_text(encoding="utf-8")

    print("\n========== OCR OUTPUT ==========\n")
    print(text)

    print("\nOCR saved to:", OCR_PATH)
else:
    print("OCR output file was not created.")