---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-prometheus-metrics
name: woodpecker-prometheus-metrics
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [prometheus, metrics, monitoring]
level: advanced
status: docs-checked
description: "Expose Woodpecker Prometheus metrics with an auth token or an unprotected metrics port."
sources: ["https://woodpecker-ci.org/docs/administration/configuration/server"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker Prometheus metrics

The server exposes `/metrics` for Prometheus only when `WOODPECKER_PROMETHEUS_AUTH_TOKEN` is set (or `WOODPECKER_PROMETHEUS_AUTH_TOKEN_FILE`). Access then requires that token as a bearer token. An administrator generates a user API token and puts it in Prometheus:

```yaml
scrape_configs:
  - job_name: 'woodpecker'
    bearer_token: dummyToken...
    static_configs:
      - targets: ['woodpecker.domain.com']
```

Use `bearer_token_file: /etc/secrets/woodpecker-monitoring-token` to read the token from a file.

Unprotected alternative: `WOODPECKER_METRICS_SERVER_ADDR=:9001` starts a separate unprotected endpoint. Empty (default) disables it. Keep it off the public network.

Documented metrics include `woodpecker_pipeline_count`, `woodpecker_pipeline_time`, `woodpecker_pipeline_total_count`, `woodpecker_pending_steps`, `woodpecker_running_steps`, `woodpecker_waiting_steps`, `woodpecker_repo_count`, `woodpecker_user_count`, `woodpecker_worker_count`, `woodpecker_step_failures_total` and the histogram `woodpecker_step_duration_seconds`.

Step-level metrics (failure counters and duration histograms) are exported unless `WOODPECKER_STEP_LEVEL_METRICS` is disabled. It defaults to true.

On Kubernetes, the Helm chart can enable the `/metrics` endpoint on port 9001 without authentication; the port is not exposed externally by default.

A scrape without the bearer token is rejected, so confirm the token belongs to an administrator account. Use the unprotected metrics address only on a private interface.

## Checked

2026-11-03. Read the Woodpecker server configuration page and Helm chart page and confirmed the /metrics endpoint requiring WOODPECKER_PROMETHEUS_AUTH_TOKEN, bearer_token and bearer_token_file examples, METRICS_SERVER_ADDR example :9001, the listed metric names, STEP_LEVEL_METRICS and the Helm chart port 9001. Removed: the PodMonitor claim and the alerting advice, which the pages do not state. 

Method: documentation only; no commands were run.
