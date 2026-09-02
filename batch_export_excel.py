import json
from openpyxl import Workbook
from openpyxl.styles import Font


# Load validated batch results
with open("validated_batch_results.json", "r", encoding="utf-8") as file:
    invoices = json.load(file)


# Create Excel workbook
workbook = Workbook()
sheet = workbook.active
sheet.title = "Invoice Report"


# Headers
headers = [
    "Source File",
    "Invoice Number",
    "Vendor",
    "Customer",
    "Invoice Date",
    "Due Date",
    "Subtotal",
    "Tax",
    "Total",
    "Status",
    "Errors",
    "Warnings"
]

sheet.append(headers)


# Make headers bold
for cell in sheet[1]:
    cell.font = Font(bold=True)


# Add invoice rows
for invoice in invoices:

    errors = "; ".join(invoice.get("validation_errors", []))
    warnings = "; ".join(invoice.get("validation_warnings", []))

    sheet.append([
        invoice.get("source_file"),
        invoice.get("invoice_number"),
        invoice.get("vendor_name"),
        invoice.get("customer_name"),
        invoice.get("invoice_date"),
        invoice.get("due_date"),
        invoice.get("subtotal"),
        invoice.get("tax"),
        invoice.get("total"),
        invoice.get("validation_status"),
        errors,
        warnings
    ])


# Adjust column widths
for column in sheet.columns:

    max_length = 0
    column_letter = column[0].column_letter

    for cell in column:
        if cell.value is not None:
            max_length = max(max_length, len(str(cell.value)))

    sheet.column_dimensions[column_letter].width = min(max_length + 2, 40)


# Freeze header row
sheet.freeze_panes = "A2"


# Save Excel report
output_file = "invoice_batch_report.xlsx"

workbook.save(output_file)

print()
print("========================================")
print("   BATCH EXCEL REPORT CREATED")
print("========================================")
print(f"✅ File: {output_file}")
print(f"✅ Invoices included: {len(invoices)}")