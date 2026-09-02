import json
from decimal import Decimal


# Load extracted invoice data
with open("ocr_invoice_result.json", "r", encoding="utf-8") as file:
    invoice = json.load(file)


print("========== INVOICE VALIDATION ==========")

errors = []
warnings = []


# ------------------------------------------------
# 1. Check line item calculations
# ------------------------------------------------

calculated_subtotal = Decimal("0")

for item in invoice.get("line_items", []):

    quantity = Decimal(str(item["quantity"]))
    unit_price = Decimal(str(item["unit_price"]))
    amount = Decimal(str(item["amount"]))

    expected_amount = quantity * unit_price

    if expected_amount != amount:
        errors.append(
            f"Line item error: {item['description']} "
            f"(expected {expected_amount}, found {amount})"
        )

    calculated_subtotal += amount


# ------------------------------------------------
# 2. Check subtotal
# ------------------------------------------------

subtotal = Decimal(str(invoice["subtotal"]))

if calculated_subtotal != subtotal:
    errors.append(
        f"Subtotal mismatch: calculated {calculated_subtotal}, "
        f"invoice says {subtotal}"
    )


# ------------------------------------------------
# 3. Check total
# ------------------------------------------------

tax = Decimal(str(invoice["tax"]))
total = Decimal(str(invoice["total"]))

calculated_total = subtotal + tax

if calculated_total != total:
    errors.append(
        f"Total mismatch: calculated {calculated_total}, "
        f"invoice says {total}"
    )


# ------------------------------------------------
# 4. Check required fields
# ------------------------------------------------

required_fields = [
    "vendor_name",
    "invoice_number",
    "invoice_date",
    "customer_name",
    "subtotal",
    "tax",
    "total"
]

for field in required_fields:

    if not invoice.get(field):
        warnings.append(f"Missing field: {field}")


# ------------------------------------------------
# Final result
# ------------------------------------------------

if not errors and not warnings:

    print("✅ VALIDATION PASSED")
    print("All invoice calculations are correct.")
    print("No required fields are missing.")

elif errors:

    print("❌ VALIDATION FAILED")

    for error in errors:
        print("ERROR:", error)

else:

    print("⚠️ VALIDATION PASSED WITH WARNINGS")

    for warning in warnings:
        print("WARNING:", warning)