from __future__ import annotations

from .logger_util import log_incident
from .notifier import send_notification
from .service_control import get_service_status, restart_service


def perform_health_check(service_name: str) -> dict:
    status = get_service_status(service_name)
    if status['active']:
        return {
            'healthy': True,
            'message': f'{service_name} is active.',
            'status': status,
        }

    restart = restart_service(service_name, reason='Automatic recovery after failed health check')
    result_label = 'success' if restart.get('success') else 'failed'
    incident = log_incident(
        service=service_name,
        problem=f'Service inactive ({status.get("active_state")})',
        action='Attempted automatic restart',
        result='success' if restart.get('success') else 'failed',
        details=restart.get('message', ''),
    )

    notification = send_notification(
        title=f'ServerPulse alert: {service_name} recovered' if restart.get('success') else f'ServerPulse alert: {service_name} restart failed',
        message=(
            f'Problem: service became inactive.\n'
            f'Action: automatic restart attempt.\n'
            f'Result: {result_label}.\n'
            f'Incident ID: {incident["id"]}'
        ),
        severity='warning' if restart.get('success') else 'critical',
    )

    return {
        'healthy': False,
        'message': f'{service_name} was inactive. Recovery attempted.',
        'status_before': status,
        'restart_result': restart,
        'incident': incident,
        'notification': notification,
    }
