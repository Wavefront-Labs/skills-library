---
id: computing-software.messaging-and-integration.dapr.configuration-metrics-cardinality-and-rules
name: configuration-metrics-cardinality-and-rules
category: computing-software
field: messaging-and-integration
product: dapr
tags: [configuration, metrics, cardinality, pathmatching, prometheus, rules, recorderrorcodes]
level: advanced
status: docs-checked
description: "Tame Dapr metric cardinality in the Configuration: http.increasedCardinality, pathMatching templates, excludeVerbs, regex rules per metric, latency buckets and recordErrorCodes."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/configuration/configuration-overview.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `metrics` block of a sidecar Configuration controls collection and cardinality. Full example from the page:

```yml
metrics:
  enabled: true
  rules: []
  latencyDistributionBuckets: []
  http:
    increasedCardinality: true
    pathMatching:
      - /items
      - /orders/{orderID}
      - /orders/{orderID}/items/{itemID}
      - /payments/{paymentID}
      - /payments/{paymentID}/status
      - /payments/{paymentID}/refund
      - /payments/{paymentID}/details
    excludeVerbs: false
  recordErrorCodes: true
```

Properties:

- `enabled` (default true): metrics collection and endpoint.
- `rules`: named rules; each has `labels` to filter on and a `regex` applied to the metrics path.
- `latencyDistributionBuckets`: histogram buckets in milliseconds.
- `http.increasedCardinality` (default true): each request path creates a new metric bucket in the HTTP server, which can consume excessive memory when paths contain variable parts such as IDs.
- `http.pathMatching`: path templates that collapse many paths into one series. With `/orders/{orderID}/items/{itemID}` all order and item IDs yield a single metric count.
- `http.excludeVerbs` (default false): ignore the HTTP verb when building the method label.
- `recordErrorCodes`: records error code metrics, off by default.

Regex rules rewrite label values for any exposed metric:

```yml
metrics:
  enabled: true
  rules:
    - name: dapr_runtime_service_invocation_req_sent_total
      labels:
      - name: method
        regex:
          "orders/": "orders/.+"
```

Use path matching or rules when requests carry IDs in the URL, otherwise label sets grow without bound.

## Checked

2026-11-08. Read the cited dapr/docs v1.15 page in full and compared each claim; all claims matched the page and none were changed.

Method: documentation only; no commands were run.
