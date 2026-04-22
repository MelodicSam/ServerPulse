async function fetchJson(url, options = {}) {
  const response = await fetch(url, options);
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response.json();
}

function setStatus(status) {
  const badge = document.getElementById('statusBadge');
  const text = document.getElementById('statusText');

  if (status.active) {
    badge.className = 'badge healthy';
    badge.textContent = 'Healthy';
    text.textContent = `${status.service} is ${status.active_state}. Enabled: ${status.enabled_state}.`;
  } else {
    badge.className = 'badge down';
    badge.textContent = 'Down / Unhealthy';
    text.textContent = `${status.service} is ${status.active_state}. Enabled: ${status.enabled_state}.`;
  }
}

function setStats(stats) {
  document.getElementById('totalIncidents').textContent = stats.total_incidents ?? 0;
  document.getElementById('successfulRecoveries').textContent = stats.successful_recoveries ?? 0;
  document.getElementById('failedRecoveries').textContent = stats.failed_recoveries ?? 0;
  document.getElementById('latestIncident').textContent = stats.latest_incident_at ?? 'None';
}

function setIncidents(incidents) {
  const body = document.getElementById('incidentTableBody');
  body.innerHTML = '';

  if (!incidents || incidents.length === 0) {
    body.innerHTML = '<tr><td colspan="5">No incidents recorded yet.</td></tr>';
    return;
  }

  for (const item of incidents) {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${item.timestamp}</td>
      <td>${item.service}</td>
      <td>${item.problem}</td>
      <td>${item.action}</td>
      <td>${item.result}</td>
    `;
    body.appendChild(row);
  }
}

function setLogs(logs) {
  document.getElementById('logViewer').textContent = logs.join('\n');
}

function setLastUpdated() {
  document.getElementById('lastUpdated').textContent = `Last updated: ${new Date().toLocaleString()}`;
}

async function loadAll() {
  try {
    const statusData = await fetchJson('/api/status');
    const logData = await fetchJson('/api/logs');
    setStatus(statusData.status);
    setStats(statusData.stats);
    setIncidents(statusData.incidents);
    setLogs(logData.logs);
    setLastUpdated();
  } catch (error) {
    console.error(error);
    alert('Could not load dashboard data. Check console or server logs.');
  }
}

async function runCheck() {
  try {
    const result = await fetchJson('/api/check', { method: 'POST' });
    alert(result.message || 'Check completed.');
    await loadAll();
  } catch (error) {
    console.error(error);
    alert('Health check failed.');
  }
}

async function manualRestart() {
  try {
    const result = await fetchJson('/api/restart', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reason: 'Manual restart triggered from dashboard' })
    });
    alert(result.success ? 'Restart successful.' : 'Restart attempted but service may still be down.');
    await loadAll();
  } catch (error) {
    console.error(error);
    alert('Restart request failed.');
  }
}

loadAll();
setInterval(loadAll, 15000);
