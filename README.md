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

The system validates invoice calculations such as:

~~~text
Quantity × Unit Price = Amount

Line Items Total = Subtotal

Subtotal + Tax = Total
~~~

If a calculation does not match, the invoice is marked as:

**REVIEW REQUIRED**

Example:

~~~text
Line item 1: quantity × unit price does not match amount.
~~~

## Screenshots

### Invoice Processing GUI

The desktop application processes invoice PDFs using OCR and Gemini AI.

![AI Invoice Processor GUI](screenshots/invoice_processor_gui.png)

### Excel Validation Report

The generated Excel report contains extracted invoice data, validation status, errors, and warnings.

![Invoice Excel Report](screenshots/invoice_excel_report.png)

## Processing Modes

### Single Invoice

Select one PDF invoice and process it through the complete workflow.

### Batch Processing

Select multiple PDF invoices and process them together. The system generates an Excel report containing the extracted data and validation results.

## Output

The generated Excel report contains:

- Source File
- Invoice Number
- Vendor
- Customer
- Invoice Date
- Due Date
- Subtotal
- Tax
- Total
- Status
- Errors
- Warnings

## Example Results

### Valid Invoice

~~~text
Status: VALID
~~~

### Invoice With Calculation Error

~~~text
Status: REVIEW REQUIRED
~~~

The system does not silently accept calculation inconsistencies. Problematic invoices are flagged for human review.

## Technology

- Python
- Tesseract OCR
- Google Gemini API
- PyMuPDF
- Tkinter
- OpenPyXL
- PyInstaller

## Architecture

~~~text
PDF Invoice
    ↓
OCR
    ↓
Gemini AI Extraction
    ↓
Structured JSON
    ↓
Invoice Validation
    ↓
Excel Report
~~~

## Windows Application

The project can be packaged as a standalone Windows `.exe` application using PyInstaller.

The application provides a desktop GUI for:

- Selecting invoice PDFs
- Processing individual invoices
- Processing multiple invoices
- Viewing processing status
- Opening the generated Excel report

## API Key

The application requires a Gemini API key.

For client deployment, each client should use their own Gemini API key.

The API key should never be committed to GitHub or embedded directly into the application source code.

## Project Purpose

This is a self-initiated portfolio project demonstrating practical AI document processing, invoice extraction, validation, exception detection, and Excel automation.

The goal is to automate repetitive invoice processing tasks while keeping validation and human review in the workflow.
