---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.observability-architecture
name: observability-architecture
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, management-and-monitoring, management-baseline, observability-architecture, opentelemetry, metrics-logs-traces, telemetry-pipeline, otel-collector]
level: advanced
status: docs-checked
description: "Architect observability: telemetry signals, an OpenTelemetry Collector tier, correlation IDs, consolidation, retention by usage, durable pipelines and telemetry cost."
sources: ["https://opentelemetry.io/docs/concepts/", "https://opentelemetry.io/docs/collector/", "https://learn.microsoft.com/azure/well-architected/operational-excellence/observability", "https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/implement-observability.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Observability architecture

## Signals
- **Metrics**: numerical values collected at regular intervals; they show performance and reliability trends.
- **Logs**: recorded system events; prefer structured logs so they are queryable.
- **Traces**: records of the path of a request through a distributed system.
- **Events** are also part of telemetry. Tie telemetry to KPIs and a health model so collection reflects targets.

## Reference pipeline
Application (OpenTelemetry instrumentation) -> **OpenTelemetry Collector** -> one or more backends.
The Collector is a vendor-agnostic way to receive, process and export telemetry, and removes the need to run
several agents. Its component types are receivers, processors, exporters, connectors and extensions. The OpenTelemetry
docs recommend running a collector alongside the service: the service offloads data quickly and the collector handles
retries, batching, encryption and sensitive data filtering. Sending straight to a backend is fine for trying things
out or small environments. Collector components have mixed stability levels; check each component's README.

## Design decisions
1. **Correlation**: use correlation IDs consistently to follow a transaction through presentation, middle and data
   tiers, and use them to merge related events.
2. **Semantic conventions**: OpenTelemetry defines common names for operations and data; use them for consistency.
3. **Sampling**: OpenTelemetry has a Sampling concept with several options; decide deliberately. For profiling, the
   Azure guide says to sample when events are frequent and use fuller profiling when events are rare.
4. **Verbosity**: verbose logging in development, reduced in production, with correlation IDs preserving end-to-end
   visibility (higher detail costs storage and processing).
5. **Retention**: keep high-resolution data short term and lower-resolution aggregates for long-term trends; move
   older data to cheaper storage; match retention to operational and compliance needs.
6. **Regions and tenants**: for multiregion workloads collect regionally first, then aggregate centrally; for
   business-critical workloads the Azure guide recommends autonomous storage of data. Both options carry cost.
7. **Sensitive data**: scrub sensitive system or user information before logging, keeping enough context to diagnose.
8. **Durability**: include buffering, queuing and scalable ingestion; use at-least-once queues for complex workloads.
9. **Cost**: telemetry has storage and processing cost; govern ingestion and routing before widening distribution.

## Gotchas
- Instrumentation tightly bound to one backend; keep it extensible and decoupled.
- Telemetry failures cascading into application failures; logging should be fire-and-forget except for critical auditing.
- Mixing workload data with telemetry.

## Verify
- [ ] A single request can be followed across tiers through correlation IDs in logs and traces.
- [ ] Telemetry cost and retention are reviewed per environment.

## Checked
2026-11-08. Confirmed against the OpenTelemetry Collector page (vendor-agnostic receive/process/export, when to use a
collector, retries/batching/encryption/filtering, component types, mixed stability), the OpenTelemetry concepts index
(semantic conventions, sampling, context propagation) and the Azure Well-Architected monitoring design guide
(correlation IDs, structured telemetry, consolidation, retention, regional then central, pipeline durability, profiling
sampling note). The AWS observability page lists the OPS04 best practices only. Removed: RED/USE, W3C Trace Context,
processor names, tail sampling, backend product list, cardinality and cost-estimate specifics (not stated on the pages).
Method: documentation only; no commands were run.
