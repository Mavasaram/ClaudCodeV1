# Dynamic Discounts — Payable Agent Prototype

Lightweight prototype for the Payable Agent AI (invoice ingestion, discount analysis, approvals, payment recommendations).

Selected stack:

- Frontend: React (recommended)
- Backend: Python + FastAPI
- File readers: Excel (.xlsx), PDF

Repository: https://github.com/Mavasaram/ClaudCodeV1

Local setup (recommended):

1. Create and activate a Python virtualenv

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install Python dependencies

```bash
pip install -r requirements.txt
```

3. Generate sample data (optional)

```bash
python3 tools/generate_sample_data.py
```

4. Git & push to GitHub (replace with SSH if preferred)

```bash
git init
git add .
git commit -m "Initial commit: scaffold and docs"
git branch -M main
git remote add origin https://github.com/Mavasaram/ClaudCodeV1.git
git push -u origin main
```

Notes:
- If using HTTPS and push fails, create a GitHub Personal Access Token and use it when prompted, or switch to SSH remote.
- Remove or mask any sensitive data (credentials, full bank account numbers) before pushing.

Next recommended tasks:
- Implement `excel_reader` and `pdf_reader` sub-agents
- Build a small FastAPI endpoint to accept uploads and return normalized JSON
- Add frontend demo pages with animated processing states
