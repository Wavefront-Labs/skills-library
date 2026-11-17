---
id: computing-software.ai-ml-engineering.seldon-core-2.performance-pipeline-critical-path
name: performance-pipeline-critical-path
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, performance, pipelines, critical-path, bottleneck, linear-pipeline, throughput]
level: advanced
status: docs-checked
description: "Test Seldon Core 2 pipelines by first measuring each model, then finding the critical path; pipeline latency is the sum along that path plus per-stage Kafka overhead."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/performance-tuning/pipelines/testing-pipelines.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pipeline performance: critical path and bottlenecks

Start by testing each model in the pipeline alone, to get its maximum throughput on its infrastructure (for example GPU specs) and configuration (for example worker count). That shows which models limit the pipeline.

## Latency components
Pipeline request latency is:
1. The sum of the latencies of each model on the critical path (the path with the bottleneck).
2. Per-stage data processing overhead from pipeline operations: data movement, copying, writing to Kafka topics.

## Linear pipelines
The maximum throughput of a chain is the minimum of the maximum throughputs of its models, for a given number of workers. Pushing past that creates a bottleneck and degrades the pipeline. To remove it:
- Give the model server more resources and more workers.
- Add model replicas to share the load; autoscaling can set the right number.

## Non-linear pipelines
Identify the critical path, the path holding the model whose throughput saturates first, then apply the same fixes to bottleneck models on that path. There is always a bottleneck model in a pipeline; the goal is to balance replicas, MLServer resources and workers so each stage handles the request throughput with as little queueing between stages as possible.

## Checked
Method: docs-checked 2026-11-09 against docs-gb/performance-tuning/pipelines/testing-pipelines.md (read in full). Replaced an unsupported closing instruction with the page's stated goal.
