---
id: computing-software.ai-ml-engineering.seldon-core-2.performance-pipeline-sharding-maxshardcountmultiplier
name: performance-pipeline-sharding-maxshardcountmultiplier
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, performance, pipelines, scalability, maxshardcountmultiplier, scalingconfig, consistent-hashing, cooperative-sticky, rebalancing]
level: advanced
status: docs-checked
description: "How Seldon Core 2 spreads pipelines and models over dataflow engine, model gateway and pipeline gateway replicas with consistent hashing and maxShardCountMultiplier."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/performance-tuning/pipelines/scalability-pipelines.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pipeline scalability: sharding across replicas

The dataflow engine, model gateway and pipeline gateway scale horizontally. Each pipeline or model is loaded on a subset of replicas using consistent hashing and rebalanced automatically when replicas change or pipelines and models are deployed or deleted.

## Controlling parameter
`maxShardCountMultiplier` sets the maximum number of replicas on which a pipeline or model loads. Configure it in SeldonConfig at `config.scalingConfig.pipelines.maxShardCountMultiplier`. With helm it defaults to `kafka.topics.numPartitions`. Do not set it above the number of Kafka partitions: that gives no benefit and may drop requests, because extra replicas receive requests but own no partitions in their consumer groups.

Changes propagate in about a minute and trigger a rebalance across `dataflow-engine`, `model-gateway` and `pipeline-gateway`. That may cause downtime depending on the Kafka partition assignment strategy. If your Kafka supports cooperative rebalancing set the strategy to `cooperative-sticky`; the dataflow engine uses a cooperative strategy by default.

## Replicas actually used
- Dataflow engine: min(spec.replicas, pipelines times partitions). With 3 pipelines, multiplier 4 and 9 replicas, 9 are used; with 1 pipeline, 4.
- Model gateway: min(replicas, min(models, maxNumConsumers) times partitions); `maxNumConsumers` defaults to 100.
- Pipeline gateway: min(replicas, min(pipelines, maxNumConsumers) times partitions).

`spec.replicas` in the SeldonRuntime is the maximum replica count. Unused replicas are scaled down automatically.

## Checked

2026-11-04. Confirmed against performance-tuning/pipelines/scalability-pipelines.md (Seldon Core 2 docs, v2 branch): config path, default, partition cap, ~1 minute propagation, cooperative-sticky, replica formulas and examples, maxNumConsumers default 100. Removed or corrected: nothing.

Method: documentation only; no commands were run.
