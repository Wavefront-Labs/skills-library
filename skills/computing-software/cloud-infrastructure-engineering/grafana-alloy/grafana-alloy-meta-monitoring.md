---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-meta-monitoring
name: grafana-alloy-meta-monitoring
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [prometheusexporterself, meta-monitoring, logging-write-to, tracing-write-to, self-monitoring]
level: practitioner
status: docs-checked
description: "Meta-monitor Alloy itself: scrape its own metrics with prometheus.exporter.self, send logs with logging write_to and traces with the tracing block."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/collect/metamonitoring.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Meta-monitoring Alloy

Alloy's own metrics are on `/metrics` at the `--server.http.listen-addr` address (for example `127.0.0.1:12345/metrics`), or you can route them through components.

## Metrics
```alloy
prometheus.exporter.self "default" {}

prometheus.scrape "metamonitoring" {
  targets    = prometheus.exporter.self.default.targets
  forward_to = [prometheus.remote_write.default.receiver]
}
prometheus.remote_write "default" {
  endpoint {
    url = "http://mimir:9009/api/v1/push"
  }
}
```
`prometheus.exporter.self` takes no arguments. Forward to `prometheus.relabel` first if needed, or to `otelcol.receiver.prometheus` for OTLP.

## Logs
`logging` is unlabeled and once per file; `write_to` accepts Loki receivers such as `loki.process.X.receiver` or `loki.relabel.X.receiver` (or `otelcol.receiver.loki` for OTLP).
```alloy
logging {
  level    = "warn"
  format   = "json"
  write_to = [loki.write.default.receiver]
}
```

## Traces
```alloy
tracing {
  sampling_fraction = 0.1
  write_to          = [otelcol.exporter.otlp.default.input]
}
otelcol.exporter.otlp "default" {
  client {
    endpoint = "tempo:4317"
  }
}
```

## Checked

2026-11-08. Read the meta-monitoring page (collect/metamonitoring.md) in full. Confirmed: the `/metrics` endpoint and `--server.http.listen-addr`, `prometheus.exporter.self` taking no arguments, forwarding targets (relabel, otelcol.receiver.prometheus), the unlabeled once-per-file logging and tracing blocks, `write_to` receivers, the logging and tracing examples, and the sampling fraction default of 0.1.

Method: documentation only; no commands were run.
