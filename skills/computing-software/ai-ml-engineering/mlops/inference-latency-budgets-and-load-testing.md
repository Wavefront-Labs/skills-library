---
id: computing-software.ai-ml-engineering.mlops.inference-latency-budgets-and-load-testing
name: inference-latency-budgets-and-load-testing
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, model-serving, inference-load-testing, latency-budget, perf-analyzer, locust, k6, capacity-planning]
level: practitioner
status: draft
description: "Set inference latency budgets and load-test model services: per-stage budget breakdown, open vs closed-loop load, perf_analyzer/locust/k6, finding the knee and replica sizing."
sources:
  - https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/perf_analyzer/README.html
  - https://docs.locust.io/en/stable/
  - https://grafana.com/docs/k6/latest/
  - https://sre.google/sre-book/service-level-objectives/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Inference latency budgets and load testing

**Goal:** know the throughput at which each replica still meets the latency SLO, and size the fleet from that.

## Budget the end-to-end latency
Example 150 ms p99 product budget: network + gateway 20 ms, feature fetch 30 ms, preprocessing 10 ms, model 60 ms, postprocessing + logging 10 ms, 20 ms slack. Measure each stage with tracing spans; the model is often not the biggest part.

## Load-test properly
- **Open-loop** (fixed arrival rate, e.g. k6 `constant-arrival-rate`) reflects real traffic: requests keep arriving while the server is slow. **Closed-loop** (N users waiting for responses) hides queueing - coordinated omission makes latencies look better than reality.
- Use realistic payloads (size and distribution, including long inputs), warm up first (JIT, caches, CUDA graphs), and run long enough (10+ min) to see GC and autoscaling effects.
- Report p50/p95/p99 and error rate per target rate.

```bash
# Triton models: sweep concurrency, measure throughput and latency
perf_analyzer -m resnet50 -u localhost:8001 -i grpc --concurrency-range 1:32:2 --percentile=99 --input-data inputs.json
```
```js
// k6 open-loop
export const options = { scenarios: { s: { executor: "constant-arrival-rate", rate: 200, timeUnit: "1s",
  duration: "10m", preAllocatedVUs: 400 } }, thresholds: { http_req_duration: ["p(99)<150"] } };
```
Locust is convenient for Python-defined user flows.

## Find the knee
Plot throughput and p99 vs offered load: throughput rises linearly, then flattens while p99 climbs steeply. Plan capacity at ~60-70% of the knee throughput per replica to absorb bursts and node loss. Re-measure after model, batch size or hardware changes.

## Levers when over budget
Dynamic batching (throughput up, adds queue delay), smaller/quantized model, compiled runtimes (TensorRT, ONNX Runtime, torch.compile), caching frequent predictions, moving feature computation offline, more replicas (doesn't fix single-request latency).

## Verify
- [ ] Per-stage latency breakdown measured in production traces.
- [ ] Open-loop load test report with knee throughput per replica.
- [ ] Autoscaling target derived from the measured knee.
