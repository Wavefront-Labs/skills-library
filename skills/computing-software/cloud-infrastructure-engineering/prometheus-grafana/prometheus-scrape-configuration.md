---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.prometheus-scrape-configuration
name: prometheus-scrape-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, scrape-config, scrape-configs, scrape-interval, scrape-timeout, metrics-path, static-configs, honor-labels, honor-timestamps, sample-limit, label-limit, body-size-limit, promtool-check-config, config-reload, lifecycle-api, global-config, external-labels, scrape-protocols, targets-page, pca]
level: practitioner
status: verified
description: "Write and safely reload prometheus.yml scrape_configs: intervals, timeouts, auth, honor_labels, per-scrape limits, external_labels, promtool checks and the /targets page as truth."
sources: ["https://prometheus.io/docs/prometheus/latest/configuration/configuration/", "https://prometheus.io/docs/prometheus/latest/management_api/", "https://prometheus.io/docs/prometheus/latest/getting_started/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prometheus scrape configuration

**Goal:** a `prometheus.yml` whose scrape jobs are correct on first reload, protected by
limits, and verifiable from the `/targets` page. Service discovery and relabeling are in
`...prometheus-grafana.prometheus-service-discovery-and-relabeling`.

## 1. Skeleton
```yaml
global:
  scrape_interval: 30s        # default for every job; 15s–60s is normal
  scrape_timeout: 10s         # must be <= scrape_interval
  evaluation_interval: 30s    # rule evaluation cadence
  external_labels:            # attached on federation/remote_write/alerts, NOT to local series
    cluster: prod-eu1
    replica: a                # differs per HA replica; Thanos/Mimir dedupe on it
rule_files: ["rules/*.yml"]
alerting:
  alertmanagers:
    - static_configs: [{ targets: ["am-0:9093", "am-1:9093", "am-2:9093"] }]
scrape_configs:
  - job_name: prometheus
    static_configs: [{ targets: ["localhost:9090"] }]
  - job_name: node
    scrape_interval: 15s
    metrics_path: /metrics
    scheme: http
    static_configs:
      - targets: ["node-a:9100", "node-b:9100"]
        labels: { env: prod }
  - job_name: app
    scheme: https
    tls_config: { ca_file: /etc/prometheus/ca.pem, insecure_skip_verify: false }
    authorization: { type: Bearer, credentials_file: /etc/prometheus/secrets/app-token }
    sample_limit: 50000       # drop the WHOLE scrape if exceeded (scrape fails, up=0)
    label_limit: 30
    label_name_length_limit: 200
    label_value_length_limit: 1024
    body_size_limit: 50MB
    target_limit: 500
    honor_labels: false       # true only for Pushgateway/federation
    honor_timestamps: true
    static_configs: [{ targets: ["app:8443"] }]
```

## 2. Settings that bite
- `job` and `instance` labels are set automatically; `instance` defaults to `host:port`.
  If the target already exposes `job`/`instance`, they become `exported_job`/`exported_instance`
  unless `honor_labels: true`.
- `scrape_timeout` greater than `scrape_interval` is rejected at load (equal is accepted). Slow exporters (SNMP, large
  kube-state-metrics) need their own job with a longer interval and timeout.
- `sample_limit` fails the whole scrape rather than truncating; you get `up=0` and
  `scrape_samples_post_metric_relabeling` stops rising. Prefer `metric_relabel_configs`
  drops for known-noisy metrics, keep the limit as the circuit breaker.
- `external_labels` are not visible in local queries; forgetting `replica` breaks HA
  dedup in Thanos/Mimir, forgetting `cluster` makes multi-cluster dashboards useless.
- `params:` passes query params (`module: [http_2xx]` for blackbox_exporter).
- `scrape_protocols: [OpenMetricsText1.0.0, PrometheusText0.0.4]` controls content
  negotiation; `PrometheusProto` is needed for native histograms.
- Secrets: use `*_file` variants (`credentials_file`, `password_file`); plain values show up
  in `/config` masked but live in git.

## 3. Validate, then reload
```bash
promtool check config prometheus.yml          # syntax + referenced files exist
promtool check rules rules/*.yml
# reload without restart (needs --web.enable-lifecycle)
curl -X POST http://localhost:9090/-/reload
# or: kill -HUP $(pidof prometheus)
curl -s localhost:9090/api/v1/status/config | jq -r .data.yaml | head
```
A failed reload (HTTP 500 from `/-/reload`, with the parse error in the body) keeps the **old** config running and logs the error; check
`prometheus_config_last_reload_successful == 1` and alert on it.

## 4. Read the targets page like an operator
`/targets` (or `curl localhost:9090/api/v1/targets | jq '.data.activeTargets[] | {job: .labels.job, health, lastError}'`):
- `context deadline exceeded` → raise `scrape_timeout` or fix the exporter.
- `server returned HTTP status 401/403` → auth config. A wrong `scheme` shows as `tls: first record does not look like a TLS handshake` (https to an http port).
- `sample limit exceeded` → see above.
- `expected a valid start token` → target is serving HTML (wrong `metrics_path`).
Per-scrape meta metrics: `scrape_duration_seconds`, `scrape_samples_scraped`,
`scrape_samples_post_metric_relabeling`, `scrape_series_added`, `up`.

## 5. Useful alerts on the scrape pipeline
```yaml
- alert: TargetDown
  expr: up == 0
  for: 5m
- alert: ScrapeSlow
  expr: scrape_duration_seconds > 0.8 * scrape_timeout_seconds   # scrape_timeout_seconds exists only with extra_scrape_metrics: true (global or per job; absent by default on 3.15.1); else hardcode the timeout
  for: 10m
- alert: PrometheusConfigReloadFailed
  expr: prometheus_config_last_reload_successful == 0
```

## Verify
- [ ] `promtool check config` passes in CI before any deploy.
- [ ] `/targets` shows every job `UP` with `scrape_duration_seconds` well under timeout.
- [ ] `external_labels` include a per-replica label if you run HA pairs.
- [ ] No credentials inline in `prometheus.yml`.
