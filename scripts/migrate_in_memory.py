#!/usr/bin/env python3
"""CLI to migrate an exported in-memory approvals/audit dump into SQLite.

Usage examples:
  # from a JSON export produced earlier
  python3 scripts/migrate_in_memory.py --json data/in_memory_dump.json

  # from a running module that exposes `_STORE` and `_AUDIT` (must be importable)
  python3 scripts/migrate_in_memory.py --module myapp.runtime_state

The JSON format expected:
{
  "store": { "INV-1": [ { <step> }, ... ] },
  "audit": { "INV-1": [ { <audit entry> }, ... ] }
}
"""
from __future__ import annotations
import argparse
import importlib
import json
import sys
from typing import Tuple

def load_from_module(module_name: str) -> Tuple[dict, dict]:
    m = importlib.import_module(module_name)
    store = getattr(m, '_STORE', None)
    audit = getattr(m, '_AUDIT', None)
    if store is None and audit is None:
        raise ValueError(f"Module '{module_name}' has no _STORE or _AUDIT variables")
    return store or {}, audit or {}

def load_from_json(path: str) -> Tuple[dict, dict]:
    with open(path, 'r') as fh:
        data = json.load(fh)
    return data.get('store', {}), data.get('audit', {})

def main(argv=None):
    parser = argparse.ArgumentParser(description='Migrate in-memory approvals/audit to SQLite')
    parser.add_argument('--json', help='Path to JSON file containing store/audit')
    parser.add_argument('--module', help='Importable module path exposing _STORE and _AUDIT')
    args = parser.parse_args(argv)

    if not args.json and not args.module:
        parser.error('Provide either --json or --module')

    try:
        if args.module:
            store, audit = load_from_module(args.module)
        else:
            store, audit = load_from_json(args.json)
    except Exception as e:
        print('Error loading source:', e, file=sys.stderr)
        sys.exit(2)

    # import the new approvals module and call migration helper
    try:
        from app import approvals
    except Exception as e:
        print('Failed to import app.approvals:', e, file=sys.stderr)
        sys.exit(3)

    try:
        approvals.migrate_from_memory(store, audit)
    except Exception as e:
        print('Migration failed:', e, file=sys.stderr)
        sys.exit(4)

    total_invoices = len(store or {})
    total_steps = sum(len(v) for v in (store or {}).values())
    total_audit = sum(len(v) for v in (audit or {}).values())
    print(f'Migrated {total_invoices} invoices, {total_steps} steps, {total_audit} audit entries into data/approvals.db')

if __name__ == '__main__':
    main()
