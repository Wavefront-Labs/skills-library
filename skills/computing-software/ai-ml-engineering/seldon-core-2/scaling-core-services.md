---
id: computing-software.ai-ml-engineering.seldon-core-2.scaling-core-services
name: scaling-core-services
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, scaling, pipeline-gateway, model-gateway, dataflow-engine, scheduler, envoy, kafka-partitions, controller]
level: advanced
status: docs-checked
description: "How to scale each Seldon Core 2 core service: stateless pipeline gateway, model gateway up to Kafka partitions, dataflow engine replicas, single scheduler, controller and Envoy."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/scaling/scaling-core-services.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Scaling the core services

When running Core 2 at scale, treat each service separately.

- Pipeline gateway: stateless, handles synchronous REST and gRPC calls to Pipelines. Scale on traffic demand.
- Model gateway: pulls model requests from Kafka and sends them to inference servers. It scales up to the partition factor of your Kafka topics. At present one uniform partition factor applies to all topics in an installation.
- Dataflow engine: runs KStream topologies for Pipelines. It can run multiple replicas, and the scheduler balances pipelines across them with a consistent hashing load balancer. Each pipeline is managed up to the partition factor of Kafka (currently hardwired to one). Use as many dataflow-engine replicas as Kafka partitions to benefit from hashing.
- Scheduler: control plane operations. It must be a single replica because it keeps state in BadgerDB on local persistent storage (a StatefulSet). Performance tests show it is not a bottleneck.
- Kubernetes Controller: passes resource updates to the Scheduler. One replica by default, but it can scale.
- Envoy: replicas get routing state from the scheduler and can be scaled as needed.

## Checked
Method: docs-checked 2026-11-09 against docs-gb/scaling/scaling-core-services.md (read in full). Dropped an unsupported pointer paragraph about pipeline throughput settings.
