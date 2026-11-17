---
id: computing-software.systems-network-administration.incus.metrics-prometheus-setup
name: metrics-prometheus-setup
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, metrics, prometheus, grafana, loki, metrics-certificate, core-metrics-address]
level: practitioner
status: docs-checked
description: "Expose Incus metrics to Prometheus: core.metrics_address, a metrics-type client certificate, the scrape job settings, Grafana dashboard 19727 and Loki logging."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/metrics.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Metrics with Prometheus

- Raw view: `incus query /1.0/metrics`. In a cluster each member returns only its own instances, so scrape each. Instance metrics are cached for 8 seconds.
- Endpoint: `core.https_address` exposes the full API; `core.metrics_address` (e.g. `":8444"`) exposes metrics only.
- Certificate (OpenSSL 1.1.0+): `openssl req -x509 -newkey ec -pkeyopt ec_paramgen_curve:secp384r1 -sha384 -keyout metrics.key -nodes -out metrics.crt -days 3650 -subj "/CN=metrics.local"`, then `incus config trust add-certificate metrics.crt --type=metrics`. It can read metrics only.
- Not recommended: `incus config set core.metrics_authentication=false`.
- Prometheus job: `metrics_path: '/1.0/metrics'`, `scheme: 'https'`, `tls_config` with `ca_file` `server.crt` (from `/var/lib/incus/`), `cert_file` `metrics.crt`, `key_file` `metrics.key`; add `server_name` if the target is not in the certificate SAN. Optional `project` parameter filters one project. One job per cluster or server.
- Grafana: the Prometheus data source assumes a 15s `scrape_interval`; if you change it, change it in both Prometheus and the data source. The dashboard needs Grafana 8.4 or later with Prometheus and Loki data sources; import dashboard ID `19727`.
- Logs go to Loki; the `instance` field must match the Prometheus job name (`logging.*.target.instance`).

## Checked

2026-11-09. Confirmed against the Incus How to monitor metrics page: per-member scraping, 8 second cache, core.metrics_address vs core.https_address, openssl command and 1.1.0 requirement, metrics certificate type, core.metrics_authentication, Prometheus job fields and server_name note, project parameter, dashboard 19727, Grafana 8.4, Loki instance field. Reworded: the Grafana 15s and 8.4 statements, which the page states separately.
Method: documentation only; no commands were run.
