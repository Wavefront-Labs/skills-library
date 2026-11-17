---
id: computing-software.cloud-infrastructure-engineering.observability.otel-collector-sidecars
name: otel-collector-sidecars
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [collector-sidecar, sidecar-collector-injection, collector-deployment, otel-operator, otel-collector]
level: practitioner
status: draft
description: "Run OTel Collector sidecars: when they beat DaemonSets, Operator sidecar mode and injection annotations, native sidecars for Jobs, resource sizing and pitfalls."
sources: ["https://github.com/open-telemetry/opentelemetry-operator#sidecar-injection", "https://opentelemetry.io/docs/collector/deployment/agent/", "https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sidecar collectors

## When sidecars make sense
- No DaemonSets allowed: EKS Fargate, GKE Autopilot restrictions, ECS tasks, Cloud Run multi-container.
- Hard tenant isolation: per-app credentials, per-app pipelines, noisy app cannot starve others.
- App insists on `localhost:4317` and you cannot change it.
Otherwise prefer a node agent DaemonSet: fewer collectors, lower total overhead, central config.

## Operator sidecar mode
```yaml
apiVersion: opentelemetry.io/v1beta1
kind: OpenTelemetryCollector
metadata: {name: sidecar, namespace: shop}
spec:
  mode: sidecar
  resources: {limits: {cpu: 200m, memory: 128Mi}}
  config:
    receivers: {otlp: {protocols: {grpc: {endpoint: 0.0.0.0:4317}, http: {endpoint: 0.0.0.0:4318}}}}
    processors:
      memory_limiter: {check_interval: 1s, limit_percentage: 80, spike_limit_percentage: 25}
      batch: {}
    exporters: {otlp: {endpoint: otel-gateway.observability:4317, tls: {insecure: true}}}
    service:
      pipelines:
        traces: {receivers: [otlp], processors: [memory_limiter, batch], exporters: [otlp]}
```
Inject: pod annotation `sidecar.opentelemetry.io/inject: "true"` (single CR in namespace) or `"sidecar"` (CR name)
or `"other-ns/sidecar"`. Injection happens at pod creation via webhook - restart pods after adding the annotation.

## Jobs and CronJobs
A classic sidecar keeps the Job pod running forever. Use Kubernetes native sidecars (init container with
`restartPolicy: Always`, k8s 1.29+); the Operator can inject that way (feature gate/flag
`--feature-gates=operator.sidecarcontainers.native` in some versions). Otherwise shut the collector down from the app
(`/shutdown` is not built in) - prefer exporting directly to a gateway for jobs.

## Sizing
Typical sidecar: 50-100m CPU, 64-128 Mi memory for a moderate app; memory_limiter mandatory. Multiply by pod count
when costing.

## Gotchas
- k8sattributes in a sidecar sees only its own pod; resource attributes are better set via env/downward API.
- Sidecar restarts lose in-memory queues; the app's SDK retries cover short gaps.
