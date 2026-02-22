from typing import Dict, List, Optional
from datetime import datetime
import sqlite3
import os
import json

# SQLite DB file (relative to repository cwd)
_DATA_DIR = os.path.join(os.getcwd(), 'data')
_DB_PATH = os.path.join(_DATA_DIR, 'approvals.db')


def _ensure_db():
    os.makedirs(_DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(_DB_PATH)
    cur = conn.cursor()
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS approvals (
            invoice_number TEXT,
            level INTEGER,
            approver_name TEXT,
            approver_role TEXT,
            status TEXT,
            assigned_at TEXT,
            actioned_at TEXT,
            actioned_by TEXT,
            notes TEXT,
            extra_json TEXT,
            PRIMARY KEY (invoice_number, level)
        )
        '''
    )
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS audit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_number TEXT,
            timestamp TEXT,
            level INTEGER,
            approver TEXT,
            actioned_by TEXT,
            status TEXT,
            notes TEXT
        )
        '''
    )
    conn.commit()
    conn.close()


def _row_to_step(row: sqlite3.Row) -> Dict:
    return {
        'invoice_number': row['invoice_number'],
        'level': row['level'],
        'approver_name': row['approver_name'],
        'approver_role': row['approver_role'],
        'status': row['status'],
        'assigned_at': row['assigned_at'],
        'actioned_at': row['actioned_at'],
        'actioned_by': row['actioned_by'],
        'notes': row['notes'],
        'extra': json.loads(row['extra_json']) if row['extra_json'] else {},
    }


def register_approvals(invoice_number: str, steps: List[Dict]) -> None:
    """Store approval steps for an invoice into SQLite. Replaces any existing steps."""
    _ensure_db()
    conn = sqlite3.connect(_DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    # delete existing for this invoice
    cur.execute('DELETE FROM approvals WHERE invoice_number = ?', (invoice_number,))
    for s in steps:
        status = s.get('status', 'Pending')
        assigned_at = s.get('assigned_at') or (datetime.utcnow().isoformat() + 'Z')
        actioned_at = s.get('actioned_at') if status == 'Completed' else None
        extra = {k: v for k, v in s.items() if k not in ('level', 'approver_name', 'approver_role', 'status', 'assigned_at', 'actioned_at', 'actioned_by', 'notes')}
        cur.execute(
            '''INSERT OR REPLACE INTO approvals
               (invoice_number, level, approver_name, approver_role, status, assigned_at, actioned_at, actioned_by, notes, extra_json)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (
                invoice_number,
                int(s.get('level', 0)),
                s.get('approver_name'),
                s.get('approver_role'),
                status,
                assigned_at,
                actioned_at,
                s.get('actioned_by'),
                s.get('notes'),
                json.dumps(extra) if extra else None,
            ),
        )
    conn.commit()
    conn.close()


def get_audit(invoice_number: str) -> List[Dict]:
    _ensure_db()
    conn = sqlite3.connect(_DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT timestamp, level, approver, actioned_by, status, notes FROM audit WHERE invoice_number = ? ORDER BY id ASC', (invoice_number,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_approvals(invoice_number: str) -> Optional[List[Dict]]:
    _ensure_db()
    conn = sqlite3.connect(_DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT * FROM approvals WHERE invoice_number = ? ORDER BY level ASC', (invoice_number,))
    rows = cur.fetchall()
    conn.close()
    return [_row_to_step(r) for r in rows] if rows else None


def update_approval(invoice_number: str, level: int, status: str, actioned_by: Optional[str] = None, notes: Optional[str] = None) -> Optional[Dict]:
    _ensure_db()
    conn = sqlite3.connect(_DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    actioned_at = datetime.utcnow().isoformat() + 'Z'
    cur.execute(
        'UPDATE approvals SET status = ?, actioned_at = ?, actioned_by = ?, notes = ? WHERE invoice_number = ? AND level = ?',
        (status, actioned_at, actioned_by, notes, invoice_number, int(level)),
    )
    if cur.rowcount == 0:
        conn.commit()
        conn.close()
        return None
    # insert audit entry
    cur.execute(
        'INSERT INTO audit (invoice_number, timestamp, level, approver, actioned_by, status, notes) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (invoice_number, actioned_at, int(level), None, actioned_by, status, notes),
    )
    conn.commit()
    # fetch updated row
    cur.execute('SELECT * FROM approvals WHERE invoice_number = ? AND level = ?', (invoice_number, int(level)))
    row = cur.fetchone()
    conn.close()
    return _row_to_step(row) if row else None


def migrate_from_memory(store: Dict[str, List[Dict]], audit: Dict[str, List[Dict]]) -> None:
    """Utility to migrate existing in-memory structures into the SQLite DB.

    Call this from a running process if you have `_STORE` and `_AUDIT` retained in memory and want to persist them.
    """
    _ensure_db()
    for inv, steps in (store or {}).items():
        register_approvals(inv, steps)
    # write audits
    conn = sqlite3.connect(_DB_PATH)
    cur = conn.cursor()
    for inv, entries in (audit or {}).items():
        for e in entries:
            cur.execute(
                'INSERT INTO audit (invoice_number, timestamp, level, approver, actioned_by, status, notes) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (
                    inv,
                    e.get('timestamp'),
                    e.get('level'),
                    e.get('approver'),
                    e.get('actioned_by'),
                    e.get('status'),
                    e.get('notes'),
                ),
            )
    conn.commit()
    conn.close()

