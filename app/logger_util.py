from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).resolve().parent / 'data'
INCIDENTS_FILE = DATA_DIR / 'incidents.json'


DATA_DIR.mkdir(parents=True, exist_ok=True)
if not INCIDENTS_FILE.exists():
    INCIDENTS_FILE.write_text('[]', encoding='utf-8')


def _load() -> list[dict]:
    try:
        return json.loads(INCIDENTS_FILE.read_text(encoding='utf-8'))
    except Exception:
        return []


def _save(data: list[dict]) -> None:
    INCIDENTS_FILE.write_text(json.dumps(data, indent=2), encoding='utf-8')


def log_incident(service: str, problem: str, action: str, result: str, details: str = '') -> dict:
    data = _load()
    entry = {
        'id': len(data) + 1,
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'service': service,
        'problem': problem,
        'action': action,
        'result': result,
        'details': details[:2000],
    }
    data.insert(0, entry)
    _save(data)
    return entry


def get_incidents(limit: int | None = None) -> list[dict]:
    data = _load()
    return data[:limit] if limit else data


def get_stats() -> dict:
    items = _load()
    total = len(items)
    recovered = sum(1 for x in items if x.get('result', '').lower() == 'success')
    failed = total - recovered
    latest = items[0]['timestamp'] if items else None
    return {
        'total_incidents': total,
        'successful_recoveries': recovered,
        'failed_recoveries': failed,
        'latest_incident_at': latest,
    }
