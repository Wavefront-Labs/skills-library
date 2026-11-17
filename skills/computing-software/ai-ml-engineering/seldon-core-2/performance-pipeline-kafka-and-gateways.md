---
id: computing-software.ai-ml-engineering.seldon-core-2.performance-pipeline-kafka-and-gateways
name: performance-pipeline-kafka-and-gateways
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, performance, pipelines, kafka-partitions, modelgateway, modelgateway-num-workers, modelgateway-max-num-consumers, pipelinegateway, dataflow-engine]
level: advanced
status: docs-checked
description: "Cut pipeline overhead in Seldon Core 2: low latency to Kafka, replicas matching partitions, and modelgateway MODELGATEWAY_NUM_WORKERS and MAX_NUM_CONSUMERS."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/performance-tuning/pipelines/core-2-configuration.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pipeline overhead: Kafka and gateway settings

Four components create data-processing overhead in a pipeline: `pipelinegateway`, `modelgateway`, `dataflow-engine` and the Kafka cluster.

## Kafka
Lower the network latency between Core 2 and Kafka, especially when Kafka is in a separate cluster. The partitions per topic, which must be fixed across all models in a pipeline, set Kafka maximum throughput and the effective replica count of `pipelinegateway`, `dataflow-engine` and `modelgateway`.

## Replica baseline
For high RPS across many pipelines use as many replicas of `pipelinegateway` and `dataflow-engine` as Kafka topic partitions. Each `dataflow-engine` then processes one partition across all pipelines.

## modelgateway
Throughput rises with workers and replicas. Two environment variables:
- `MODELGATEWAY_NUM_WORKERS`: lightweight inference workers (goroutines) per consumer that forward requests to inference servers and wait for responses.
- `MODELGATEWAY_MAX_NUM_CONSUMERS`: size of the hash table assigning models to consumers within a namespace. Each model in a namespace is consistently assigned to one consumer by its index in the table; the table size influences how many models share a consumer.

Raise workers first, then consumers, provided the `modelgateway` pod has the resources.

## Checked
Method: docs-checked 2026-11-09 against docs-gb/performance-tuning/pipelines/core-2-configuration.md (read in full).
