---
id: computing-software.cloud-infrastructure-engineering.observability.autoscaling-otel-collectors
name: autoscaling-otel-collectors
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [collector-hpa, collector-autoscaling, collector-deployment, otel-collector, kubernetes-hpa]
level: advanced
status: docs-checked
description: "Decide when and how to scale OpenTelemetry Collectors: memory_limiter and queue signals, when not to scale, stateless, scraper and stateful tiers."
sources: ["https://opentelemetry.io/docs/collector/scaling/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scaling collectors

The Collector scaling guide splits components into three kinds: stateless, scrapers and stateful. Understand the
workload first; the metrics below give hints on when to act.

## When to scale
- With the `memory_limiter` processor in the pipeline, watch `otelcol_processor_refused_spans` (the same metric
  exists for the other signals). If data is refused too often, scale up. Scale down once memory use across nodes
  is significantly lower than the processor's limit.
- Watch exporter queue metrics `otelcol_exporter_queue_size` and `otelcol_exporter_queue_capacity`. General
  guidance: consider scaling up when the queue reaches 60-70% of capacity, scale down if it is consistently low,
  and keep a minimum number of replicas, for example three, for resilience.
- Scraping receivers such as Prometheus: shard once the time to scrape all targets gets critically close to the
  scrape interval.
- Component-specific metrics help too; the load-balancing exporter exposes `otelcol_loadbalancer_backend_latency`,
  useful to spot a single slow backend.

## When NOT to scale
- The telemetry database cannot keep up: more Collectors will not help without scaling the database.
- The network link to the backend is saturated: more Collectors can be harmful.
- Queue size stays near capacity: exporting is slower than receiving. Raising queue capacity costs memory but gives
  the backend room; if the queue keeps rising proportionally, look outside the Collector. More workers only add
  pressure to an already loaded system.
- A rising `otelcol_exporter_send_failed_spans` means permanent send failures; scaling up will likely worsen it.

## Stateless collectors
Most components are stateless: add replicas and spread traffic with a load balancer. In Kubernetes, prefer
off-the-shelf options (service meshes such as Istio or Linkerd, or cloud load balancers). For gRPC (OTLP) use an L7
load balancer that understands gRPC; an L4 balancer may pin a client to one Collector and negate scaling.
Layering ideas from the guide: DaemonSet Collectors per node feeding a central Collector; sidecars when nodes are
few and pods many (better gRPC balancing without a gRPC-specific balancer, and one failed DaemonSet pod does not
take down a node's pods). The Operator injects a sidecar when the Collector CR has `mode: sidecar` and the pod
carries the annotation `sidecar.opentelemetry.io/inject: 'true'`.

## Scrapers
Adding identical Collectors makes each scrape the same endpoints (for example out-of-order samples). Shard
endpoints instead: one config per Collector (for example per namespace or label), or the Operator's Target
Allocator, which distributes Prometheus scrape targets across Collectors. With `mode: statefulset` and
`targetAllocator.enabled: true` on the CR, the Operator rewrites the scrape config to use `http_sd_configs`
pointing at the allocator; changing `replicas` on the CR then redistributes targets.

## Stateful collectors
The tail-sampling processor holds spans in memory until a trace is complete; spreading a trace over replicas gives
inconsistent decisions and traces missing spans. Span-to-metrics aggregation by service name is inaccurate when
several Collectors see one service. Put a Collector layer with the load-balancing exporter in front, which hashes
trace ID or service name consistently. It can resolve backends from a DNS A record (such as a Kubernetes headless
service) or a static host list; each Collector may run the DNS query at a different time, so lower the interval in
highly elastic environments.

## Verify
- [ ] Refused-span and queue-fill metrics are monitored before choosing to scale.
- [ ] Stateful tiers sit behind a load-balancing exporter layer.

## Checked
2026-11-09. Confirmed against the opentelemetry.io Collector scaling page (markdown source, read in full except
the final load-balancing exporter configuration example). Removed unconfirmed claims: the HorizontalPodAutoscaler
manifest and CPU target, the Operator `autoscaler` field, KEDA and prometheus-adapter advice, `GOMEMLIMIT`,
`file_storage` persistent queue, PDB and gRPC `max_connection_age` advice, and the Kubernetes HPA and Operator API
sources (not read).
Method: docs-checked 2026-11-09 against the opentelemetry.io Collector scaling page markdown; documentation only, no commands run.
