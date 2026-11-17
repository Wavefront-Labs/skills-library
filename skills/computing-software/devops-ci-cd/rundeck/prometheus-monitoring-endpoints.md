---
id: computing-software.devops-ci-cd.rundeck.prometheus-monitoring-endpoints
name: prometheus-monitoring-endpoints
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, prometheus, monitoring-endpoints, metrics, jmx-export]
level: practitioner
status: docs-checked
description: "Scrape Rundeck 6 metrics with Prometheus from /monitoring/prometheus, use the health and info endpoints, and troubleshoot 404 or stale metrics."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/administration/monitoring/monitoring.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Endpoints (modern ones need Rundeck 6.0 or later):
- `/monitoring/prometheus`: Prometheus text format
- `/monitoring/metrics` lists metric names; `/monitoring/metrics/{name}` gives one
- `/monitoring/health`: `{"status":"UP"}` or `DOWN`; suited to load balancer checks
- `/monitoring/info`: app name and version
- `/monitoring/threaddump`: JVM thread dump

Prometheus scrape config:

```yaml
scrape_configs:
  - job_name: 'rundeck'
    scrape_interval: 30s
    metrics_path: '/monitoring/prometheus'
    static_configs:
      - targets: ['rundeck.example.com:4440']
```

Useful series include `jvm.memory.used`, `jvm.threads.live`, `system.cpu.usage`, `executor.queued`, and execution metrics such as `rundeck_executions_total`, `rundeck_executions_running`.

HAProxy check: `option httpchk GET /monitoring/health` plus `http-check expect status 200`.

Through the API (authenticated), `/api/25/monitoring/*` forwards to these endpoints.

Troubleshooting:
- 404: confirm `rundeck.metrics.monitoring.enabled=true`, the correct path, and Rundeck 6.0+.
- Stale metrics: `rundeck.metrics.enabled=true` is the master switch. JMX also needs `rundeck.metrics.jmxEnabled=true` and a restart.
- Health DOWN: check logs, database connectivity, memory and disk, and the thread dump.

## Checked

2026-11-04: endpoints, scrape config, metric names, HAProxy check, API forwarding path and troubleshooting steps confirmed against the Using Monitoring Data page.
Method: documentation only; no commands were run.
