---
id: computing-software.cloud-infrastructure-engineering.observability.otel-collector-failover-and-high-availability
name: otel-collector-failover-and-high-availability
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [collector-high-availability, failover-connector, collector-deployment, sending-queue-config, persistent-queue]
level: advanced
status: docs-checked
description: "Make collector pipelines highly available: stateless replicas behind a load balancer, persistent sending queues, and the failover connector with priority levels."
sources: ["https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/connector/failoverconnector", "https://opentelemetry.io/docs/collector/scaling/", "https://github.com/open-telemetry/opentelemetry-collector/blob/main/exporter/exporterhelper/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Collector failover and HA

## Replicas
Most Collector components are stateless, so scaling and availability come from adding replicas behind a load
balancer: if one instance fails, the balancer can redirect traffic to healthy ones. For gRPC (OTLP) use an L7
balancer; an L4 balancer may pin clients to one Collector. Stateful components (tail sampling, span-to-metrics)
need a load-balancing exporter layer in front, otherwise one trace is split across replicas (Collector scaling
guide).

## Persistent queues (exporterhelper)
`sending_queue.storage` (default none) enables persistence using a storage extension; the file storage extension
is described as a popular and safe choice. If the Collector is killed with items in the persistent queue, they are
picked up on restart and exporting continues. `sending_queue.queue_size` (default 1000) bounds the queue. If data
cannot be added (queue full, or storage out of space or I/O errors) it is typically dropped, unless
`block_on_overflow` (default false) is true. Auth extension context is not propagated through the persistent queue.
```yaml
extensions:
  file_storage/otc:
    directory: /var/lib/storage/otc
exporters:
  otlp:
    endpoint: backend.example.com:4317
    sending_queue:
      storage: file_storage/otc
service:
  extensions: [file_storage/otc]
```

## Failover connector (contrib, alpha for traces, metrics and logs)
Health-based routing between pipelines depending on the health of downstream exporters.
- `priority_levels` (required): list of levels, 1 to n; multiple pipelines can sit at one level.
- `retry_interval` (optional, default 10 minutes): how often the connector tries to reestablish higher levels.
- `sending_queue` (optional, enabled by default): queue inside the connector. The README recommends configuring the
  queue here and disabling `sending_queue` on the exporters in the priority pipelines, so data is not stuck in the
  queue of an unhealthy exporter where it cannot fail over.
- `condition.error.contains`: case-insensitive substrings; only matching errors trigger failover. Omit it and all
  errors trigger failover.
If any pipeline at a stable level fails, that level is unhealthy and the connector moves down one level and routes
all data there.
```yaml
connectors:
  failover:
    priority_levels:
      - [traces/first]
      - [traces/second]
    retry_interval: 5m
service:
  pipelines:
    traces:        {receivers: [otlp], exporters: [failover]}
    traces/first:  {receivers: [failover], exporters: [otlp_grpc/first]}
    traces/second: {receivers: [failover], exporters: [otlp_grpc/second]}
```

## Verify
- [ ] Making the primary exporter fail shifts data to the next priority level, and it returns after `retry_interval`.
- [ ] Exporters in priority pipelines have their own `sending_queue` disabled when the connector queue is used.

## Checked
2026-11-09. Confirmed against the failover connector README, the exporterhelper README (queue and persistence
sections searched) and the opentelemetry.io Collector scaling page (all read as raw markdown). Removed unconfirmed
claims: PDB and anti-affinity advice, the PVC or hostPath volume remark, the earlier claim that a queue absorbs
errors so failover will not trigger (the README instead recommends moving the queue to the connector), the
memory_limiter and batch pipeline example and the claim about data being split across backends.
Method: docs-checked 2026-11-09 against the failoverconnector README, exporterhelper README and the Collector scaling page markdown; documentation only, no commands run.
