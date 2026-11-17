---
id: computing-software.cloud-infrastructure-engineering.kubernetes.istio-telemetry-api
name: istio-telemetry-api
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, service-mesh, istio, telemetry-api, access-logs, tracing]
level: practitioner
status: docs-checked
description: "Configure Istio access logging, tracing sampling and metric tags mesh-wide, per namespace or per workload with the Telemetry API instead of meshConfig edits."
sources: ["https://istio.io/latest/docs/reference/config/telemetry/", "https://istio.io/latest/docs/tasks/observability/logs/telemetry-api/", "https://istio.io/latest/docs/tasks/observability/distributed-tracing/telemetry-api/", "https://istio.io/latest/docs/tasks/observability/metrics/customize-metrics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Istio Telemetry API

`Telemetry` resources (`telemetry.istio.io/v1`) control metrics, access logs and tracing at
three levels: root namespace (`istio-system` by default, mesh-wide), a namespace, or workloads by
selector. The hierarchy is workload, then namespace, then root namespace, with the narrower scope winning.

## Mesh-wide access logs for errors only
```yaml
apiVersion: telemetry.istio.io/v1
kind: Telemetry
metadata: {name: mesh-default, namespace: istio-system}
spec:
  accessLogging:
  - providers: [{name: envoy}]
    filter: {expression: "!has(response.code) || response.code >= 400"}   # response.code is absent when a connection fails
```

## Tracing sampling per namespace
Providers are defined once in meshConfig (`extensionProviders`, for example an OpenTelemetry
collector), then referenced:
```yaml
apiVersion: telemetry.istio.io/v1
kind: Telemetry
metadata: {name: tracing, namespace: shop}
spec:
  tracing:
  - providers: [{name: otel}]
    randomSamplingPercentage: 5
```

## Metrics: drop a high-cardinality tag
```yaml
spec:
  selector: {matchLabels: {app: gateway}}
  metrics:
  - providers: [{name: prometheus}]
    overrides:
    - match: {metric: REQUEST_COUNT, mode: CLIENT_AND_SERVER}
      tagOverrides:
        request_host: {operation: REMOVE}
```

## Debug
```bash
kubectl get telemetry -A
```
Per the API reference, a namespace (including the root namespace) may have only one selector-less
Telemetry resource, and only one resource may select any given workload; keep one per scope.

## Verify
`kubectl logs <pod> -c istio-proxy` shows access log lines only for 4xx and 5xx after applying the
mesh-default example.

## Checked
2026-10-26. Checked against the istio.io docs source and the istio/api Telemetry proto (telemetry/v1alpha1, with v1 as an alias). Confirmed: hierarchy workload, namespace, root namespace; only one selector-less Telemetry per namespace and one per selected workload; `filter.expression` CEL for access logs; `randomSamplingPercentage`; metric override `REQUEST_COUNT`, `CLIENT_AND_SERVER`, `tagOverrides` with `REMOVE`; providers defined under `meshConfig.extensionProviders`. Added: the CEL note that `response.code` is absent when a connection fails. Removed: the debug commands that were not in the Telemetry docs.
Method: documentation only; no commands were run.
