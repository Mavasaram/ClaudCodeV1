"""Generate sample Excel and PDF invoice files for demo and testing.

Usage:
    python tools/generate_sample_data.py

Creates:
 - sample_invoices.xlsx
 - sample_invoice_INV-2025-45678.pdf
"""
from pathlib import Path
import pandas as pd
from datetime import datetime

OUT_DIR = Path("sample_data")
OUT_DIR.mkdir(exist_ok=True)

def make_excel(path: Path):
    invoices = [
        {
            "InvoiceNumber": "INV-2025-45678",
            "VendorName": "ABC Supplies Inc.",
            "InvoiceDate": "2026-02-01",
            "DueDate": "2026-03-03",
            "InvoiceAmount": 125450.00,
            "Currency": "USD",
            "PaymentTerms": "Net 30",
            "DiscountTerms": "2/10 Net 30",
            "PO_Number": "PO-99881",
            "CostCenter": "CC-4501",
            "Department": "Operations",
            "PaymentMethod": "ACH",
            "VendorBankAccount": "XXXX-XXXX-7845",
            "Reference": "INV-2025-45678"
        }
    ]

    invoices_df = pd.DataFrame(invoices)

    line_items = [
        {
            "InvoiceNumber": "INV-2025-45678",
            "LineNumber": 1,
            "SKU": "ABC-111",
            "Description": "Widget A",
            "Quantity": 100,
            "UnitPrice": 1000.00,
            "LineTotal": 100000.00
        },
        {
            "InvoiceNumber": "INV-2025-45678",
            "LineNumber": 2,
            "SKU": "ABC-222",
            "Description": "Widget B",
            "Quantity": 25,
            "UnitPrice": 1018.00,
            "LineTotal": 25450.00
        }
    ]

    line_items_df = pd.DataFrame(line_items)

    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        invoices_df.to_excel(writer, sheet_name="Invoices", index=False)
        line_items_df.to_excel(writer, sheet_name="LineItems", index=False)

    print(f"Wrote Excel: {path}")


def make_pdf(path: Path):
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
    except Exception:
        print("reportlab not installed — to generate PDF run: pip install reportlab")
        return

    c = canvas.Canvas(str(path), pagesize=letter)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(72, 720, "Invoice")
    c.setFont("Helvetica", 10)
    c.drawString(72, 700, "Invoice Number: INV-2025-45678")
    c.drawString(72, 685, "Vendor: ABC Supplies Inc.")
    c.drawString(72, 670, "Invoice Date: 2026-02-01")
    c.drawString(72, 655, "Due Date: 2026-03-03")
    c.drawString(72, 640, "Invoice Amount: $125,450.00")

    # simple table header
    c.drawString(72, 600, "Line Items:")
    y = 580
    c.drawString(72, y, "1 | ABC-111 | Widget A | 100 | 1,000.00 | 100,000.00")
    y -= 15
    c.drawString(72, y, "2 | ABC-222 | Widget B | 25 | 1,018.00 | 25,450.00")

    c.showPage()
    c.save()
    print(f"Wrote PDF: {path}")


def main():
    excel_path = OUT_DIR / "sample_invoices.xlsx"
    pdf_path = OUT_DIR / "sample_invoice_INV-2025-45678.pdf"
    make_excel(excel_path)
    make_pdf(pdf_path)


if __name__ == "__main__":
    main()
