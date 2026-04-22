from __future__ import annotations

import os
import requests

DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL', '')
TEAMS_WEBHOOK_URL = os.getenv('TEAMS_WEBHOOK_URL', '')
TIMEOUT = 10


def _post_json(url: str, payload: dict) -> tuple[bool, str]:
    try:
        response = requests.post(url, json=payload, timeout=TIMEOUT)
        if 200 <= response.status_code < 300:
            return True, f'Notification sent ({response.status_code}).'
        return False, f'Webhook returned {response.status_code}: {response.text[:300]}'
    except Exception as exc:
        return False, f'Notification error: {exc}'


def send_notification(title: str, message: str, severity: str = 'warning') -> dict:
    if DISCORD_WEBHOOK_URL:
        ok, status = _post_json(DISCORD_WEBHOOK_URL, {
            'username': 'ServerPulse',
            'content': f'**{title}**\n{message}\nSeverity: `{severity}`',
        })
        return {'sent': ok, 'provider': 'discord', 'status': status}

    if TEAMS_WEBHOOK_URL:
        ok, status = _post_json(TEAMS_WEBHOOK_URL, {
            '@type': 'MessageCard',
            '@context': 'https://schema.org/extensions',
            'summary': title,
            'themeColor': 'FFAA00' if severity == 'warning' else 'FF0000',
            'title': title,
            'text': message,
        })
        return {'sent': ok, 'provider': 'teams', 'status': status}

    return {'sent': False, 'provider': 'none', 'status': 'No webhook URL configured.'}
