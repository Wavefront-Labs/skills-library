---
id: computing-software.systems-network-administration.uptime-kuma.uptime-kuma-prometheus-metrics-and-api-keys
name: uptime-kuma-prometheus-metrics-and-api-keys
category: computing-software
field: systems-network-administration
product: uptime-kuma
tags: [prometheus, metrics-endpoint, api-keys, monitor-status, monitor-response-time, scrape-config, basic-auth]
level: advanced
status: docs-checked
description: "Scrape Uptime Kuma /metrics with Prometheus using basic auth or API keys, and query monitor_status and response time."
sources: ["https://github.com/louislam/uptime-kuma/wiki/Prometheus-Integration", "https://github.com/louislam/uptime-kuma/wiki/Prometheus-API-Keys"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Prometheus metrics and API keys

Metrics are served at `http://<host>:<port>/metrics` in Prometheus exporter format. Labels: `monitor_name`, `monitor_type`, `monitor_url`, `monitor_hostname`, `monitor_port`. Main series: `monitor_status` and `monitor_response_time`.

Scrape config (basic auth is on by default):

```yaml
- job_name: "uptime"
  scrape_interval: 30s
  scheme: http
  metrics_path: "/metrics"
  static_configs:
      - targets: ["uptime-kuma.url"]
  basic_auth:
      username: <your user>
      password: <your password>
```

API keys (since 1.21.0): create under Settings, API Keys with a name and expiry or no expiry. The key is shown once. The moment you add the first key, basic auth for the endpoint is permanently disabled. Keys can be disabled temporarily; expired keys are kept (to help debugging) until you delete them. Authenticate with an empty username: `curl -u":<key>" uptime.kuma/metrics`, and in Prometheus set only `basic_auth.password: <api key>`. A key cannot be used for the rest of the web interface.

PromQL examples: `sum(monitor_response_time) by (monitor_name)`, `monitor_status{monitor_name="Google"}`.

## Checked

2026-11-04. Confirmed against the Uptime Kuma wiki: Prometheus Integration and Prometheus API Keys pages (endpoint, labels, scrape config, 1.21.0, key behaviour, curl form). Removed: The generic verify line.

Method: documentation only; no commands were run.
