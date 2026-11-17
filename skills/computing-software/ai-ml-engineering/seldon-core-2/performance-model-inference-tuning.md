---
id: computing-software.ai-ml-engineering.seldon-core-2.performance-model-inference-tuning
name: performance-model-inference-tuning
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, performance, mlserver, parallel-workers, adaptive-batching, grpc, input-size, model-artefact, quantization]
level: advanced
status: docs-checked
description: "Speed up Seldon Core 2 inference: prefer gRPC for binary payloads, use MLServer adaptive batching and parallel_workers, shrink inputs, and prune or quantize the model artefact."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/performance-tuning/models/inference.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Inference performance tuning

## Request-level options
- gRPC can beat REST when the payload benefits from binary serialisation.
- Group real-time requests into small batches with MLServer adaptive batching to raise throughput while keeping latency acceptable.
- Reduce input dimensions to speed processing and cut (de)serialisation overhead.
- For MLServer models, set `parallel_workers` in line with the CPU cores assigned to the Server pod. It helps synchronous models, CPU-bound async models and I/O-bound async models with high throughput, and can steady the latency distribution.

## Parallel workers
MLServer runs inference through a pool of worker processes. Measure the one-worker maximum throughput and the n-worker maximum throughput. The n-worker figure is not n times the one-worker figure. If workers wait on I/O or a GPU, setting workers above the CPU count can raise throughput. If traffic is below the one-worker maximum, extra workers add little. Raise workers up to or slightly above the core count when saturated and the pod has spare CPU.

## Model artefact
The model architecture, size, weight precision and input size set the inherent cost. Options:
- Pruning of unimportant parameters.
- Quantization to lower precision weights and activations.
- Dimensionality reduction of inputs.
- Efficient architectures such as MobileNet, EfficientNet or DistilBERT.
- Optimised formats and runtimes such as ONNX Runtime, TensorRT or OpenVINO.

## Checked
Method: docs-checked 2026-11-09 against docs-gb/performance-tuning/models/inference.md (read in full).
