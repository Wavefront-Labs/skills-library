---
id: computing-software.devops-ci-cd.gitlab-ci.runner-prometheus-metrics
name: runner-prometheus-metrics
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, runner-metrics, runner-prometheus, listen-address, runner-alerts]
level: advanced
status: docs-checked
description: "Expose GitLab Runner metrics on listen_address, scrape them with Prometheus (or the Helm chart ServiceMonitor), and alert on saturation, errors and job failures."
sources: ["https://docs.gitlab.com/runner/monitoring/", "https://docs.gitlab.com/runner/install/kubernetes/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Runner metrics with Prometheus

## 1. Enable
```toml
# config.toml (global section)
listen_address = ":9252"
concurrent = 20
```
Helm chart:
```yaml
metrics:
  enabled: true
  serviceMonitor: { enabled: true }      # Prometheus Operator
service:
  enabled: true
```
Check: `curl -s localhost:9252/metrics | grep gitlab_runner_`.

## 2. Metrics that matter
| Metric | Use |
|---|---|
| `gitlab_runner_jobs_running_total` vs `gitlab_runner_concurrent` | saturation (the `concurrent` setting) |
| `gitlab_runner_limit` | per-runner `limit` setting |
| `gitlab_runner_request_concurrency_exceeded_total` | excess requests above the configured `request_concurrency` |
| `gitlab_runner_errors_total` | caught runner errors |
| `gitlab_runner_api_request_statuses_total{endpoint,status}` | auth/token problems with GitLab |
| `gitlab_runner_version_info` | fleet version drift |

## 3. Alerts
```promql
# runner cannot talk to GitLab
increase(gitlab_runner_api_request_statuses_total{status=~"401|403|5.."}[10m]) > 0
```

## Gotchas
- `listen_address = ":9252"` listens on all interfaces (`localhost:9252` only on loopback); with no port it defaults to 9252. Restrict network access to the port.

## Verify
- [ ] Grafana panel shows `gitlab_runner_jobs_running_total` against `gitlab_runner_concurrent` per runner.

## Checked

2026-10-31. Confirmed against the GitLab Runner monitoring page (embedded Prometheus metrics, `listen_address` global option, default port 9252, `:9252` versus `localhost:9252`, the Helm metrics block with `enabled`, `port` 9252 and `serviceMonitor`, and the metric names gitlab_runner_concurrent, gitlab_runner_limit, gitlab_runner_request_concurrency_exceeded_total, gitlab_runner_errors_total, gitlab_runner_api_request_statuses_total, gitlab_runner_version_info and gitlab_runner_jobs_running_total).
Removed: gitlab_runner_jobs{state}, gitlab_runner_failed_jobs_total, gitlab_runner_job_duration_seconds_bucket, the saturation and system-failure alert expressions, the errors_total level label, the admin UI and runner-jobs API queue-time section, and the autoscaled-machines gotcha, none of which appear in the fetched pages.

Method: documentation only; no commands were run.
