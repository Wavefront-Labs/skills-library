---
id: computing-software.ai-ml-engineering.seldon-core-2.dataflow-paradigm-and-kafka-backbone
name: dataflow-paradigm-and-kafka-backbone
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, dataflow, kafka, kafka-streams, pipelines, architecture]
level: intro
status: docs-checked
description: "Why Seldon Core 2 replaced the v1 central orchestrator with a Kafka dataflow design, and what that gives: async mode, no single point of failure, lineage, shared nodes."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/architecture/dataflow.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Dataflow design with Kafka

## Why v1 changed
Seldon Core v1 modelled an inference graph, but ran it through a central orchestrator that knew the topology and called each service in order. That orchestrator became a bottleneck and a single point of failure, hid the data transformations between services, and made lineage hard to trace.

## How Core 2 evaluates a graph
Core 2 follows the data flow paradigm and runs on Kafka. An inference request is put on a pipeline input topic, which triggers evaluation. Each model sits behind a model gateway that reads its input Kafka topic, calls the model server, and writes the response to its output topic. A pipeline gateway offers a synchronous service API on top, for v1-style use.

## What this buys you
- Both synchronous and asynchronous operation: send data to the input topic and read the result later from the output topic.
- No single point of failure: if a node in the graph is down, data waits on the streams and evaluation resumes when it returns.
- Intermediate data can be inspected or collected at any step, giving lineage, context from other parts of the graph, fewer false-positive alerts and reproducible results.
- New nodes can be added at arbitrary places without affecting pipeline execution, and several pipelines can share common nodes to save resources.

Join types (inner, outer, triggers) are explained in the pipeline skills.

## Checked

Confirmed against the Dataflow with Kafka architecture page: the v1 orchestrator problems, the Kafka-based evaluation with model gateway and pipeline gateway, synchronous and asynchronous operation, no single point of failure, lineage benefits, and adding or sharing nodes.

Method: docs-checked 2026-11-09 against the Seldon Core v2 docs-gb architecture/dataflow.md page (raw markdown).
