---
id: computing-software.ai-ml-engineering.pytorch.diagnosing-kernel-launch-overhead
name: diagnosing-kernel-launch-overhead
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, kernel-launch-overhead, cpu-bound, cuda-graphs, python-overhead, small-batch]
level: practitioner
status: draft
description: "Recognise and fix CPU-bound PyTorch workloads where kernel launches dominate: profiler signatures, batch sizing, torch.compile, CUDA graphs and fused ops."
sources:
  - https://pytorch.org/tutorials/recipes/recipes/tuning_guide.html
  - https://pytorch.org/docs/stable/notes/cuda.html#cuda-graphs
  - https://pytorch.org/blog/accelerating-pytorch-with-cuda-graphs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Diagnosing CPU-bound / kernel-launch-overhead workloads

**Symptom:** GPU utilization is low but the data loader is not the problem; small batches or small models (RL policies, LLM decode, tiny MLPs) run barely faster on a big GPU than a small one.

## Signature
- In the profiler or Nsight timeline: many short kernels (a few microseconds) with gaps between them, and the CPU thread constantly in `cudaLaunchKernel`.
- Each eager op costs roughly 5-20 microseconds of CPU dispatch; a kernel that runs in 3 microseconds cannot keep the GPU busy.
- Quick test: double the batch size. If step time barely changes, you are overhead bound.

```python
from torch.profiler import profile, ProfilerActivity
with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA]) as p:
    for _ in range(10): step()
print(p.key_averages().table(sort_by="self_cpu_time_total", row_limit=15))
```
CPU self time far above CUDA time per op confirms it.

## Fixes
1. **Bigger work per launch:** increase batch size, batch environments/requests, fuse small layers.
2. **torch.compile:** fuses pointwise ops into fewer kernels and removes Python dispatch; `mode="reduce-overhead"` adds CUDA graphs.
3. **CUDA graphs** (manual `torch.cuda.CUDAGraph` or via compile): replay a whole step with one launch; requires static shapes and static memory addresses.
4. **Fused implementations:** `fused=True` optimizers, `F.scaled_dot_product_attention`, fused LayerNorm/RMSNorm, apex/Liger kernels.
5. **Remove Python-side work** from the loop: per-step logging with `.item()`, list comprehensions over parameters, dynamic module creation.
6. **For LLM decode:** use a serving engine (vLLM, SGLang, TensorRT-LLM) that already uses CUDA graphs and continuous batching.

## Verify
- [ ] Kernel count per step (from profiler) and step time before/after.
- [ ] GPU active time / step time ratio increases (Nsight or `torch.cuda.Event` timing).
