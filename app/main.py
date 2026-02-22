from fastapi import FastAPI, UploadFile, File, HTTPException, Header, Request
from fastapi.responses import JSONResponse
import shutil
from pathlib import Path
from app.excel_reader import parse_excel
from app.pdf_reader import parse_pdf
from app.processor import analyze_invoice, enrich_with_routing_and_schedule
from app.erp_mock import list_vendors, get_vendor_by_name
from app.approvals import register_approvals, get_approvals, update_approval
import os

app = FastAPI(title="Payable Agent Prototype")

UPLOAD_DIR = Path(".uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.post("/upload_excel")
async def upload_excel(file: UploadFile = File(...)):
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Only Excel files (.xlsx/.xls) are supported")

    dest = UPLOAD_DIR / file.filename
    with dest.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    parsed = parse_excel(str(dest))
    return JSONResponse(content=parsed)



@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported for this endpoint")

    dest = UPLOAD_DIR / file.filename
    with dest.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    parsed = parse_pdf(str(dest))
    # run basic processing if fields present
    fields = parsed.get("fields", {})
    line_items = parsed.get("line_items", [])
    analysis = analyze_invoice(fields, line_items)
    # enrich analysis with payment schedule and approval routing
    analysis = enrich_with_routing_and_schedule(analysis, fields)
    parsed["analysis"] = analysis

    # register approval steps in in-memory approvals store (keyed by InvoiceNumber)
    invoice_id = parsed.get('fields', {}).get('InvoiceNumber')
    if invoice_id and analysis.get('approval_steps'):
        register_approvals(invoice_id, analysis.get('approval_steps'))
        parsed['invoice_id'] = invoice_id
    return JSONResponse(content=parsed)


@app.get('/erp/vendors')
def api_list_vendors():
    return JSONResponse(content=list_vendors())


@app.get('/erp/vendor')
def api_get_vendor(name: str):
    v = get_vendor_by_name(name)
    if not v:
        raise HTTPException(status_code=404, detail='Vendor not found')
    return JSONResponse(content=v)


@app.get('/approvals/{invoice_number}')
def api_get_approvals(invoice_number: str):
    a = get_approvals(invoice_number)
    if a is None:
        raise HTTPException(status_code=404, detail='Approvals not found')
    return JSONResponse(content={"invoice": invoice_number, "steps": a})


@app.post('/approvals/{invoice_number}/update')
def api_update_approval(invoice_number: str, payload: dict):
    level = payload.get('level')
    status = payload.get('status')
    actioned_by = payload.get('actioned_by')
    notes = payload.get('notes')
    if level is None or status is None:
        raise HTTPException(status_code=400, detail='level and status required')
    s = update_approval(invoice_number, level, status, actioned_by, notes)
    if s is None:
        raise HTTPException(status_code=404, detail='Approval step not found')
    return JSONResponse(content=s)


@app.get('/approvals/{invoice_number}/audit')
def api_get_approvals_audit(invoice_number: str):
    from app.approvals import get_audit
    return JSONResponse(content={"invoice": invoice_number, "audit": get_audit(invoice_number)})


@app.post('/simulate/{invoice_number}')
def api_run_simulation(invoice_number: str):
    from app.simulated_approvers import run_simulation
    res = run_simulation(invoice_number)
    return JSONResponse(content=res)


@app.post('/migrate_memory')
def api_migrate_memory(payload: dict, request: Request, x_migrate_secret: str = Header(None)):
    """Securely migrate an exported in-memory approvals/audit dump into SQLite.

    Protect this endpoint by setting the `MIGRATE_SECRET` env var on the server and
    supplying it in the `X-MIGRATE-SECRET` header.
    Payload options:
      - { "module": "module.path" }  # imports module and reads _STORE/_AUDIT
      - { "json_path": "/path/to/dump.json" }
      - { "store": {...}, "audit": {...} }
    """
    # only allow requests coming from localhost (127.0.0.1 or ::1)
    client_host = None
    try:
        client_host = request.client.host
    except Exception:
        client_host = None
    if client_host not in ('127.0.0.1', '::1', 'localhost'):
        raise HTTPException(status_code=403, detail=f'Migration endpoint allowed only from localhost (got {client_host})')

    expected = os.getenv('MIGRATE_SECRET')
    if not expected:
        raise HTTPException(status_code=400, detail='Server migration secret not configured (MIGRATE_SECRET)')
    if x_migrate_secret != expected:
        raise HTTPException(status_code=403, detail='Invalid migration secret')

    # load source
    store = {}
    audit = {}
    if 'module' in payload:
        import importlib
        m = importlib.import_module(payload['module'])
        store = getattr(m, '_STORE', {}) or {}
        audit = getattr(m, '_AUDIT', {}) or {}
    elif 'json_path' in payload:
        import json
        p = payload['json_path']
        try:
            with open(p, 'r') as fh:
                d = json.load(fh)
            store = d.get('store', {})
            audit = d.get('audit', {})
        except Exception as e:
            raise HTTPException(status_code=400, detail=f'Failed to read JSON path: {e}')
    else:
        store = payload.get('store', {}) or {}
        audit = payload.get('audit', {}) or {}

    from app.approvals import migrate_from_memory
    try:
        migrate_from_memory(store, audit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Migration failed: {e}')

    return JSONResponse(content={"migrated_invoices": len(store), "migrated_audit_entries": sum(len(v) for v in audit.values())})
