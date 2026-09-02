import os
import json
import io
import time

import pymupdf
import pytesseract
from PIL import Image
from google import genai
from google.genai import types


# -----------------------------
# Configuration
# -----------------------------

PDF_PATH = "invoice.pdf"
OUTPUT_PATH = "ocr_invoice_result.json"

TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
MODEL = "gemini-3.7-flash"


# -----------------------------
# Setup
# -----------------------------

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not loaded.")

client = genai.Client(api_key=api_key)


# -----------------------------
# Step 1: PDF → OCR text
# -----------------------------

print("Opening PDF...")

doc = pymupdf.open(PDF_PATH)

ocr_text = ""

for page_number, page in enumerate(doc, start=1):

    print(f"OCR processing page {page_number}...")

    # Render PDF page as image
    pix = page.get_pixmap(matrix=pymupdf.Matrix(2, 2))

    image = Image.open(
        io.BytesIO(pix.tobytes("png"))
    )

    # OCR
    text = pytesseract.image_to_string(image)

    ocr_text += f"\n--- Page {page_number} ---\n"
    ocr_text += text

doc.close()

print("OCR completed.")


# -----------------------------
# Step 2: OCR text → JSON
# -----------------------------

prompt = f"""
You are an invoice data extraction system.

Convert the following OCR text into structured JSON.

Return ONLY valid JSON.
Do not use markdown.
Do not add explanations.

Required JSON structure:

{{
    "vendor_name": null,
    "invoice_number": null,
    "invoice_date": null,
    "due_date": null,
    "customer_name": null,
    "line_items": [
        {{
            "description": null,
            "quantity": null,
            "unit_price": null,
            "amount": null
        }}
    ],
    "subtotal": null,
    "tax": null,
    "total": null
}}

Rules:
- Use null when information is missing.
- quantity should be a number.
- unit_price, amount, subtotal, tax and total should be numbers.
- Remove currency symbols such as $.
- Reconstruct line items carefully from the OCR text.
- Do not invent information.

OCR TEXT:
{ocr_text}
"""

print("Sending OCR text to Gemini...")

max_retries = 3
response = None

for attempt in range(max_retries):
    try:
        print(f"Gemini attempt {attempt + 1}/{max_retries}...")

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                automatic_function_calling=types.AutomaticFunctionCallingConfig(
                    disable=True
                )
            )
        )

        break

    except Exception as e:
        print(f"Gemini request failed: {e}")

        if attempt < max_retries - 1:
            print("Waiting 5 seconds before retry...")
            time.sleep(5)
        else:
            raise


# -----------------------------
# Step 3: Parse JSON
# -----------------------------

response_text = response.text.strip()

try:
    data = json.loads(response_text)

except json.JSONDecodeError:
    print("\nGemini returned invalid JSON:")
    print(response_text)
    raise


# -----------------------------
# Step 4: Save result
# -----------------------------

with open(
    OUTPUT_PATH,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        data,
        f,
        indent=4,
        ensure_ascii=False
    )


print("\n==============================")
print("OCR + GEMINI EXTRACTION DONE")
print("==============================")
print(f"Output file: {OUTPUT_PATH}")

print("\nExtracted JSON:")
print(
    json.dumps(
        data,
        indent=4,
        ensure_ascii=False
    )
)