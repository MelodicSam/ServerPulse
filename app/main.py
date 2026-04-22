from __future__ import annotations

import os
from datetime import datetime
from flask import Flask, jsonify, render_template, request

from .logger_util import get_incidents, get_stats
from .monitor import perform_health_check
from .service_control import get_service_status, restart_service, get_recent_service_logs


app = Flask(__name__)
SERVICE_NAME = os.getenv('SERVICE_NAME', 'nginx')
HOSTNAME = os.getenv('SERVER_NAME', 'serverpulse-host')


@app.route('/')
def index():
    return render_template('index.html', service_name=SERVICE_NAME, hostname=HOSTNAME)


@app.route('/api/status')
def api_status():
    status = get_service_status(SERVICE_NAME)
    incidents = get_incidents(limit=10)
    stats = get_stats()
    payload = {
        'service_name': SERVICE_NAME,
        'hostname': HOSTNAME,
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'status': status,
        'stats': stats,
        'incidents': incidents,
    }
    return jsonify(payload)


@app.route('/api/check', methods=['POST'])
def api_check():
    result = perform_health_check(SERVICE_NAME)
    return jsonify(result)


@app.route('/api/restart', methods=['POST'])
def api_restart():
    reason = request.json.get('reason', 'Manual restart from dashboard') if request.is_json else 'Manual restart from dashboard'
    result = restart_service(SERVICE_NAME, reason=reason)
    return jsonify(result)


@app.route('/api/logs')
def api_logs():
    lines = int(request.args.get('lines', 25))
    logs = get_recent_service_logs(SERVICE_NAME, lines=lines)
    return jsonify({'service_name': SERVICE_NAME, 'logs': logs})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
