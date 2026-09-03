# AI Invoice Processor

AI-powered invoice processing workflow that converts PDF invoices into structured data, validates invoice calculations, detects exceptions, and generates Excel reports.

## Workflow

PDF → OCR → Gemini AI → Structured JSON → Validation → Excel

## Features

- PDF invoice processing
- OCR for scanned/image-based invoices
- AI-powered invoice data extraction
- Structured JSON output
- Invoice calculation validation
- Exception and error detection
- Single invoice processing
- Batch invoice processing
- Excel report generation
- REVIEW REQUIRED status for problematic invoices
- Windows desktop GUI
- Standalone Windows `.exe` deployment

## Invoice Data Extracted

The system can extract:

- Vendor name
- Invoice number
- Invoice date
- Due date
- Customer name
- Line items
- Quantity
- Unit price
- Amount
- Subtotal
- Tax
- Total

## Validation

If a calculation does not match, the invoice is marked as:

**REVIEW REQUIRED**

Example:

```text
Line item 1: quantity × unit price does not match amount.
