# Dynamic Discounts — Project Details

Date: 2026-02-22

## Objective

Create a local, web-based application for business users to ingest specific data files (Excel, PDF), optionally receive ERP inputs, process data via backend sub-agents, and present results in a friendly, animated UI for demo and production use.

## Chosen stack (initial)

- Frontend: React (recommended) — modern, component-driven UI with animation support
- Backend: Python + FastAPI — lightweight, async, easy to extend with sub-agents
- File readers: Excel (.xlsx) and PDF (parser sub-agents)
- ERP: Support mock/demo data by default; provide optional connector for real ERP via secure API credentials

## High-level features

- Upload and parse input files (Excel, PDF)
- File-reader sub-agents for extracting structured inputs
- Background processing pipeline (FastAPI + worker tasks)
- Animated, user-friendly frontend with progress/processing visuals
- ERP mock service and optional real ERP connector

## Current todo (snapshot)

- [in-progress] Create project scaffold (frontend + backend)
- [not-started] Define data inputs & file schemas
- [not-started] Implement file-reader sub-agents
- [not-started] Build backend API & processing
- [not-started] Develop frontend UI + animations
- [not-started] Add ERP mock & demo data
- [not-started] Write README + run instructions

## File / data schemas (to define)

- Excel: sheet names, required columns (e.g., SKU, Price, Cost, StartDate, EndDate, Segment)
- PDF: policy or contract extraction rules (table detection, OCR if scanned)
- JSON: optional structured exchange format for ERP or processed output

## Sub-agent roles (initial)

- `excel_reader`: validate and parse .xlsx input into normalized rows
- `pdf_reader`: extract tables / key fields from PDFs (use camelot/Tabula or OCR fallback)
- `erp_fetcher`: mock ERP API for demo; pluggable real connector
- `processor`: apply business rules and compute discounts

## Minimal run instructions (placeholders)

1. Backend (Python): create a virtualenv, install `fastapi`, `uvicorn`, `pandas`, `openpyxl`, `pdfplumber`/`camelot`, and other deps.

2. Frontend (React): scaffold with `create-react-app` or `Vite`, add animation library (Framer Motion).

3. Start backend:

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

4. Start frontend (from `frontend/`):

```
cd frontend
npm install
npm run dev
```

## Next steps (recommended immediate actions)

1. Scaffold the repo (backend + frontend) and commit initial files.
2. Define exact Excel sheet column names and PDF extraction targets for the first demo.
3. Implement `excel_reader` and `pdf_reader` sub-agents with unit tests.

---

This document is a living note for the project — update as choices and schemas solidify.
