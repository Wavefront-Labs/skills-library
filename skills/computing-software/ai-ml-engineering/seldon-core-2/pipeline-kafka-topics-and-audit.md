---
id: computing-software.ai-ml-engineering.seldon-core-2.pipeline-kafka-topics-and-audit
name: pipeline-kafka-topics-and-audit
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, pipeline, kafka-topics, audit, replay, async-inference, tracing]
level: practitioner
status: docs-checked
description: "Pipelines run on Kafka: every step input and output has a topic, which gives audit, replay and debugging, and lets you read results asynchronously."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/pipelines.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pipeline Kafka topics, audit and replay

Pipelines are implemented using Kafka. Each input and output of a pipeline step has an associated Kafka topic, so data from every step is preserved. That makes auditing, replay and debugging easier.

## What you get
- Full audit: as a request moves through the steps, its data appears in the step input and output topics, so every transformation can be inspected.
- Asynchronous use: besides synchronous HTTP/gRPC, a pipeline can be fed and read through the Kafka topics created for it.
- Latency visibility: tracing monitors the processing latency of pipelines.

## Practical use
A pipeline can have paths that do not reach the output, for example drift detection steps. The architecture page says new nodes can be added to an inference graph without affecting pipeline execution.

Pipelines can be deployed before or at the same time as their models, and the models must be available for the pipeline to function.

## Related
Topic naming and cleanup are covered in the Kafka topic lifecycle skill.

## Checked

Confirmed against the Pipelines page (Data Centric Implementation section) and the dataflow architecture page: Kafka topics per step input and output, audit, replay and debugging, tracing for latency, synchronous and asynchronous use, and models needing to be available. Removed the seldon pipeline inspect command and the claim that non-output steps are handled asynchronously, which these pages do not state.

Method: docs-checked 2026-11-09 against the Seldon Core v2 docs-gb pipelines.md and architecture/dataflow.md pages (raw markdown).
