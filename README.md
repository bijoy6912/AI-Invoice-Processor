# AI Invoice Processor

AI-powered invoice extraction, validation, OCR, and Excel reporting.

## What This Project Does

This project extracts structured data from invoice PDFs using OCR and Gemini AI.

It can:

- Extract invoice details from PDF invoices
- Process scanned/image-based invoices using OCR
- Convert invoice data into structured JSON
- Validate invoice calculations
- Process multiple invoices in batch
- Export validated results to Excel
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

```text
Invoice PDF
    ↓
PyMuPDF
    ↓
Tesseract OCR
    ↓
Raw OCR Text
    ↓
Gemini AI
    ↓
Structured JSON
    ↓
Validation
    ↓
Excel Report