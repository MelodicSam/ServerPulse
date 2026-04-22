from __future__ import annotations

import os
import subprocess
from datetime import datetime

SYSTEMCTL_BIN = os.getenv('SYSTEMCTL_BIN', 'systemctl')
JOURNALCTL_BIN = os.getenv('JOURNALCTL_BIN', 'journalctl')
ALLOW_REAL_CONTROL = os.getenv('ALLOW_REAL_CONTROL', 'true').lower() == 'true'


def _run_command(command: list[str]) -> tuple[bool, str]:
    try:
        completed = subprocess.run(command, capture_output=True, text=True, timeout=20, check=False)
        output = (completed.stdout or '') + (completed.stderr or '')
        return completed.returncode == 0, output.strip()
    except FileNotFoundError:
        return False, f'Command not found: {command[0]}'
    except subprocess.TimeoutExpired:
        return False, 'Command timed out.'
    except Exception as exc:
        return False, f'Unexpected error: {exc}'


def get_service_status(service_name: str) -> dict:
    active_ok, active_out = _run_command([SYSTEMCTL_BIN, 'is-active', service_name])
    enabled_ok, enabled_out = _run_command([SYSTEMCTL_BIN, 'is-enabled', service_name])
    status_ok, status_out = _run_command([SYSTEMCTL_BIN, 'status', service_name, '--no-pager', '--lines=10'])

    active_state = active_out.splitlines()[0] if active_out else 'unknown'
    enabled_state = enabled_out.splitlines()[0] if enabled_out else 'unknown'

    return {
        'service': service_name,
        'active': active_ok and active_state == 'active',
        'active_state': active_state,
        'enabled_state': enabled_state,
        'checked_at': datetime.utcnow().isoformat() + 'Z',
        'summary': status_out[:2000],
        'status_ok': status_ok,
    }


def restart_service(service_name: str, reason: str = 'Automatic recovery') -> dict:
    if not ALLOW_REAL_CONTROL:
        return {
            'success': False,
            'message': 'Service control is disabled by ALLOW_REAL_CONTROL=false.',
            'service': service_name,
            'reason': reason,
        }

    ok, output = _run_command(['sudo', SYSTEMCTL_BIN, 'restart', service_name])
    after = get_service_status(service_name)
    return {
        'success': ok and after['active'],
        'message': output[:2000],
        'service': service_name,
        'reason': reason,
        'post_restart_status': after,
    }


def get_recent_service_logs(service_name: str, lines: int = 25) -> list[str]:
    ok, output = _run_command([JOURNALCTL_BIN, '-u', service_name, '-n', str(lines), '--no-pager'])
    if not ok and not output:
        return ['Unable to read journal logs.']
    return output.splitlines()[-lines:]
