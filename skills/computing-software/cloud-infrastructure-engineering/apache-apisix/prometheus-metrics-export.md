---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.prometheus-metrics-export
name: prometheus-metrics-export
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, prometheus, metrics, export-server, plugin-attr, observability, plugin]
level: practitioner
status: docs-checked
description: "Expose APISIX Prometheus metrics: enable the plugin on a route, plugin_attr export_addr and export_uri, public-api alternative, prefer_name and stream metrics."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/plugins/prometheus.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prometheus metrics export

Enable on a route or globally with `"plugins": { "prometheus": {} }`. Optional attribute `prefer_name` (false) exports route and service names instead of IDs.

Export endpoint in `conf/config.yaml`; reload APISIX after changes:

```yaml
plugin_attr:
  prometheus:
    export_uri: /apisix/prometheus/metrics
    enable_export_server: true
    export_addr:
      ip: 127.0.0.1    # use 0.0.0.0 to reach it from outside a container
      port: 9091
```

Default endpoint: `http://127.0.0.1:9091/apisix/prometheus/metrics` (Prometheus text format). Point your Prometheus scrape job there.

To serve it on the public listener instead, set `enable_export_server: false` and add a route with the `public-api` plugin; this adds request-path overhead.

Stream metrics: set `apisix.proxy_mode: http&stream`, configure `stream_proxy`, add `prometheus` to `stream_plugins`, then enable it on a stream route.

## Checked

2026-11-04. Confirmed against the APISIX prometheus plugin page: prefer_name, export_uri, enable_export_server, export_addr and port 9091, 0.0.0.0 for container access, reload after changes, the public-api route with its overhead caution, the stream setup with proxy_mode, stream_proxy and stream_plugins. Nothing removed.

Method: documentation only; no commands were run.
