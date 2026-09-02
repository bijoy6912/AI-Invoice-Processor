import os
import json
from pypdf import PdfReader
from google import genai


# Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Folder containing invoices
invoice_folder = "invoices"

# Store all results
all_invoices = []


# Find all PDF files
pdf_files = [
    file for file in os.listdir(invoice_folder)
    if file.lower().endswith(".pdf")
]

print(f"Found {len(pdf_files)} PDF files.")
print()


# Process each PDF
for filename in pdf_files:

    print(f"Processing: {filename}")

    pdf_path = os.path.join(invoice_folder, filename)

    # Read PDF
    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    # AI prompt
    prompt = f"""
You are a professional invoice data extraction assistant.

Extract all important information from this invoice.

Return ONLY valid JSON.
Do not use markdown code blocks.
Do not add explanations.

Use exactly this structure:

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
- Extract every line item.
- quantity must be a number.
- unit_price must be a number.
- amount must be a number.
- subtotal, tax and total must be numbers.
- Do not include "$".
- Do not invent information.
- Use null if information is missing.

Invoice text:

{text}
"""

    # Send to Gemini
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    result = response.text.strip()

    # Convert AI result to JSON
    try:
        invoice_data = json.loads(result)

        invoice_data["source_file"] = filename

        all_invoices.append(invoice_data)

        print("  ✅ Successfully extracted")

    except json.JSONDecodeError:

        print("  ❌ AI returned invalid JSON")


print()
print("========== BATCH PROCESSING COMPLETE ==========")

# Save all results
with open("batch_results.json", "w", encoding="utf-8") as file:
    json.dump(all_invoices, file, indent=4)

print(f"✅ Saved {len(all_invoices)} invoices to batch_results.json")