import os
import json
import time
from pathlib import Path

import pymupdf
import pytesseract
from PIL import Image
from google import genai
from google.genai import types


# =================================================
# CONFIGURATION
# =================================================

TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

MODELS = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash"
]

MAX_RETRIES_PER_MODEL = 2


# =================================================
# GEMINI SETUP
# =================================================

def create_gemini_client():

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not loaded."
        )

    return genai.Client(
        api_key=api_key
    )


# =================================================
# PDF → OCR
# =================================================

def extract_ocr_text(pdf_path):

    pdf_path = Path(pdf_path)

    if not pdf_path.exists():

        raise FileNotFoundError(
            f"PDF file not found: {pdf_path}"
        )

    pytesseract.pytesseract.tesseract_cmd = (
        TESSERACT_PATH
    )

    print(f"Opening PDF: {pdf_path}")

    document = pymupdf.open(
        str(pdf_path)
    )

    all_text = []

    try:

        for page_number, page in enumerate(
            document,
            start=1
        ):

            print(
                f"OCR processing page "
                f"{page_number}..."
            )

            matrix = pymupdf.Matrix(
                2,
                2
            )

            pixmap = page.get_pixmap(
                matrix=matrix,
                alpha=False
            )

            image = Image.frombytes(
                "RGB",
                [
                    pixmap.width,
                    pixmap.height
                ],
                pixmap.samples
            )

            text = pytesseract.image_to_string(
                image
            )

            if text.strip():

                all_text.append(
                    f"--- PAGE {page_number} ---\n"
                    f"{text}"
                )

    finally:

        document.close()

    ocr_text = "\n\n".join(
        all_text
    )

    if not ocr_text.strip():

        raise RuntimeError(
            "OCR did not produce any text."
        )

    return ocr_text


# =================================================
# OCR → GEMINI → JSON
# =================================================

def extract_invoice_data(
    ocr_text,
    client
):

    prompt = f"""
You are an invoice data extraction system.

Extract structured information from the OCR text below.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "vendor_name": "",
    "invoice_number": "",
    "invoice_date": "",
    "due_date": "",
    "customer_name": "",
    "line_items": [
        {{
            "description": "",
            "quantity": 0,
            "unit_price": 0.0,
            "amount": 0.0
        }}
    ],
    "subtotal": 0.0,
    "tax": 0.0,
    "total": 0.0
}}

Rules:

1. Do not invent missing information.
2. If a field is unavailable, use an empty string.
3. Preserve invoice numbers exactly.
4. Extract every visible line item.
5. Quantity must be numeric.
6. Unit price must be numeric.
7. Amount must be numeric.
8. Subtotal, tax, and total must be numeric.
9. Do not include currency symbols inside numeric values.
10. Return JSON only.

OCR TEXT:

{ocr_text}
"""

    last_error = None

    for model in MODELS:

        print(
            f"Trying Gemini model: {model}"
        )

        for attempt in range(
            1,
            MAX_RETRIES_PER_MODEL + 1
        ):

            try:

                response = (
                    client.models.generate_content(
                        model=model,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            response_mime_type="application/json"
                        )
                    )
                )

                response_text = response.text

                if not response_text:

                    raise RuntimeError(
                        "Gemini returned an empty response."
                    )

                data = json.loads(
                    response_text
                )

                print(
                    f"Extraction successful "
                    f"using {model}."
                )

                return data

            except Exception as error:

                last_error = error

                print(
                    f"Model {model} failed "
                    f"(attempt {attempt})."
                )

                print(str(error))

                if attempt < MAX_RETRIES_PER_MODEL:

                    wait_seconds = (
                        3 * attempt
                    )

                    print(
                        f"Retrying in "
                        f"{wait_seconds} seconds..."
                    )

                    time.sleep(
                        wait_seconds
                    )

        print(
            "Trying fallback model..."
        )

    raise RuntimeError(
        "All Gemini models failed. "
        f"Last error: {last_error}"
    )


# =================================================
# COMPLETE INVOICE PROCESSOR
# =================================================

def process_invoice(
    pdf_path,
    output_path=None
):

    print("=" * 50)
    print("AI Invoice Processing")
    print("=" * 50)

    # Create Gemini client
    client = create_gemini_client()

    # PDF → OCR
    print("Step 1: OCR")

    ocr_text = extract_ocr_text(
        pdf_path
    )

    # OCR → AI → JSON
    print("Step 2: AI Extraction")

    invoice_data = extract_invoice_data(
        ocr_text,
        client
    )

    # Optional JSON save
    if output_path:

        output_path = Path(
            output_path
        )

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                invoice_data,
                file,
                indent=4,
                ensure_ascii=False
            )

    print("Invoice processing completed.")

    return invoice_data