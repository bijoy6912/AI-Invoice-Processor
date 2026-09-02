# AI Invoice Processor
AI-powered invoice extraction, validation, OCR, and Excel reporting.
## What This Project Does

This project extracts structured data from invoice PDFs using OCR and Gemini AI.

It can:
- Extract invoice details from PDFs
- Process scanned invoices using OCR
- Convert invoice data into structured JSON
- Validate invoice calculations
- Export results to Excel
- Handle temporary AI API failures with automatic retries
## Technology Stack

- Python
- PyMuPDF
- Tesseract OCR
- Gemini AI
- OpenPyXL
- JSON
- Excel
## Workflow

Invoice PDF
→ OCR
→ Gemini AI
→ Structured JSON
→ Validation
→ Excel Report
## Key Features

### 1. PDF Invoice Extraction
Extracts invoice number, dates, vendor, customer, line items, subtotal, tax, and total.

### 2. OCR Support
Can process scanned/image-based invoices using Tesseract OCR.

### 3. AI-Powered Structuring
Uses Gemini AI to convert raw invoice text into structured JSON.

### 4. Validation
Checks line-item calculations, subtotal, tax, total, and required fields.

### 5. Excel Reporting
Exports extracted and validated invoice data into a client-friendly Excel report.

### 6. Retry Handling
Automatically retries temporary Gemini API failures.
## Example Output

The system successfully processed a sample invoice and produced:

- Structured JSON output
- Validation status: `VALID`
- Excel report with invoice details
- Correct subtotal: `$850.00`
- Correct tax: `$68.00`
- Correct total: `$918.00`
## Setup

1. Create a Python virtual environment.
2. Install the required packages.
3. Install Tesseract OCR.
4. Set the `GEMINI_API_KEY` environment variable.
5. Place the invoice PDF in the project folder.
6. Run the OCR + Gemini extraction script.
7. Run validation.
8. Export the result to Excel.
## Project Structure

AI-Invoice-Processor/
├── invoice.pdf
├── invoices/
├── ai_extract.py
├── ocr_gemini.py
├── validate_invoice.py
├── export_excel.py
├── batch_process.py
├── batch_validate.py
├── batch_export_excel.py
├── invoice_result.json
├── ocr_invoice_result.json
├── invoice_result.xlsx
├── invoice_batch_report.xlsx
└── README.md
## Future Improvements

- Support multiple invoice formats
- Add confidence scores for extracted fields
- Improve table extraction for complex invoices
- Add a web interface
- Add database storage
- Add support for additional document types