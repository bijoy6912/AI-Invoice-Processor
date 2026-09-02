import json
from openpyxl import Workbook
from openpyxl.styles import Font


# Load invoice data
with open("ocr_invoice_result.json", "r", encoding="utf-8") as file:
    invoice = json.load(file)


# Create Excel workbook
workbook = Workbook()
sheet = workbook.active
sheet.title = "Invoice Data"


# Excel headers
headers = [
    "Invoice Number",
    "Vendor",
    "Customer",
    "Description",
    "Quantity",
    "Unit Price",
    "Amount",
    "Subtotal",
    "Tax",
    "Total",
    "Status"
]

sheet.append(headers)


# Make headers bold
for cell in sheet[1]:
    cell.font = Font(bold=True)


# Determine validation status
status = "VALID"


# Add line items
for item in invoice.get("line_items", []):

    sheet.append([
        invoice.get("invoice_number"),
        invoice.get("vendor_name"),
        invoice.get("customer_name"),
        item.get("description"),
        item.get("quantity"),
        item.get("unit_price"),
        item.get("amount"),
        invoice.get("subtotal"),
        invoice.get("tax"),
        invoice.get("total"),
        status
    ])


# Adjust column widths
for column in sheet.columns:
    max_length = 0
    column_letter = column[0].column_letter

    for cell in column:
        if cell.value is not None:
            max_length = max(max_length, len(str(cell.value)))

    sheet.column_dimensions[column_letter].width = max_length + 2


# Save Excel file
output_file = "invoice_result.xlsx"
workbook.save(output_file)

print(f"✅ Excel file created successfully: {output_file}")