---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-performance-tuning
name: jaeger-performance-tuning
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, performance-tuning, collector-scaling, save-latency, ingester-partitions]
level: advanced
status: docs-checked
description: "Tune Jaeger by scaling collectors, checking storage latency, and buffering with Kafka where bursts exceed storage."
sources:
  - https://www.jaegertracing.io/docs/2.22/operations/performance-tuning/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stop spans being dropped under load.

Jaeger buffers and batches data; when more spans arrive than it can safely process, spans may be dropped, and defaults may not suit every case. Jaeger v2 is based on the OpenTelemetry Collector, so most of its Scaling the Collector advice applies.

- Scale collectors up and down with your platform's auto-scaling; collectors are nearly horizontally scalable. Add instances when platform auto-scaling is available, when starting instances is easier than changing running ones, or to spread CPU.
- Make sure storage keeps up. Each span is written by one worker that blocks until it is stored. If storage is slow, too many workers block and spans drop. The histogram `jaeger_collector_save_latency_bucket` helps diagnose this (latency should stay flat over time), but the docs state it is not yet available in Jaeger v2.
- Consider Kafka as intermediate buffer where traffic spikes are frequent but storage catches up later. Collectors scale as before; trace IDs shard Kafka partitions and each collector can write to any partition. Ingesters negotiate and rebalance partitions automatically, but more ingesters than partitions leaves some idle.

## Checked

2026-11-08: confirmed against the Jaeger 2.22 Performance Tuning Guide, read in full. Removed the pointer to `otelcol_*` counters, which that page does not mention.

Method: documentation only; no commands were run.
