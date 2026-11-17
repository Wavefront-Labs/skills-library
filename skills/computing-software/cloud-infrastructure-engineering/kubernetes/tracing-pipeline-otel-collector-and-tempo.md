---
id: computing-software.cloud-infrastructure-engineering.kubernetes.tracing-pipeline-otel-collector-and-tempo
name: tracing-pipeline-otel-collector-and-tempo
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, tracing, tempo, grafana-tempo, jaeger, otel-collector-pipeline, tail-sampling, opentelemetry, k8sattributesprocessor, otel-agent-gateway]
level: advanced
status: docs-checked
description: "Build a trace pipeline: OTel Collector agent and gateway tiers, tail-based sampling with the load-balancing exporter, and Grafana Tempo on object storage."
sources: ["https://opentelemetry.io/docs/collector/deployment/", "https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/tailsamplingprocessor", "https://grafana.com/docs/tempo/latest/setup/helm-chart/", "https://www.jaegertracing.io/docs/latest/deployment/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Tracing pipeline: OTel Collector and Tempo

## Architecture
apps (OTLP) → **agent** collectors (DaemonSet: k8sattributes, batch) → **load-balancing
exporter** keyed by traceID → **gateway** collectors (tail sampling) → Tempo/Jaeger.
Tail sampling needs every span of a trace on the **same** collector instance — hence the
loadbalancing exporter tier.

## Agent (DaemonSet)
```yaml
receivers: {otlp: {protocols: {grpc: {}, http: {}}}}
processors:
  memory_limiter: {check_interval: 1s, limit_percentage: 80, spike_limit_percentage: 25}
  k8sattributes: {extract: {metadata: [k8s.namespace.name, k8s.pod.name, k8s.deployment.name, k8s.node.name]}}
  batch: {}
exporters:
  loadbalancing:
    routing_key: traceID
    protocol: {otlp: {tls: {insecure: true}}}
    resolver: {k8s: {service: otel-gateway-headless.observability}}
service:
  pipelines:
    traces: {receivers: [otlp], processors: [memory_limiter, k8sattributes, batch], exporters: [loadbalancing]}
```
k8sattributes needs RBAC to read the Kubernetes objects it extracts from (see its README); extracting deployment, replicaset and similar metadata is off by default and costs extra memory. The loadbalancing exporter's `k8s` resolver needs `get`, `list` and `watch` on EndpointSlices in the target namespace. Put `memory_limiter` first in each pipeline.

## Gateway with tail sampling (Deployment/StatefulSet)
```yaml
processors:
  tail_sampling:
    decision_wait: 10s              # default 30s
    num_traces: 100000              # default 50000
    policies:
    - {name: errors, type: status_code, status_code: {status_codes: [ERROR]}}
    - {name: slow, type: latency, latency: {threshold_ms: 500}}
    - {name: baseline, type: probabilistic, probabilistic: {sampling_percentage: 5}}
exporters:
  otlp/tempo: {endpoint: tempo-distributor.observability:4317, tls: {insecure: true}}
```
Scale gateways horizontally; the load-balancing exporter's view of the topology is eventually consistent (the `k8s` resolver updates faster than `dns`), so expect a window of mismatched routing while scaling.

## Tempo
```bash
helm install tempo grafana/tempo-distributed -n observability -f tempo-values.yaml
```
The chart's README says it is migrating to the grafana-community/helm-charts repository, with updates
there after 30 January 2026; check which repo currently publishes it. Key values: `storage.trace.backend`
(for example `s3`), the `traces.otlp.grpc` / `traces.otlp.http` receivers (disabled by default in the chart),
retention via `compactor.config.compaction.block_retention` (chart default 48h), and
`metricsGenerator.enabled` (default false) for span metrics and service graphs that remote-write to Prometheus.

## Verify
- [ ] An error trace from a test request appears in Tempo after `decision_wait`; most OK traces are dropped as designed.
- [ ] `otelcol_receiver_refused_spans` and `otelcol_exporter_send_failed_spans` stay near zero.

## Checked

2026-10-26, against OpenTelemetry Collector contrib READMEs (loadbalancingexporter, tailsamplingprocessor, k8sattributesprocessor), memorylimiterprocessor README, Collector internal telemetry docs, and the grafana/helm-charts tempo-distributed chart (README and values.yaml, last chart commit 2026-01-30). Confirmed: loadbalancing `routing_key` values and `traceID` default for traces, `k8s` resolver `service` form and EndpointSlice RBAC, tail sampling policy types, `decision_wait` and `num_traces` defaults, policy `status_code`, `latency` (`threshold_ms`) and `probabilistic` (`sampling_percentage`), memory_limiter fields and first-processor advice, internal metric names, chart value keys and defaults. Wrong: `otelcol_processor_refused_spans` (the documented metric is `otelcol_receiver_refused_spans`), and Tempo chart repo location is migrating. Removed unconfirmed Jaeger v2 and Loki derived-field claims and the memory formula. The Tempo application config was not checked beyond the chart values.

Method: documentation only; no commands were run.
