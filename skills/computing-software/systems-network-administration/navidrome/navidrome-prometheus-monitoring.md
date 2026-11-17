---
id: computing-software.systems-network-administration.navidrome.navidrome-prometheus-monitoring
name: navidrome-prometheus-monitoring
category: computing-software
field: systems-network-administration
product: navidrome
tags: [navidrome, prometheus, metrics, openmetrics, grafana, monitoring, metricspath, scrape]
level: practitioner
status: docs-checked
description: "Expose Navidrome metrics for Prometheus: enable the endpoint, obscure or password-protect the path, scrape config, Docker network layout and Grafana dashboards."
sources: ["https://www.navidrome.org/docs/usage/integration/monitoring/", "https://www.navidrome.org/docs/usage/configuration/options/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Navidrome Prometheus monitoring

Navidrome serves OpenMetrics-format metrics when enabled:

```yaml
environment:
  ND_PROMETHEUS_ENABLED: "true"
  ND_PROMETHEUS_METRICSPATH: "/metrics_SOME_SECRET_KEY"
```
A custom `Prometheus.MetricsPath` is strongly recommended if the instance is public; `Prometheus.Password` adds Basic Auth to the endpoint.

Prometheus scrape config:

```yaml
global:
  scrape_interval: 10s
scrape_configs:
  - job_name: 'navidrome'
    metrics_path: /metrics_SOME_SECRET_KEY
    scheme: http
    static_configs:
      - targets: ['navidrome:4533']
```
Put Navidrome, Prometheus and Grafana on one Docker network (the docs use `metrics-network`) so the target resolves by service name. Grafana dashboards listed by the docs: IDs 24397 and 18038.

Verify: open Prometheus targets page and check the `navidrome` job is UP.

## Checked

2026-11-04. Confirmed against the Navidrome Monitoring page (env vars, recommended custom metrics path, scrape config, `metrics-network`, dashboard IDs) and the Configuration Options page (`Prometheus.MetricsPath`, `Prometheus.Password` Basic Auth). Removed the dashboard name and the Grafana datasource claim, which the page does not state.

Method: documentation only; no commands were run.
