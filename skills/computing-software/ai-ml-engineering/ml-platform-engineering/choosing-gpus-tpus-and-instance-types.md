---
id: computing-software.ai-ml-engineering.ml-platform-engineering.choosing-gpus-tpus-and-instance-types
name: choosing-gpus-tpus-and-instance-types
category: computing-software
field: ai-ml-engineering
product: ml-platform-engineering
tags: [ml-platform, gpu, accelerator-selection, tpu, gpu-memory-estimation, instance-selection, training-compute]
level: practitioner
status: draft
description: "Choose accelerators for training and inference: memory estimates (weights, optimizer, activations, KV cache), GPUs vs TPUs, and cost-per-throughput benchmarks."
sources:
  - https://huggingface.co/docs/transformers/main/en/model_memory_anatomy
  - https://cloud.google.com/tpu/docs/intro-to-tpu
  - https://docs.aws.amazon.com/ec2/latest/instancetypes/ac.html
  - https://arxiv.org/abs/1910.02054
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choosing GPUs, TPUs and instance types

**Goal:** pick the cheapest hardware that fits the job's memory and finishes within the time budget.

## Estimate memory first
**Training (mixed precision, Adam):** about 16-18 bytes per parameter for weights (bf16 + fp32 master copy), gradients and the two Adam moments - before activations (ZeRO paper accounting). A 7B model needs ~120 GB for states alone: it doesn't fit one 80 GB GPU without sharding (FSDP/ZeRO), LoRA, or 8-bit optimizers.
**Activations:** scale with batch x sequence length x layers x hidden; activation checkpointing trades compute for memory.
**Inference:** weights (2 bytes/param bf16, ~0.5-0.6 for 4-bit) + **KV cache** = `2 x layers x kv_heads x head_dim x seq_len x batch x bytes`. Long-context, high-concurrency serving is often KV-bound, not weight-bound.

## Accelerator classes (check current generations)
| Need | Typical choice |
|---|---|
| Large-scale LLM pre-training / big fine-tunes | latest high-memory data-centre GPUs (H100/H200/B-series class) with NVLink + fast inter-node fabric, or TPU pods |
| Mid-size training, research | previous-gen data-centre GPUs (A100-class) - often far cheaper and more available |
| Inference of small/medium models, video, CV | inference GPUs (L4/L40S-class) or CPUs for classical ML |
| Very large-batch JAX/TF workloads, cost-efficient scale | TPUs (v5e/v5p/later), via JAX or PyTorch/XLA |
| Tabular/classical ML | CPUs; GPUs only for GPU-native libraries (XGBoost/cuML) at scale |

## TPU considerations
Best with JAX (or Keras on JAX); PyTorch/XLA works but expect graph-compilation friction (dynamic shapes, Python control flow). Pods give very fast interconnect for large data/model parallelism. Availability is region-specific.

## Benchmark before committing
Run the real training step or serving load for 30-60 minutes on 2-3 candidates; compare **cost per unit of work** (tokens/$, images/$, requests/$ at SLO), not price per hour. Newer GPUs often cost more per hour and less per token, especially with FP8/bf16 kernels.

## Also check
Interconnect for multi-node jobs, local NVMe for data staging, CPU RAM for dataloaders, quota/availability in your regions, driver/CUDA support for your framework versions.

## Verify
- [ ] Written memory estimate for training and serving configurations.
- [ ] Cost-per-throughput benchmark on candidate instances.
- [ ] Quota/capacity confirmed in the target region.
