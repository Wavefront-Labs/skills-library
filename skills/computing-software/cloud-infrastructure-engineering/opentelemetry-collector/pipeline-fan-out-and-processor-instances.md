---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.pipeline-fan-out-and-processor-instances
name: pipeline-fan-out-and-processor-instances
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, pipeline, fan-out, processors, architecture]
level: advanced
status: docs-checked
description: "How data flows through Collector pipelines: receivers fan out to every pipeline, and each pipeline gets its own processor instances."
sources:
  - https://opentelemetry.io/docs/collector/architecture/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A pipeline is receivers, then processors, then exporters, for one signal type.

Fan-out: when a receiver is listed in more than one pipeline, the Collector sends every item it receives to all of those pipelines. Likewise an exporter listed in several pipelines receives data from each.

Processor instances: each pipeline gets its own instance of every processor it references, even when the same processor name appears in several pipelines. State is therefore not shared. For example, a `transform` processor used in two pipelines is two independent instances configured the same way. The same processor name must not be referenced more than once in a single pipeline.

Blocking: the call from receiver to fan-out consumer to the first processors is synchronous. If one processor blocks the call, the other pipelines attached to that receiver are blocked from receiving the same data, and the receiver itself stops processing and forwarding newly received data.

## Checked

Method: docs-checked 2026-11-09 against the opentelemetry.io collector/architecture page (docs repo raw markdown).
