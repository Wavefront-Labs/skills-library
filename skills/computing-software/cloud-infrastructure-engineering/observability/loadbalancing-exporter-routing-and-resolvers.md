---
id: computing-software.cloud-infrastructure-engineering.observability.loadbalancing-exporter-routing-and-resolvers
name: loadbalancing-exporter-routing-and-resolvers
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [loadbalancing-routing-key, loadbalancing-resolver, collector-deployment, otel-collector, tail-sampling]
level: advanced
status: docs-checked
description: "Configure the loadbalancing exporter for trace affinity: routing keys (traceID, service, metric, streamID, attributes), DNS/k8s/static resolvers, RBAC and rebalancing behaviour."
sources: ["https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/exporter/loadbalancingexporter", "https://opentelemetry.io/docs/collector/scaling/#scaling-stateful-collectors"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# loadbalancing exporter: routing keys and resolvers

Stateful processing needs all related data on one collector: tail sampling (whole trace), spanmetrics/servicegraph
(per service), `deltatocumulative`/cumulativetodelta (per stream). The loadbalancing exporter in a first tier hashes a
key and forwards to a consistent backend in the second tier. The README says the exporter type was renamed to
`load_balancing` (snake case); `loadbalancing` still works as a deprecated alias, so new configs should use `load_balancing:`.

## Config
```yaml
exporters:
  load_balancing:
    routing_key: traceID          # service | traceID | resource | metric | streamID | attributes | randomness
    protocol:
      otlp:
        timeout: 5s
        tls: {insecure: true}
        sending_queue: {enabled: true, queue_size: 5000}
    resolver:
      k8s:
        service: otel-sampler-headless.observability
        ports: [4317]
      # dns: {hostname: otel-sampler-headless.observability.svc.cluster.local, port: 4317, interval: 5s}
      # static: {hostnames: [sampler-0:4317, sampler-1:4317]}
      # aws_cloud_map: {namespace: obs, service_name: sampler}
```
Defaults when `routing_key` is unset: `traceID` for traces, `service` for logs and for metrics. Valid keys per signal (README
table): `service` spans, logs, metrics; `traceID` spans, logs; `resource` logs, metrics; `metric` and `streamID` metrics;
`attributes` spans, logs, metrics (list the keys in `routing_attributes`); `randomness` spans (routes by the OTel randomness
value, the `rv` in tracestate or the low bits of the trace ID).

## Resolvers
- `k8s`: needs RBAC `get`, `list`, `watch` on `discovery.k8s.io/v1` `EndpointSlice` in the target namespace (otherwise the resolver
  cache stays empty). `service` takes `name.namespace`; `ports` defaults to 4317; `timeout` defaults to 1m; `return_hostnames`
  needs a headless Service in front of a StatefulSet. Endpoints whose `ready` condition is explicitly false are excluded. The
  README says it updates more quickly than `dns`.
- `dns`: resolves a hostname (for example a headless Service) every `interval` (default 5s); `port` defaults to 4317, `timeout` 1s.
- `static`: fixed list of `hostnames`.
- `aws_cloud_map`: `namespace` and `service_name` required; `interval` default 30s; returns at most 100 hosts.
- Specify only one resolver; several at once is an error.

## Rebalancing
When the backend list changes, around R/N of the routes (R = routes, N = backends) are rerouted, so a trace in flight can
split across two samplers. The README says more backends means less disruption per change, and suggests the
`groupbytrace` processor if routing stability matters and backends change constantly. Keep the second tier's membership
stable where you can. The README also warns that with the `static` resolver data can be lost if a target stays unavailable,
and that topology changes under `dns` or `k8s` are reflected only eventually.

## Metrics
`otelcol_loadbalancer_num_backends`, `otelcol_loadbalancer_num_backend_updates`, `otelcol_loadbalancer_num_resolutions`,
`otelcol_loadbalancer_backend_outcome`, `otelcol_loadbalancer_backend_latency` (documentation.md). Alert if backends = 0.

## Gotchas
- Several first-tier collectors can run the exporter: the README says consistent hashing gives the same result across instances
  that share the same configuration.
- Resiliency has two levels: the exporter's own `timeout`, `retry_on_failure` and `sending_queue`, and the same settings under
  `protocol.otlp` for each backend. A persistent queue is not supported in the `otlp` section. Do not set `endpoint` there; the
  exporter overrides it.
- Mismatched resolver views between first-tier pods can send one trace to two samplers.
- Routing uses the key only, not backend load, so `routing_key: service` sends a hot service to one backend; watch per-backend load.

## Checked

2026-10-24. OpenTelemetry Collector contrib loadbalancing exporter README and documentation.md (main branch). Confirmed: type rename to `load_balancing` with deprecated alias, routing key list, per-signal validity and defaults, resolver options and defaults, EndpointSlice RBAC (discovery.k8s.io), rebalancing behaviour (R/N), resiliency options, and metric names. Removed unconfirmed claims about StatefulSet and HPA guidance and the old `endpoints` RBAC.

Method: documentation only; no commands were run.
