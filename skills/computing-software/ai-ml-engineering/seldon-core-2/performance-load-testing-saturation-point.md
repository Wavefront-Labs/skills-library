---
id: computing-software.ai-ml-engineering.seldon-core-2.performance-load-testing-saturation-point
name: performance-load-testing-saturation-point
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, performance, load-testing, open-loop, closed-loop, coordinated-omission, saturation-point, latency-percentiles]
level: advanced
status: docs-checked
description: "Load test Seldon Core 2 models: find the single-replica saturation point with a staged open-loop test, avoid coordinated omission, and keep a 10 to 20 percent margin."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/performance-tuning/models/load-testing.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Load testing models and finding the saturation point

Load test before tuning, to learn how a model behaves on MLServer or Triton when saturated, that is at the maximum throughput one replica can handle.

## Saturation point
The load saturation point is the maximum throughput one model replica can sustain. Above it, latency degrades because of queuing at the bottleneck (a model step, or contention on CPU, memory or network). Find it with an open-loop test in stages: each stage ramps linearly to a target RPS and holds it for a set time, and the target RPS rises monotonically between stages.

Run each replica with a margin below saturation, say 10 to 20 percent, so latency does not degrade and there is spare capacity while new server and model replicas start. Use the result to set autoscaling parameters.

## Closed loop versus open loop
- Closed loop: each virtual user waits for a response before sending the next request. When the system overloads, users send less often, which hides the overload (coordinated omission), so reported latency at a given throughput can be much smaller than reality.
- Open loop: a constant RPS is held, giving a more accurate picture of production latency. Check your tool (Locust, k6) for the workload model.

## Good practice
- Track latency percentiles such as p50, p90, p95 and p99.
- For reproducible results, run the servers under test on nodes where other components are not using much shared compute, memory or IO.

## Checked
Method: docs-checked 2026-11-09 against docs-gb/performance-tuning/models/load-testing.md (read in full).
