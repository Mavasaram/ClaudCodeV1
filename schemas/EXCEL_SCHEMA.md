# Excel Input Schema

This document defines the recommended Excel sheet layout and required columns for invoice ingestion into the Payable Agent pipeline.

Sheet: `Invoices` (required)

Columns (recommended names and types):

- `InvoiceNumber` (string) — unique invoice identifier
- `VendorName` (string)
- `VendorID` (string) — vendor master ID (optional)
- `InvoiceDate` (ISO date yyyy-mm-dd) — invoice issuance date
- `DueDate` (ISO date yyyy-mm-dd) — payment due date
- `InvoiceAmount` (decimal) — total invoice amount
- `Currency` (string) — ISO currency code (e.g., USD)
- `PaymentTerms` (string) — e.g., "Net 30", "2/10 Net 30"
- `DiscountTerms` (string) — e.g., "2/10 Net 30" or blank
- `PO_Number` (string) — related purchase order
- `CostCenter` (string)
- `Department` (string)
- `GLAccount` (string)
- `PaymentMethod` (string) — e.g., ACH, Wire, Check
- `VendorBankAccount` (string) — masked or full depending on security
- `Reference` (string) — free-text reference
- `Status` (string) — optional (e.g., Pending, Approved)

Sheet: `LineItems` (optional)

Columns:

- `InvoiceNumber` (string) — join key to `Invoices` sheet
- `LineNumber` (int)
- `SKU` (string)
- `Description` (string)
- `Quantity` (decimal)
- `UnitPrice` (decimal)
- `LineTotal` (decimal)

Validation notes:

- Dates should parse to ISO format; accept common variants but normalize on ingest.
- Currency codes should use three-letter ISO codes.
- Invoice totals should equal the sum of line totals when `LineItems` are provided; otherwise trust the `InvoiceAmount` field.
- Use consistent header names; allow a mapping configuration if vendor files differ.

Example row (Invoices sheet):

InvoiceNumber: INV-2025-45678
VendorName: ABC Supplies Inc.
InvoiceDate: 2026-02-01
DueDate: 2026-03-03
InvoiceAmount: 125450.00
Currency: USD
PaymentTerms: Net 30
DiscountTerms: 2/10 Net 30
PO_Number: PO-99881
CostCenter: CC-4501
Department: Operations
PaymentMethod: ACH
VendorBankAccount: XXXX-XXXX-7845
