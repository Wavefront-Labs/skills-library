---
id: computing-software.devops-ci-cd.semaphore-ui.prometheus-metrics
name: prometheus-metrics
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [metrics, prometheus, grafana, monitoring, observability, semaphore-ui]
level: practitioner
status: docs-checked
description: "Expose GET /api/metrics for Prometheus (v2.20+) with Basic Auth and read task counters."
sources:
  - https://semaphoreui.com/docs/admin-guide/metrics
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Prometheus metrics

Goal: monitor Semaphore with Prometheus and Grafana (version 2.20 or later).

Endpoint: `GET /api/metrics`, Prometheus text format, disabled by default, Basic Auth with a static service credential unrelated to user accounts.

```json
{
  "metrics": { "enabled": true, "username": "prometheus", "password": "changeme" }
}
```

Variables: `SEMAPHORE_METRICS_ENABLED`, `SEMAPHORE_METRICS_USERNAME`, `SEMAPHORE_METRICS_PASSWORD`. If disabled or credentials are wrong or missing, the endpoint returns 401.

Metrics:
- Go runtime and process metrics (goroutines, memory, CPU, GC).
- `semaphore_tasks_running` gauge: tasks running now.
- `semaphore_tasks_total{status}` counter: finished tasks by `success`, `error`, `stopped`.

They update at the moment a task changes state, with no polling delay.

Scrape job:

```yaml
scrape_configs:
  - job_name: semaphore
    metrics_path: /api/metrics
    basic_auth:
      username: prometheus
      password: changeme
    static_configs:
      - targets: ["semaphore.example.com:3000"]
```

Verify: run a PromQL query for `semaphore_tasks_running` (the page uses Grafana Explore for this).

## Checked

2026-11-07. Read in full: the Metrics page, from its markdown source in the semaphore-docs repository (admin-guide/metrics.md; no snippet files). Confirmed: version 2.20, GET /api/metrics, disabled by default with Basic Auth, the three variables, 401 behaviour, the two task metrics and the status values, real-time updates, and the scrape job. Removed: the `scheme: https` tip, the example alert expression, and the curl Verify step, none of which the page states.
Method: documentation only; no commands were run.
