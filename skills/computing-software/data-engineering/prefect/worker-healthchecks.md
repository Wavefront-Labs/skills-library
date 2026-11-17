---
id: computing-software.data-engineering.prefect.worker-healthchecks
name: worker-healthchecks
category: computing-software
field: data-engineering
product: prefect
tags: [healthcheck, worker, probe, liveness, docker]
level: practitioner
status: docs-checked
description: "Enable the Prefect worker health endpoint with --with-healthcheck, interpret 200 and 503 responses, and wire Docker, Compose and Kubernetes probes."
sources:
  - https://docs.prefect.io/v3/advanced/worker-healthchecks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let an orchestrator restart a stuck worker.

```bash
prefect worker start --pool "my-pool" --with-healthcheck
```

Endpoint: `/health` on `0.0.0.0:8080` by default (`http://localhost:8080/health`). Change with `PREFECT_WORKER_WEBSERVER_HOST` and `PREFECT_WORKER_WEBSERVER_PORT`.

Responses to GET:
- 200 `{"message": "OK"}` when healthy
- 503 `{"message": "Worker may be unresponsive at this time"}` when unhealthy

Unhealthy means no successful poll within `PREFECT_WORKER_QUERY_SECONDS * 30` seconds (300 seconds by default). On Prefect Cloud, a `Prefect-Maintenance: true` header makes the worker wait out `Retry-After`, so it stays healthy during maintenance.

Docker:

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD python -c "import urllib.request as u; u.urlopen('http://localhost:8080/health', timeout=1)"
```

Kubernetes liveness probe (enabled by default in the Prefect Helm chart):

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 60
  periodSeconds: 30
  timeoutSeconds: 10
  failureThreshold: 3
```

Docker Compose uses the same Python one-liner in `healthcheck.test` with the same interval, timeout, retries and start_period.

Related: `PREFECT_WORKER_HEARTBEAT_SECONDS` (default 30), `PREFECT_WORKER_PREFETCH_SECONDS` (default 10).

## Checked
2026-11-08. Confirmed against the worker healthchecks page: --with-healthcheck, /health on 0.0.0.0:8080, host and port settings, 200 and 503 bodies, the PREFECT_WORKER_QUERY_SECONDS * 30 rule (300 seconds), Prefect-Maintenance handling, Docker, Compose and Kubernetes probe values, Helm default, and heartbeat and prefetch defaults. Nothing removed.
Method: documentation only; no commands were run.
