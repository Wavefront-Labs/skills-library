---
id: computing-software.cloud-infrastructure-engineering.istio.istio-metrics-prometheus
name: istio-metrics-prometheus
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, istio-metrics, prometheus, istio-requests-total]
level: practitioner
status: docs-checked
description: "Scrape standard Istio request metrics with Prometheus and reduce label cardinality through the Telemetry metrics API."
sources: ["https://istio.io/latest/docs/reference/config/metrics/", "https://istio.io/latest/docs/reference/config/telemetry/", "https://istio.io/latest/docs/ops/best-practices/security/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Sidecars emit standard metrics such as `istio_requests_total`. Port 15020 serves merged Prometheus telemetry from the Istio agent, Envoy and the application.

```yaml
apiVersion: telemetry.istio.io/v1
kind: Telemetry
metadata: {name: drop-dims, namespace: istio-system}
spec:
  metrics:
  - providers: [{name: prometheus}]
    overrides:
    - match: {metric: REQUEST_COUNT}
      tagOverrides:
        request_protocol: {operation: REMOVE}
```

Gotchas: `REQUEST_COUNT` is exported by the Prometheus provider as `istio_requests_total`. If `match` is omitted, overrides apply to all metrics in both client and server mode. `REMOVE` drops the tag from the metric.

Verify: query `istio_requests_total` in Prometheus and confirm the removed tag (`request_protocol` here) no longer appears.

## Checked

2026-11-03. Confirmed in the Telemetry reference (`metrics`, `overrides`, `match.metric: REQUEST_COUNT`, `tagOverrides` with `operation: REMOVE`, mapping to `istio_requests_total`, default match scope), the standard metrics page (`istio_requests_total`) and the security best-practices page (port 15020 merged Prometheus telemetry). Removed: `istio_request_duration_milliseconds` and `/stats/prometheus` port statements, scrape-by-annotation or PodMonitor, the cardinality remarks, and the recording-rule advice (not on the pages read).

Method: documentation only; no commands were run.
