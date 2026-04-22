<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=260&section=header&text=ServerPulse&fontSize=65&fontAlignY=38&desc=Nginx%Healing%Server=%%7C%20%20%7C%20%20&descAlignY=62&animation=fadeIn&color=0:020617,25:0f172a,55:0ea5e9,100:22d3ee"/>

**ServerPulse** is a self-healing server dashboard for Linux services. It monitors a service such as **Nginx**, shows its live status in a web dashboard, attempts recovery when the service fails, records incidents, and can send Discord or Teams notifications.

## Features

- Live dashboard for Linux service health
- Manual health check and restart actions
- Automatic recovery workflow
- Incident logging with timestamps
- Recent service log viewer
- Discord or Teams webhook alert support
- Dockerized setup for easy deployment

## Project Structure

```text
ServerPulse/
├── app/
│   ├── main.py
│   ├── monitor.py
│   ├── notifier.py
│   ├── logger_util.py
│   ├── service_control.py
│   ├── templates/
│   │   └── index.html
│   ├── static/
│   │   ├── style.css
│   │   └── main.js
│   └── data/
│       └── incidents.json
├── scripts/
│   └── start.sh
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

## How it Works

1. The dashboard checks the service status using `systemctl`.
2. If the service is healthy, it displays the current state.
3. If the service becomes inactive, ServerPulse can attempt a restart.
4. Every incident is saved to `incidents.json`.
5. A Discord or Teams webhook can be used to send alerts.

## Important Note About Docker

Because `systemctl` controls services on the **host OS**, the default Docker Compose setup runs with:

- `ALLOW_REAL_CONTROL=false`

That keeps the dashboard safe for demo use.

### Recommended ways to use this project

#### Demo mode
Use Docker and show the dashboard UI, logging structure, and project design.

#### Real recovery mode on a Linux VM
Run the Flask app directly on your Ubuntu/Rocky VM, or adjust the container to use privileged access and host mounts if you fully understand the security implications.

## Quick Start (Demo Mode)

```bash
git clone https://github.com/YOUR-USERNAME/ServerPulse.git
cd ServerPulse
docker compose up --build
```

Open:

```text
http://localhost:5000
```

## Run Without Docker on Linux VM

```bash
git clone https://github.com/YOUR-USERNAME/ServerPulse.git
cd ServerPulse
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export SERVICE_NAME=nginx
export SERVER_NAME=$(hostname)
export ALLOW_REAL_CONTROL=true
python -m flask --app app.main run --host=0.0.0.0 --port=5000
```

## API Endpoints

- `GET /api/status` → current service state, incidents, and stats
- `POST /api/check` → run health check and recovery attempt if needed
- `POST /api/restart` → manually restart the service
- `GET /api/logs` → show recent `journalctl` logs

## Environment Variables

| Variable | Purpose |
|---|---|
| `SERVICE_NAME` | Service to monitor, for example `nginx` |
| `SERVER_NAME` | Host label shown in the dashboard |
| `ALLOW_REAL_CONTROL` | Enable or disable real restart actions |
| `DISCORD_WEBHOOK_URL` | Discord webhook for alerts |
| `TEAMS_WEBHOOK_URL` | Teams webhook for alerts |

## Suggested Demo for GitHub README / Video

1. Show the dashboard running.
2. Open the incident table and recent logs area.
3. Run a manual check.
4. Explain that in safe demo mode, restart actions are disabled.
5. On your Linux VM, switch `ALLOW_REAL_CONTROL=true` and show a real restart test.
6. Capture a Discord or Teams alert screenshot.

## Good GitHub Description

> Dockerized self-healing Linux service dashboard with monitoring, incident logging, restart workflows, and webhook alerts.

## Future Improvements

- Add SQLite instead of JSON logging
- Add login authentication
- Monitor multiple services
- Add CPU and RAM usage cards
- Add charts for uptime history
- Add email alerts

## License

MIT
