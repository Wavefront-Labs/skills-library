---
id: computing-software.ai-ml-engineering.seldon-core-2.async-inference-via-kafka
name: async-inference-via-kafka
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, inference, async-inference, kafka, kafka-topics, pipeline-header, protobuf-payload]
level: practitioner
status: docs-checked
description: "Send asynchronous inference to Seldon Core 2 by producing v2 payloads to Kafka input topics and reading outputs topics, with the required pipeline Kafka header for pipelines."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/inference.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Asynchronous inference through Kafka

Push v2 protocol payloads to the input topic of a model or pipeline and read the response from the matching output topic. Kafka payloads must be Protobuf v2.

## Topic pattern
```
seldon.<namespace>.<model|pipeline>.<name>.<inputs|outputs>
```

## Models
- Local install, model `iris`: produce to `seldon.default.model.iris.inputs`, read `seldon.default.model.iris.outputs`.
- Kubernetes in `seldon-mesh`: produce to `seldon.seldon-mesh.model.iris.inputs`, read `seldon.seldon-mesh.model.iris.outputs`.

## Pipelines
- Local, pipeline `mypipeline`: `seldon.default.pipeline.mypipeline.inputs` and `.outputs`.
- Kubernetes in `seldon-mesh`: `seldon.seldon-mesh.pipeline.mypipeline.inputs` and `.outputs`.
- When writing to a pipeline topic, add a Kafka header with key `pipeline` and the pipeline name as value.

## Metadata
Kafka metadata attached to your request is passed around the graph.

## Notes
See the topic lifecycle skill for topic cleanup.

## Checked

Confirmed against the Inference page (Asynchronous Requests section): Protobuf requirement for Kafka payloads, the topic name pattern, the model and pipeline topic examples for local and seldon-mesh installs, the pipeline Kafka header, and metadata passing. Removed the topicPrefix and topic persistence statements, which this page does not state.

Method: docs-checked 2026-11-09 against the Seldon Core v2 docs-gb inference.md page (raw markdown).
