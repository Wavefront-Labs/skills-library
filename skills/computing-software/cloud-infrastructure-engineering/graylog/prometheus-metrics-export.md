---
id: computing-software.cloud-infrastructure-engineering.graylog.prometheus-metrics-export
name: prometheus-metrics-export
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [prometheus, metrics, metrics-exporter, server-conf, monitoring]
level: practitioner
status: docs-checked
description: "Export Graylog metrics to Prometheus: enable the exporter in server.conf, scrape port 9833 and add custom mappings."
sources:
  - https://go2docs.graylog.org/current/interacting_with_your_log_data/metrics.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# prometheus metrics export

Standard metrics are in the UI (System > Nodes, then a node's metrics) and via the REST API browser.

For Prometheus, set in `server.conf` (administrator task):

```
prometheus_exporter_enabled = true
```

Metrics are then served on port 9833 at `http://127.0.0.1:9833/api/metrics/prometheus`. Change the listener with:

```
prometheus_exporter_bind_address = 10.0.0.1:9090
```

Mappings:
- `prometheus_exporter_mapping_file_path_core`: path to a YAML file that completely replaces the default core mappings (watched for changes at runtime).
- `prometheus_exporter_mapping_file_path_custom`: a YAML file that adds to the core mappings.

Graylog re-reads the mapping files every 30 seconds by default; change that with `prometheus_exporter_mapping_file_refresh_interval`.

## Checked

2026-11-04. Confirmed against the Operational Metrics page (property names, port 9833, default URI, bind address example, core and custom mapping files, refresh interval). Removed: the restart instruction (not on the page).

Method: documentation only; no commands were run.
