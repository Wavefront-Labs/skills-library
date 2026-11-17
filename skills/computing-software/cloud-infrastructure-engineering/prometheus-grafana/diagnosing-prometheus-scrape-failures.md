---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.diagnosing-prometheus-scrape-failures
name: diagnosing-prometheus-scrape-failures
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [scrape-failure-diagnosis, context-deadline-exceeded, target-health-debugging, scrape-config, up-metric, prometheus-troubleshooting]
level: practitioner
status: docs-checked
description: "Map Prometheus target errors (context deadline exceeded, connection refused, 401/403/404, x509, sample limit) to causes and fixes, with curl checks from the server."
sources: ["https://prometheus.io/docs/prometheus/latest/configuration/configuration/#scrape_config", "https://prometheus.io/docs/concepts/jobs_instances/", "https://prometheus.io/docs/prometheus/latest/querying/api/#targets"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Diagnosing scrape failures

Start at Status > Targets (or `GET /api/v1/targets?state=active` and read `lastError`). Reproduce the scrape from the Prometheus host or pod with `curl` or `wget` against the target's metrics URL.

| lastError | Cause | Fix |
|---|---|---|
| `context deadline exceeded` | response slower than `scrape_timeout` (default 10s) | measure with `time curl`; speed up exporter, raise timeout (< interval), split job |
| `connection refused` | wrong port or process not listening on that interface | check port, bind address (`0.0.0.0` vs `127.0.0.1`) |
| `no such host` | DNS / SD giving stale names | check SD, CoreDNS |
| `i/o timeout` / `no route to host` | NetworkPolicy, security group, firewall | allow Prometheus source |
| `server returned HTTP status 401/403` | missing/wrong auth (or kubelet RBAC) | configure `authorization`/`basic_auth`, RBAC for `nodes/metrics` |
| `HTTP status 404` | wrong `metrics_path` | set path (`/actuator/prometheus`, `/metrics`) |
| `x509: certificate signed by unknown authority` / `cannot validate certificate for <ip>` | CA or SAN mismatch | `tls_config.ca_file`, `server_name`; `insecure_skip_verify` only temporarily |
| sample limit error | more samples than `sample_limit` after metric relabeling; the whole scrape fails | intended protection; fix target or raise limit |
| body size error | response larger than `body_size_limit` (experimental, 0 = no limit) | same |
| parse or content-type error | not a metrics endpoint, HTML login page, bad content type | fix path/auth; `fallback_scrape_protocol` |
| `server returned HTTP status 503` | target overloaded or not ready | target side |

## Queries
```promql
up == 0
avg_over_time(up[1h]) < 0.9          # flapping targets
scrape_duration_seconds > 5           # close to timeout
```

## Gotchas
- `scrape_timeout` cannot be greater than the scrape interval.
- An exporter that does live collection (DB queries) can be slow under load exactly when you need it: cache in the exporter.

## Checked
2026-10-31. Confirmed on the Prometheus scrape_config and HTTP API pages: `scrape_timeout` default 10s and cannot exceed the interval, `metrics_path` default `/metrics`, `body_size_limit` (experimental, 0 = no limit), `sample_limit` failing the whole scrape, `fallback_scrape_protocol`, `tls_config` `ca_file` and `server_name`, `/api/v1/targets?state=active` with `lastError`, `up` and `scrape_duration_seconds`. Removed: the kubectl example and exact error strings for limit and parse errors (not in the docs). Remaining error-text rows are Go net/http strings shown as typical symptoms, not Prometheus doc claims.
Method: documentation only; no commands were run.

## Verify
- [ ] `count(up == 0)` is 0 or every down target has a known reason.
- [ ] An alert on `up == 0` for important jobs exists (with `for: 5m`).
