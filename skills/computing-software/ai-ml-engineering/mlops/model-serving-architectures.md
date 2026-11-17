---
id: computing-software.ai-ml-engineering.mlops.model-serving-architectures
name: model-serving-architectures
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, model-serving, inference, batch-inference, online-inference, latency, throughput, autoscaling, dynamic-batching, triton, torchserve, model-caching, cold-start, gpu-serving, embedding-serving]
level: advanced
status: draft
description: "Choose and build the right model-serving pattern: batch vs online vs streaming, dynamic batching for GPU throughput, autoscaling, and the latency/cost tradeoffs each implies."
sources:
  - https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/index.html
  - https://pytorch.org/serve/
  - https://cloud.google.com/vertex-ai/docs/predictions/overview
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Model serving architectures — matching the pattern to the latency/cost budget

**Goal:** pick batch, online, or streaming inference deliberately based on the actual latency requirement and traffic shape, then build the serving layer so it uses GPU/CPU efficiently instead of either idling or falling over under load.

## 1. Pick the pattern first
- **Batch inference**: run predictions on a large input set on a schedule (nightly scoring, feature precomputation), write results to a store, serve reads from that store at request time. Use when the prediction doesn't need to reflect data from the last few minutes and the entity set is enumerable (all users, all SKUs). Cheapest per-prediction, highest throughput, zero online latency risk — but predictions are stale by up to the batch interval.
- **Online (real-time) inference**: a request triggers a live forward pass, typically behind a REST/gRPC endpoint, latency budget in the tens to low hundreds of milliseconds. Needed when the input isn't known ahead of time (a live user action, free-text query) or freshness matters (fraud scoring on the current transaction).
- **Streaming inference**: predictions computed continuously as events arrive (Kafka/Kinesis consumer calling the model per event or per micro-batch), output written to a stream or store. Use for near-real-time aggregate scoring (anomaly detection over an event stream) where neither "whole dataset nightly" nor "one request at a time" fits.
- Many systems use **more than one simultaneously**: batch-precompute embeddings nightly, serve online by doing a fast lookup + a lightweight online re-rank — decide this split by what actually needs freshness versus what's expensive to compute (don't put the expensive forward pass on the request path if it can be precomputed).

## 2. Online serving: the knobs that actually move latency/throughput
- **Dynamic batching**: group concurrent incoming requests into a single forward-pass batch inside a short time window (a few milliseconds to ~50ms) to use GPU parallelism; frameworks like NVIDIA Triton and TorchServe do this for you via config, not custom code. The window size trades latency (longer window = more batching = higher throughput, worse p99 latency for an unlucky early request) against throughput — tune it against your actual p99 SLO, not a default.
- **Model format matters for throughput**: a plain Python/PyTorch eager model is the slowest serving path; `torch.compile`, ONNX export, or TensorRT compilation typically give 1.5–5x throughput gains on the same hardware — benchmark before assuming the model itself needs to shrink.
- **Separate CPU-bound preprocessing from GPU-bound inference** into different pool sizes/processes — a slow tokenizer or image-decode step run on the same process as the GPU forward pass serializes work that could overlap, and is the most common hidden bottleneck in "the GPU is only 30% utilized" complaints.
- **Cold starts**: a scaled-to-zero or newly-scheduled replica pays model-load time (disk read, CUDA context init, sometimes a JIT/compile warm-up) before serving its first request — this can be seconds to tens of seconds for large models. If traffic is bursty, keep a minimum warm replica count rather than relying purely on scale-from-zero, or pre-warm with a synthetic request after deploy before routing real traffic.
- **Autoscaling signal**: scale on request queue depth or in-flight request count, not raw CPU%, for GPU-bound services — GPU utilization and CPU utilization are often decoupled, and CPU-based autoscaling under- or over-reacts.

## 3. Common architecture mistakes
- Putting a large embedding/feature lookup (a network call to a feature store) *inside* the critical request path without a cache — adds a second network hop's tail latency on top of inference; cache hot keys locally (even a small in-process LRU) when the feature changes slowly.
- No request-level timeout/fallback: a model service with no hard timeout means one slow GPU (thermal throttling, a stuck batch) cascades into the caller's timeout and retries pile up — set a timeout shorter than the caller's, and define a fallback (cached last-known prediction, a simpler heuristic model, or a documented default) rather than a hard failure for latency-critical paths.
- Shipping a new model format/runtime (e.g. moving from PyTorch eager to a compiled TensorRT engine) straight to 100% of production traffic — validate numerically (same inputs, compare outputs within tolerance) before the performance win, since compilation and quantization can silently change output slightly.
- Sizing GPU serving fleets off average load instead of peak — GPU instances are expensive and slow to provision; undersizing for peak causes queueing that looks like a model problem but is a capacity problem. Load-test at the actual expected peak QPS, not average.

## Verify
- [ ] Serving pattern (batch/online/streaming) chosen based on documented freshness and latency requirements, not habit.
- [ ] Dynamic batching window tuned against measured p99 latency, not left at a framework default.
- [ ] Preprocessing and GPU inference run in separately sized pools; GPU utilization measured, not assumed.
- [ ] Cold-start behavior measured; a minimum warm pool or pre-warm step exists if traffic is bursty.
- [ ] Every online-serving call path has a timeout and a defined fallback on timeout/error.
- [ ] A new serving runtime/format validated for numerical parity against the previous one before full rollout.
