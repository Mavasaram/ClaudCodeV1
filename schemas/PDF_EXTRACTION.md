# PDF Extraction Targets

This document describes the fields and extraction rules for invoice PDFs. Use table detection libraries (Camelot, Tabula, or `pdfplumber`) and OCR (`pytesseract`) for scanned documents.

Primary fields to extract:

- `InvoiceNumber` — prefer patterns like INV-YYYY-######
- `VendorName`
- `InvoiceDate` — parse to ISO date
- `DueDate` — parse to ISO date
- `InvoiceAmount` — numeric, currency-normalized
- `Currency`
- `PaymentTerms` / `DiscountTerms`
- `PO_Number`
- `LineItems` (table): SKU, Description, Qty, UnitPrice, LineTotal
- `VendorBankAccount` / Payment details (if present)

Extraction strategy:

1. Attempt to locate invoice header area: search text for keywords `Invoice`, `Invoice No`, `Invoice #`.
2. Use table detection to find line-item tables; fall back to heuristic table parsing if library fails.
3. Normalize numbers by removing currency symbols and thousands separators.
4. If document appears scanned (low text density), run OCR and reapply steps above.
5. Validate extracted totals: compare table row totals with reported `InvoiceAmount`.

Tooling suggestions:

- `pdfplumber` — good for text extraction and simple tables
- `camelot` / `tabula-py` — better for structured tables when PDFs are digital
- `pytesseract` + `pdf2image` — for OCR fallback on scanned PDFs

Output format:

Return a normalized JSON payload with the same fields as the `Invoices` sheet and an optional `LineItems` array.

Confidence and flags:

- Each extracted field should include a confidence score where possible and a `flag` when parsing fails or mismatches are found (e.g., totals mismatch).
