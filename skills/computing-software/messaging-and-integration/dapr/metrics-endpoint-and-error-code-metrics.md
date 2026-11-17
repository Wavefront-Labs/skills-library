---
id: computing-software.messaging-and-integration.dapr.metrics-endpoint-and-error-code-metrics
name: metrics-endpoint-and-error-code-metrics
category: computing-software
field: messaging-and-integration
product: dapr
tags: [metrics, prometheus, metrics-port, enable-metrics, recorderrorcodes, annotations, observability]
level: practitioner
status: docs-checked
description: "Control the Dapr Prometheus endpoint: default port 9090, --enable-metrics, enable-metrics and metrics-port annotations, spec.metrics.enabled, and recordErrorCodes."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/observability/metrics/metrics-overview.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Every Dapr process emits Go runtime/process metrics plus Dapr metrics, and each sidecar exposes a Prometheus-compatible endpoint. It is on by default at port `9090`.

CLI or `daprd`: disable with `--enable-metrics=false`; change the port with `--metrics-port`.

Kubernetes annotations per app (with metrics disabled, `daprd` does not open the listening port):

```yaml
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "nodeapp"
        dapr.io/app-port: "3000"
        dapr.io/enable-metrics: "true"
        dapr.io/metrics-port: "9090"
```

Via application Configuration, `spec.metrics.enabled: false` turns collection off in the sidecars that use it:

```yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: tracing
  namespace: default
spec:
  metrics:
    enabled: false
```

Error code metrics record Dapr API error codes (the standardized errors APIs return to callers). Off by default:

```yaml
spec:
  metrics:
    enabled: true
    recordErrorCodes: true
```

A resulting series carries labels such as `app_id`, `category` (for example `state`), `error_code` (for example `ERR_STATE_STORE_NOT_CONFIGURED`), `namespace`, `instance`, `job` and `service`. The page describes the new metric as `error_code_total`, for monitoring error codes by application, code and category.

For HTTP request metrics with unbounded paths, use `spec.metrics.http.pathMatching` with `increasedCardinality: false`; non-matched paths then fall into a catch-all bucket with an empty `path` label, matched ones keep the template such as `/orders/{orderID}`.

## Checked

2026-11-08. Read the cited dapr/docs v1.15 page in full and compared each claim; wording tightened where it went beyond the page, the remaining claims are unchanged.

Method: documentation only; no commands were run.
