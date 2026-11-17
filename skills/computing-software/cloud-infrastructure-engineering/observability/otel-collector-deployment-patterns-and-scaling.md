---
id: computing-software.cloud-infrastructure-engineering.observability.otel-collector-deployment-patterns-and-scaling
name: otel-collector-deployment-patterns-and-scaling
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [observability, opentelemetry, otel-collector, collector-deployment, agent-gateway, gateway-collector, agent-collector, daemonset, sidecar, deployment, statefulset, no-collector, collector-scaling, loadbalancing-exporter, trace-id-routing, tail-sampling-scaling, horizontal-scaling, hpa, backpressure, resource-sizing, multi-cluster, cross-region, kafka-buffer, high-availability, collector-topology]
level: advanced
status: docs-checked
description: "Choose and size a Collector topology: no-collector vs agent vs gateway, stateless vs stateful scaling (tail sampling), trace-ID routing with the loadbalancing exporter."
sources: ["https://opentelemetry.io/docs/collector/deploy/", "https://opentelemetry.io/docs/collector/deploy/agent/", "https://opentelemetry.io/docs/collector/deploy/gateway/", "https://opentelemetry.io/docs/collector/scaling/", "https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/exporter/loadbalancingexporter"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Collector deployment patterns and scaling

**Goal:** telemetry leaves every host quickly and cheaply, central policy (sampling,
redaction, routing, tenancy) lives in one tier, and that tier scales horizontally without
breaking the processors that need all spans of a trace in one place.

## 1. The patterns
| Pattern | Shape | Pros | Cons |
|---|---|---|---|
| **No collector** | SDK → backend directly | simplest | app owns retries/auth/batching; per-app config; no central policy |
| **Agent** | SDK → local Collector (DaemonSet per node, or sidecar per pod) → backend | app offloads fast over localhost; host metrics/logs collection; k8s metadata enrichment | per-node resource cost; N configs to roll |
| **Gateway** | SDKs/agents → central Collector Deployment (LB in front) → backend | one place for tail sampling, tenancy, redaction, egress auth; fewer backend connections | extra hop; must be HA and scaled; needs trace-aware routing for stateful processors |
| **Agent + gateway** (recommended for clusters) | DaemonSet agents → gateway Deployment → backends | local buffering + central policy | two tiers to operate |
Rules of thumb: Kubernetes → DaemonSet agent + gateway. VMs → agent per host. Serverless → no
collector or a collector layer/extension with short timeouts.

## 2. Agent tier specifics
```yaml
# DaemonSet agent: cheap, stateless, enrich + forward
receivers: { otlp: { protocols: { grpc: { endpoint: 0.0.0.0:4317 } } } }
processors: { memory_limiter: {...}, batch: {} }
exporters: { otlp/gateway: { endpoint: otel-gateway:4317, sending_queue: { enabled: true }, retry_on_failure: { enabled: true } } }
```
The exporter helper's `sending_queue` and `retry_on_failure` are enabled by default (queue_size default 1000);
if the queue is full, data is dropped unless `block_on_overflow` is set.
Sidecars (Operator `mode: sidecar`, pod annotation `sidecar.opentelemetry.io/inject`) suit strict isolation; cost = 1 Collector per pod.

## 3. Gateway tier and the stateful problem
Most components are stateless and scale by adding replicas behind a load balancer. Components like the
tail sampling processor keep state in memory and cannot be scaled by simply adding replicas; a
trace-aware load balancer (the loadbalancing exporter) must send **all spans of a trace to the same replica**.
The span metrics connector needs all spans of a service on one replica (`routing_key: service`).
Solve with a two-layer gateway:
```yaml
# layer 1 (stateless, scales freely): routes by trace id
exporters:
  loadbalancing:
    routing_key: traceID               # also: service, metric, resource, streamID, attributes, randomness
    protocol: { otlp: { timeout: 1s, tls: { insecure: true } } }
    resolver:
      k8s: { service: otel-sampler.observability, ports: [4317] }   # watches endpoints; also dns:{hostname}, static:{hostnames}, aws_cloud_map
service: { pipelines: { traces: { receivers: [otlp], processors: [memory_limiter, batch], exporters: [loadbalancing] } } }
# layer 2 (StatefulSet "otel-sampler"): tail_sampling / spanmetrics → backend
```
The exporter uses consistent hashing; topology changes are eventually reflected, and for a while the view of
backends can differ from the real topology (the dns resolver is slower than k8s). The Collector docs show a
StatefulSet for the stateful tier, and `routing_key: service` for span metrics so each service's metrics come from one replica.

## 4. Sizing and autoscaling
- Benchmark your own pipeline for throughput per CPU; no figure here is portable.
- Scale on evidence: a rising `otelcol_exporter_queue_size / otelcol_exporter_queue_capacity` or a rising
  `otelcol_receiver_refused_spans` shows a bottleneck. If `otelcol_exporter_send_failed_spans` keeps rising the
  backend is the problem and scaling the Collector will likely make it worse.
- Use the `memory_limiter` processor on every tier; give the termination grace period enough time to drain queues.
- Run at least 2 replicas per tier with anti-affinity and a PodDisruptionBudget.

## 5. Buffers and multi-cluster
- A message queue such as Kafka between agents and gateway adds replay and decouples producers from
  backend outages beyond what exporter queues cover; it costs a Kafka to run.
- Multi-cluster/region: agent+gateway per cluster, gateways export over TLS to a
  central gateway or straight to backends; add `cluster`/`region` resource attributes at the edge.
- Keep backend credentials in the gateway so apps never hold them.

## 6. Watch the topology
```promql
sum by (exporter) (rate(otelcol_exporter_send_failed_spans[5m]))
sum by (exporter) (otelcol_exporter_queue_size) / sum by (exporter) (otelcol_exporter_queue_capacity)
sum by (receiver) (rate(otelcol_receiver_refused_spans[5m]))          # clients are getting errors → scale or raise limits
sum(rate(otelcol_receiver_accepted_spans[5m])) - sum(rate(otelcol_exporter_sent_spans[5m]))   # in-flight / loss delta
otelcol_loadbalancer_num_backends ; otelcol_loadbalancer_backend_latency   # loadbalancing exporter
```
See `...observability.otel-collector-troubleshooting-and-internal-telemetry`.

## Gotchas
- The loadbalancing exporter's dns resolver works with a Kubernetes headless Service; k8s resolver needs RBAC to get, list and watch EndpointSlices.
- Tail sampling behind an ordinary LB "works" but samples randomly per fragment; traces come back partial.
- Rolling the stateful tier discards in-memory state (for example in-flight tail-sampling traces); plan the window.
- With the static resolver there is a risk of data loss if one endpoint is unavailable and redelivery is exhausted; dns and k8s resolvers update the endpoint list.

## Verify
- [ ] Killing one gateway replica causes no `send_failed` increase on agents (queue + retry) and traces remain complete (tail-sampling tier intact).
- [ ] Load test above normal: `refused_spans` stays 0 and queue ratio stays low.
- [ ] Backend outage test: queues absorb it within their configured capacity; data appears after recovery.
- [ ] Every sampled trace in the backend has its spans from all services (no partial traces), proving trace-id routing.

## Checked
2026-10-31. Confirmed against the Collector scaling and gateway deployment pages and the loadbalancing exporter README (stateless vs stateful components, tail sampling not trivially scalable, `routing_key` values service/traceID/metric/resource/streamID/attributes/randomness with traceID the default for traces, static/dns/k8s/aws_cloud_map resolvers, consistent hashing, `groupbytrace`, `otelcol_loadbalancer_num_backends` and `_backend_latency`), the exporter helper README (`sending_queue`, `retry_on_failure`, `queue_size` default 1000, `block_on_overflow`) and the internal-telemetry metric names. Removed: CPU-per-spans throughput figures, HPA/queue thresholds, `trace_dropped_too_early`, the agent processor and receiver details, Kafka/auth component names, the `servicegraph` and `cumulativetodelta` claims, the 1/N remap figure and the 30 s decision_wait rule (not in the pages).
Method: documentation only; no commands were run.
