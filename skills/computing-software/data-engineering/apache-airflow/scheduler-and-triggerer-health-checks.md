---
id: computing-software.data-engineering.apache-airflow.scheduler-and-triggerer-health-checks
name: scheduler-and-triggerer-health-checks
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, scheduler-health-check, health-endpoint, liveness-probes, jobs-check]
level: practitioner
status: docs-checked
description: "Monitor Airflow component health: the API health endpoint, scheduler health check server, airflow jobs check for liveness probes, and alerting on stale heartbeats."
sources:
  - https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/logging-monitoring/check-health.html
  - https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#jobs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scheduler, triggerer and DAG processor health checks

**Goal:** detect a dead or stuck component in minutes, and let Kubernetes restart it.

## Health endpoint
- Airflow 3: `GET /api/v2/monitor/health` on the API server.
- Returns status and `latest_*_heartbeat` for metadatabase, scheduler, triggerer, dag_processor. A component is unhealthy when its heartbeat is older than its health-check threshold (for the scheduler, `[scheduler] scheduler_health_check_threshold`).
```bash
curl -s https://airflow.example.com/api/v2/monitor/health | jq
```

## Scheduler's own health server
```ini
[scheduler]
enable_health_check = True
scheduler_health_check_server_port = 8974
```
`GET http://scheduler:8974/health` returns 200/503: good for a liveness probe without touching the API server.

## CLI checks
```bash
airflow jobs check --job-type SchedulerJob --local
airflow jobs check --job-type TriggererJob --local
airflow jobs check --job-type DagProcessorJob --hostname "$(hostname)"
```
`airflow jobs check` checks whether matching jobs are still alive.

## Alerting
- External synthetic check on the health endpoint every minute.
- Metrics: `scheduler_heartbeat` (counter should increase), `dag_processing.last_duration`, `executor.open_slots`, `scheduler.tasks.starving`.
- Canary DAG: a tiny DAG scheduled every 5-10 minutes; alert if its last success is older than 2 intervals. It catches broken workers/queues that heartbeats miss.

## Gotchas
- `jobs check` hits the metadata DB; very frequent probes on many pods add DB load. Keep probe periods modest.
- A healthy heartbeat does not mean tasks run: workers can be down. That is what the canary DAG is for.

## Verify
Kill the scheduler pod: the health endpoint flips to unhealthy within the threshold and the probe restarts the pod.

## Checked

2026-10-28. Confirmed in the Airflow health-check page, configuration reference, CLI reference and metrics page: `/api/v2/monitor/health` and its JSON (`status`, `latest_scheduler_heartbeat`, triggerer), scheduler health server `enable_health_check` and port 8974 (503 when unhealthy), `airflow jobs check` and its `--job-type` values, `scheduler_heartbeat` metric. Removed: Airflow 2 `/health` placement, the scheduler threshold default, exit-code and Helm-probe claims, and the probe period figures.
Method: documentation only; no commands were run.
