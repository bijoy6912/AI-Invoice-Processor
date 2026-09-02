import json
from decimal import Decimal


# Load batch results
with open("batch_results.json", "r", encoding="utf-8") as file:
    invoices = json.load(file)


validated_invoices = []


print("========== BATCH VALIDATION ==========")


for invoice in invoices:

    errors = []
    warnings = []

    # Check line items
    calculated_subtotal = Decimal("0")

    for item in invoice.get("line_items", []):

        quantity = Decimal(str(item["quantity"]))
        unit_price = Decimal(str(item["unit_price"]))
        amount = Decimal(str(item["amount"]))

        expected_amount = quantity * unit_price

        if expected_amount != amount:
            errors.append(
                f"Line item mismatch: {item['description']}"
            )

        calculated_subtotal += amount

    # Check subtotal
    subtotal = Decimal(str(invoice["subtotal"]))

    if calculated_subtotal != subtotal:
        errors.append(
            f"Subtotal mismatch: calculated {calculated_subtotal}, "
            f"invoice says {subtotal}"
        )

    # Check total
    tax = Decimal(str(invoice["tax"]))
    total = Decimal(str(invoice["total"]))

    calculated_total = subtotal + tax

    if calculated_total != total:
        errors.append(
            f"Total mismatch: calculated {calculated_total}, "
            f"invoice says {total}"
        )

    # Check required fields
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

    # Determine status
    if errors:
        status = "FAILED"
    elif warnings:
        status = "WARNING"
    else:
        status = "VALID"

    # Add status to invoice
    invoice["validation_status"] = status
    invoice["validation_errors"] = errors
    invoice["validation_warnings"] = warnings

    validated_invoices.append(invoice)

    print(
        f"{invoice.get('source_file', 'unknown')} → {status}"
    )


# Save validated results
with open("validated_batch_results.json", "w", encoding="utf-8") as file:
    json.dump(validated_invoices, file, indent=4)


print()
print("========== VALIDATION COMPLETE ==========")
print(
    f"✅ Saved results to validated_batch_results.json"
)