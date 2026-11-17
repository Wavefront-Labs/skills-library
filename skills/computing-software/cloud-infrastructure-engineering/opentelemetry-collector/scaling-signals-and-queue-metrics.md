---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.scaling-signals-and-queue-metrics
name: scaling-signals-and-queue-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, scaling, queue, metrics, autoscaling, saturation]
level: advanced
status: docs-checked
description: "Decide when to scale the Collector by watching queue size, queue capacity and refused or failed data metrics."
sources:
  - https://opentelemetry.io/docs/collector/scaling/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The scaling page uses the Collector's own metrics to decide when to scale.

- `otelcol_processor_refused_spans`, with `memory_limiter` in the pipeline, records data blocked from the pipeline; the same metric exists for other signals. If data is refused too often, scale up. Scale down once memory use across nodes is well below the limit.
- `otelcol_exporter_queue_size` against `otelcol_exporter_queue_capacity`. A full queue rejects data, counted by `otelcol_exporter_enqueue_failed_spans`. The general guidance is to consider scaling up at 60-70% of capacity, and down when consistently low, keeping a minimum number of replicas such as three.
- `otelcol_loadbalancer_backend_latency`, a histogram from the load-balancing exporter, shows whether backends take similar time; one slow backend points outside the Collector.
- For scrapers, shard when the time to scrape all targets approaches the scrape interval.

When NOT to scale:

- The backend cannot keep up, or the network to it is saturated. Adding Collectors may cause harmful side effects.
- The queue stays near capacity even as you raise it. Adding workers only adds pressure to a loaded system.
- `otelcol_exporter_send_failed_spans` keeps rising, meaning sends failed permanently. Scaling likely worsens it.

Stateless Collectors scale by adding replicas behind a load balancer; service meshes such as Istio or Linkerd, or cloud load balancers, are suggested on Kubernetes.

## Checked

Method: docs-checked 2026-11-09 against the opentelemetry.io collector/scaling page (docs repo raw markdown).
