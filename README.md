# Payable Agent AI – Local Web Application

> A business-friendly demo application for processing invoices (Excel/PDF), analyzing payment terms, calculating discount impact, and managing multi-level approval workflows with animated UI and persistent state.

## 📋 Quick Start

### Prerequisites
- Python 3.8+
- macOS, Linux, or Windows with a web browser

### 1. Set Up Environment

Clone the repository and create a virtual environment:
```bash
git clone https://github.com/Mavasaram/ClaudCodeV1.git
cd "Dynamic Discounts"
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Generate Sample Data (Optional)

Create demo invoice files for testing:
```bash
python3 tools/generate_sample_data.py
```

Output: `sample_data/sample_invoices.xlsx` and `sample_data/sample_invoice_INV-2025-45678.pdf`

### 3. Start the Backend Server

Run the FastAPI backend (listens on `http://127.0.0.1:8000`):
```bash
export MIGRATE_SECRET='demo-secret'  # used only if migrating in-memory data
uvicorn app.main:app --reload
```

Leave this terminal running. You'll see `Uvicorn running on http://127.0.0.1:8000`.

### 4. Open the Frontend UI

In a separate terminal, open the static demo UI in your browser:
```bash
open frontend_static/index.html
# or on Linux:
xdg-open frontend_static/index.html
# or manually copy the file path into your browser address bar
```

You should see a clean interface with:
- File upload area
- Processing indicator
- Analysis results display
- Approval workflow timeline
- Action buttons (Approve / Escalate)
- Audit log panel

---

## 📖 User Guide: Invoice Processing & Approval Workflow

### Step-by-Step Workflow

#### **Step 1: Upload an Invoice**

1. Click the **"Choose File"** button in the UI.
2. Select a PDF invoice file (e.g., `sample_data/sample_invoice_INV-2025-45678.pdf`).
3. Click **"Upload & Process"**.

The system will:
- Parse the PDF and extract invoice details (number, date, amount, line items).
- Analyze the invoice for discount terms and payment impact.
- Calculate the annualized discount return if early payment terms are offered.
- Determine the Days Payable Outstanding (DPO) impact.
- Route the invoice to approval levels based on amount.
- Display enriched analysis.

#### **Step 2: Review Analysis**

After upload, the UI shows:

**📊 Key Metrics:**
- **Invoice Number** & **Invoice Date**
- **Invoice Amount** (total to be paid)
- **Due Date** (standard net payment date)
- **Recommended Payment Date** (if discount is available, the discount cut-off date)
- **Discount Terms** (e.g., "2% 10 Net 30" meaning 2% off if paid within 10 days)
- **Annualized Return** (calculated benefit of taking the discount, typical range 36–73%)
- **DPO Impact** (effect on Days Payable Outstanding if discount is taken)

**Example Analysis Output:**
```json
{
  "invoice_number": "INV-2025-45678",
  "invoice_amount": 125450.0,
  "discount_terms": "2% / 10 Net 30",
  "annualized_return": "36.73%",
  "dpo_impact": "Reduces DPO by ~5 days if discount taken",
  "payment_schedule": {
    "recommended_payment_date": "2026-03-03",
    "discount_date": "2026-02-26"
  }
}
```

#### **Step 3: Review Approval Routing**

Below the analysis, an **Approval Timeline** card displays the multi-level approval chain:

**Approval Levels** (example for a $125k invoice):
- **Level 1 – Manager** (≤$50k) — Status: **Completed** (pre-approved)
- **Level 2 – Operations Manager** (≤$200k) — Status: **Pending** ⏳
- **Level 3 – VP Operations** (>$200k) — Status: **Pending** ⏳

Each level shows:
- Approver name and role
- Assigned date & time
- Status badge (Pending / Completed / Escalated)
- Escalation threshold (time window before automatic escalation)

#### **Step 4: Take Action on Approval Steps**

For **Pending** approval levels, you can:

**Option A – Approve**
1. Click the **"Approve"** button next to a Pending level.
2. A confirmation modal appears: *"Confirm approval of Level 2 by Operations Manager?"*
3. Click **"Confirm"** to approve.
4. The UI updates:
   - Status changes to **Completed** ✓
   - The step card animates (slides in from left, brief highlight).
   - Timestamp **Actioned At** is recorded.
   - Actioned By field shows the approver role.

**Option B – Escalate** (optional future feature)
1. Click the **"Escalate"** button to flag the step as requiring higher authority.
2. A modal prompts for escalation reason (optional notes).
3. The status updates to **Escalated** and is recorded in the audit log.

#### **Step 5: Run Simulation**

To test the automated approval workflow without manually approving each step:

1. Click the **"Run Simulation"** button (lower section of the UI).
2. The system auto-approves all Pending steps based on role-based rules:
   - Each level is assigned a simulated approver matching the role.
   - Approvals are recorded with timestamps and actor names.
   - Animation shows each step completing in sequence.
3. After simulation completes, all Pending steps become **Completed**.

#### **Step 6: View Audit Log**

At the bottom of the UI, the **Audit Log** panel displays a chronological record of all actions:

**Audit Entry Example:**
```
[2026-02-22 18:56:08] Level 2 approved by Operations Manager (notes: "Routine approval")
[2026-02-22 18:56:15] Level 3 approved by VP Operations (Simulation)
```

Each entry includes:
- Exact timestamp
- Approval level
- Approver role
- Actioned by (user/system identifier)
- Status outcome
- Notes (if any)

#### **Step 7: Verify Persistence**

State persists across browser refreshes and server restarts (stored in SQLite at `data/approvals.db`):

1. Approve or simulate steps as in Steps 4–5.
2. Close the browser tab or restart the backend:
   ```bash
   # Kill the uvicorn server (Ctrl+C), then restart:
   uvicorn app.main:app --reload
   ```
3. Reopen the frontend UI.
4. Upload the same invoice again (or navigate to it if cached).
5. The approval state, audit log, and timestamps are preserved.

---

## 🔧 Advanced Usage

### Excel File Upload (Alternative Input)

The system also accepts Excel workbooks (`.xlsx`). The UI currently defaults to PDF, but the backend supports:

```bash
curl -F "file=@sample_data/sample_invoices.xlsx" http://127.0.0.1:8000/upload_excel
```

Excel schema: columns for `InvoiceNumber`, `InvoiceDate`, `DueDate`, `Amount`, `LineItems`, etc. See `schemas/EXCEL_SCHEMA.md` for details.

### Database Persistence

#### View Approvals via API

Fetch the current approval state for an invoice:
```bash
curl http://127.0.0.1:8000/approvals/INV-2025-45678
```

Response:
```json
{
  "invoice": "INV-2025-45678",
  "steps": [
    {
      "level": 1,
      "approver_name": "Level1 Approver",
      "status": "Completed",
      "actioned_at": "2026-02-22T18:56:08.224679Z",
      ...
    },
    {
      "level": 2,
      "approver_name": "Sarah Johnson",
      "status": "Pending",
      ...
    }
  ]
}
```

#### Retrieve Audit History

Get all actions (approvals, escalations, simulations) for an invoice:
```bash
curl http://127.0.0.1:8000/approvals/INV-2025-45678/audit
```

#### Manually Update an Approval Step

Approve a step via API:
```bash
curl -X POST http://127.0.0.1:8000/approvals/INV-2025-45678/update \
  -H "Content-Type: application/json" \
  -d '{
    "level": 2,
    "status": "Completed",
    "actioned_by": "api_user",
    "notes": "Approved via API"
  }'
```

#### Programmatic Simulation

Trigger role-based auto-approval:
```bash
curl -X POST http://127.0.0.1:8000/simulate/INV-2025-45678
```

Returns:
```json
{
  "invoice_number": "INV-2025-45678",
  "simulated_approvals": [
    {"level": 2, "approver": "Sarah Johnson", "status": "Completed"},
    {"level": 3, "approver": "Michael Chen", "status": "Completed"}
  ]
}
```

### Migrating In-Memory Data

If you have a prior version's in-memory approval data (from `_STORE` and `_AUDIT` variables), you can migrate it to SQLite:

#### Option 1: CLI Migration Script

Export your in-memory data to JSON:
```json
{
  "store": {
    "INV-2025-45678": [
      { "level": 1, "approver_name": "...", "status": "Completed", ... }
    ]
  },
  "audit": {
    "INV-2025-45678": [
      { "timestamp": "...", "level": 1, "status": "Completed", ... }
    ]
  }
}
```

Then run the CLI:
```bash
python3 scripts/migrate_in_memory.py --json data/in_memory_dump.json
```

#### Option 2: Runtime Endpoint

Start the server with the migration secret:
```bash
export MIGRATE_SECRET='demo-secret'
uvicorn app.main:app --reload
```

Call the migration endpoint from localhost:
```bash
curl -X POST http://127.0.0.1:8000/migrate_memory \
  -H "Content-Type: application/json" \
  -H "X-MIGRATE-SECRET: demo-secret" \
  -d '{"json_path": "data/in_memory_dump.json"}'
```

**Security Note:** The endpoint only accepts requests from `127.0.0.1` (localhost) and requires a matching `MIGRATE_SECRET` environment variable.

---

## 📁 Project Structure

```
Dynamic Discounts/
├── README.md                          # This file
├── PROJECT_DETAILS.md                 # High-level project overview
├── PAYABLE_AGENT_USE_CASE.md          # Detailed business use case
├── requirements.txt                   # Python dependencies
│
├── app/
│   ├── main.py                        # FastAPI server entry point
│   ├── excel_reader.py                # Parse Excel invoices
│   ├── pdf_reader.py                  # Parse PDF invoices
│   ├── processor.py                   # Business logic (discount, DPO, routing)
│   ├── erp_mock.py                    # Mock ERP vendor master
│   ├── approvals.py                   # SQLite-backed approval & audit store
│   └── simulated_approvers.py         # Role-based automation
│
├── frontend_static/
│   ├── index.html                     # Static UI (no npm/node required)
│   ├── app.js                         # UI logic & API calls
│   └── styles.css                     # Animations & layout
│
├── frontend/                          # (Optional) React + Vite scaffold
│   ├── package.json
│   ├── src/
│   │   ├── App.jsx
│   │   └── components/
│   └── ...
│
├── tools/
│   └── generate_sample_data.py        # Create demo Excel/PDF invoices
│
├── scripts/
│   └── migrate_in_memory.py           # CLI to migrate in-memory state to SQLite
│
├── schemas/
│   ├── EXCEL_SCHEMA.md                # Excel column definitions
│   └── PDF_EXTRACTION.md              # PDF parsing strategy
│
├── sample_data/                       # Demo invoices (generated)
│   ├── sample_invoices.xlsx
│   └── sample_invoice_INV-2025-45678.pdf
│
├── data/
│   └── approvals.db                   # SQLite DB (created on first use)
│
└── .uploads/                          # Temporary upload storage
```

---

## 🚀 Deployment & Best Practices

### Local Development
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Testing in a Browser
- Open `frontend_static/index.html` locally (file:// protocol).
- The static UI polls the backend at `http://127.0.0.1:8000` every 2 seconds to refresh approval state and audit log.

### Production Considerations
- Use a production ASGI server (e.g., `gunicorn` with uvicorn workers).
- Set `MIGRATE_SECRET` as an env var; do not commit it to version control.
- Configure CORS if the frontend is served from a different origin.
- Use HTTPS in production.
- Back up `data/approvals.db` regularly.
- Consider adding role-based access control (RBAC) for the approval endpoints.

### Database Backup
```bash
cp data/approvals.db data/approvals.db.backup.$(date +%Y%m%d_%H%M%S)
```

---

## ❓ Troubleshooting

### Issue: "Module not found: pandas" or "pdfplumber"
**Solution:** Ensure you've installed dependencies:
```bash
pip install -r requirements.txt
```

### Issue: "Cannot connect to http://127.0.0.1:8000"
**Solution:** Check that the backend server is running:
```bash
uvicorn app.main:app --reload
# Look for: "Uvicorn running on http://127.0.0.1:8000"
```

### Issue: Frontend doesn't update after approval
**Solution:** The UI polls every 2 seconds. Check browser console for errors (press F12). Verify the backend is responding to `/approvals/{invoice_number}` calls.

### Issue: "Approvals not found" when clicking Approve
**Solution:** Ensure you've uploaded an invoice first (status should change from "Processing" to showing analysis and approval timeline).

### Issue: Database locked error
**Solution:** Only one Python process can write to `data/approvals.db` at a time. If you're running multiple uvicorn workers, configure SQLite WAL mode or switch to PostgreSQL.

---

## 📚 Documentation

For detailed information:
- [Project Overview](PROJECT_DETAILS.md) – Architecture and goals
- [Payable Agent Use Case](PAYABLE_AGENT_USE_CASE.md) – Business workflows and examples
- [Excel Schema](schemas/EXCEL_SCHEMA.md) – Input format for Excel invoices
- [PDF Extraction Strategy](schemas/PDF_EXTRACTION.md) – PDF parsing approach

---

## 🔗 Links

- **GitHub Repository:** https://github.com/Mavasaram/ClaudCodeV1
- **Sample Data Generator:** `tools/generate_sample_data.py`
- **API Docs (Live):** http://127.0.0.1:8000/docs (when server is running)

---

## 📝 License

This project is provided as-is for demonstration and internal business use.

---

## ✅ Checklist: First-Time Setup

- [ ] Clone repository and cd into `Dynamic Discounts`
- [ ] Create virtual environment: `python3 -m venv .venv`
- [ ] Activate venv: `source .venv/bin/activate`
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Generate sample data: `python3 tools/generate_sample_data.py`
- [ ] Start backend: `uvicorn app.main:app --reload`
- [ ] Open frontend in browser: `frontend_static/index.html`
- [ ] Upload a sample PDF and test the approval workflow
- [ ] Verify state persists after a server restart
- [ ] (Optional) Review API docs at http://127.0.0.1:8000/docs

---

**Questions or issues?** Refer to the troubleshooting section above or review the project documentation files.
- Build a small FastAPI endpoint to accept uploads and return normalized JSON
- Add frontend demo pages with animated processing states
