---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.pushgateway-for-batch-jobs
name: pushgateway-for-batch-jobs
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, pushgateway, pushgateway-when-to-use, pushgateway-batch-jobs, batch-jobs, cron-metrics, push-metrics, push-to-gateway, honor-labels, push-time-seconds, service-level-batch, textfile-collector-alternative, pca]
level: practitioner
status: verified
description: "Decide when the Pushgateway is right (service-level batch jobs only), push metrics with curl or a client library, scrape it with honor_labels, and alert on stale pushes."
sources: ["https://prometheus.io/docs/practices/pushing/", "https://github.com/prometheus/pushgateway/blob/master/README.md", "https://prometheus.io/docs/instrumenting/pushing/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pushgateway for batch jobs

**Goal:** get metrics out of short-lived jobs that cannot be scraped, without turning the
Pushgateway into a general-purpose push endpoint that silently breaks `up`, staleness and
instance-level monitoring.

## 1. When to use it (and when not)
Use the Pushgateway **only** for *service-level* batch jobs: a job that is not tied to one
machine or instance (nightly ETL, a Kubernetes CronJob that may land anywhere). Don't use it for:
- machine-level cron (use node_exporter's **textfile collector** instead — see
  `node-exporter-collectors-and-textfile`);
- long-running services (scrape them; a push loses `up`, and the gateway becomes a SPOF);
- event logging (a push *replaces* the whole group; it is not a counter stream).

The Pushgateway never expires metrics. A job that stops running keeps reporting its last
values forever — your freshness check (section 4) is mandatory.

## 2. Push from the job
```bash
# curl: grouping key = job=nightly_export; the gateway stores instance="" (shown as instance="" in its /metrics)
cat <<EOF | curl --data-binary @- http://pushgateway:9091/metrics/job/nightly_export
# TYPE nightly_export_rows_processed gauge
nightly_export_rows_processed 128345
# TYPE nightly_export_last_success_timestamp_seconds gauge
nightly_export_last_success_timestamp_seconds $(date +%s)
EOF
```
Run against Pushgateway 1.11.4: HTTP 200, and `/metrics` then showed both metrics with `instance=""` and `job="nightly_export"` plus `push_time_seconds` and `push_failure_time_seconds` (0 after a good push) for the group. Python client (prometheus_client, run):
```python
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
reg = CollectorRegistry()
Gauge("nightly_export_last_success_timestamp_seconds", "", registry=reg).set_to_current_time()
push_to_gateway("pushgateway:9091", job="nightly_export", registry=reg)
```
HTTP verbs matter (run): `PUT` replaces every metric in the group (after `PUT ma, mb` then `POST ma` and `POST mc`, `ma` was updated and `mb`, `mc` kept; a following `PUT ma` left only `ma`), `POST` replaces only metrics with the same name, `DELETE` removes the group (HTTP 202). Use `POST` for jobs that push several
independent metrics at different times; use `PUT` when one push is the whole truth.

Extra grouping labels go in the URL path: `/metrics/job/nightly_export/region/eu` (run). Label
values with `/` must be base64-encoded with the `@base64` suffix: `/path@base64/L3Zhci9sb2c=` stored `path="/var/log"` (run); the same suffix works for `instance` and the other label names.

## 3. Scrape it with honor_labels
```yaml
scrape_configs:
  - job_name: pushgateway
    honor_labels: true          # keep job/instance from the pushed group
    static_configs:
      - targets: ["pushgateway:9091"]
```
Without `honor_labels: true` every pushed series gets the scrape job's `job` (and `instance` of the gateway) and the pushed `job` is renamed `exported_job` — the most common mistake. Run with a second scrape job named `pushgw_nohonor`: `ma{exported_job="verbs", instance="127.0.0.1:19091", job="pushgw_nohonor"}`, versus `ma{job="verbs"}` with `honor_labels: true`, where the empty pushed `instance` simply left no `instance` label. No `up` series exists for a pushed job (run: `up{job="verbs"}` empty).

## 4. Freshness alert
The gateway adds `push_time_seconds` and `push_failure_time_seconds` per group (both seen in the run):
```promql
time() - push_time_seconds{job="nightly_export"} > 26 * 3600
```
Alert on the age of the push, not on the job's own metrics, so a job that never runs is caught. The expression was evaluated in `promtool test rules` with `push_time_seconds` fixed at 1000: it returned 99000 at 100000 s and nothing at 90000 s (threshold 93600 s).

## 5. Operations
- Run with `--persistence.file=/data/pushgateway.data --persistence.interval=5m` (`--help`: the interval is the minimum time between writes, default 5m; with an empty file, metrics are only kept in memory) or a restart wipes every group. Run: with the file, 11 groups survived a restart; without it, a pushed group was gone after a restart.
- Clean up finished groups from the job (`curl -X DELETE …/metrics/job/<job>/…`) or via the
  admin API (`pushgateway-grouping-keys-and-admin-api`); otherwise retired jobs linger forever.
- The Prometheus pushing practices page lists the drawbacks: through one Pushgateway it is a single point of failure and a bottleneck, `up` is lost, and it never forgets series until they are deleted through its API (all three fetched from the page). Keep it to the service-level batch jobs described above.

## Gotchas
- Pushing a counter as a plain value and expecting `rate()` to work: the gateway exposes the
  pushed value as a constant between pushes. Run: after pushing `cnt_total 10` and waiting, `increase(cnt_total[20s])` was 0; after pushing `4`, `resets(...)` was 1 and `increase` was 5.33. Push gauges and timestamps.
- Pushing with `instance` set makes each run a new series when the hostname varies — leave
  `instance` empty for service-level jobs.
- `push_to_gateway` raises on connection errors (run: pushing to a closed port raised `URLError`); wrap it so a monitoring hiccup does not fail the job itself.

## Verify
- [ ] `curl pushgateway:9091/metrics | grep push_time_seconds` lists exactly the live jobs.
- [ ] In Prometheus, `nightly_export_rows_processed` has `job="nightly_export"`, not `exported_job`.
- [ ] The freshness alert fires when you stop the job for longer than its interval.

## Checked
Pushgateway 1.11.4 and Prometheus 3.15.1 (windows-amd64) run locally, prometheus_client in a venv: the curl push from the skill, the Python `push_to_gateway`, PUT/POST/DELETE semantics, extra grouping labels, `@base64` values, scrape with and without `honor_labels` (exported_job), `push_time_seconds`/`push_failure_time_seconds`, a counter pushed once and then lowered (increase and resets), persistence across a restart with and without `--persistence.file`.
