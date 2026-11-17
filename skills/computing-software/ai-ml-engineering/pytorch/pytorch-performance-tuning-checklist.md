---
id: computing-software.ai-ml-engineering.pytorch.pytorch-performance-tuning-checklist
name: pytorch-performance-tuning-checklist
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, performance-tuning-guide, scaled-dot-product-attention, channels-last, fused-optimizer, throughput]
level: practitioner
status: gated
description: "Work through the PyTorch performance checklist: SDPA/flash attention, channels_last, fused optimizers, TF32/bf16, torch.compile, data loading and sync removal."
sources:
  - https://pytorch.org/tutorials/recipes/recipes/tuning_guide.html
  - https://pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html
  - https://pytorch.org/tutorials/intermediate/memory_format_tutorial.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PyTorch performance tuning checklist

Profile first; apply in roughly this order, re-measuring each. This machine has no GPU, so speedup figures and CUDA-only behaviour below were not measured (gated: unconfirmed, source is paywalled or blocked); API names, defaults and CPU-side behaviour were run on torch 2.14.

## 1. Input pipeline
`num_workers` > 0, `pin_memory=True`, `persistent_workers=True`, `non_blocking=True` copies. GPU must not wait on data (see the input-bound skill; `persistent_workers=True` needs `num_workers > 0`).

## 2. Remove host syncs
No `.item()` / `print(tensor)` / `.cpu()` every step; `torch.cuda.set_sync_debug_mode("warn")` finds them (raises `AssertionError: Torch not compiled with CUDA enabled` on a CPU build, not run on a GPU). Use `optimizer.zero_grad(set_to_none=True)` (it is the default: the signature reads `set_to_none=True` on 2.14).

## 3. Precision
- bf16 autocast (Ampere+) or fp16 + GradScaler.
- `torch.set_float32_matmul_precision("high")` for remaining fp32 matmuls.
- Dimensions multiple of 8 (fp16/bf16) or 16 (FP8/int8) for tensor cores: vocab size, hidden size, batch size. Padding vocab from 50257 to 50304 makes it a multiple of 8 and of 64 (50257 % 8 = 1); the GPT-2 speedup from doing so is a community claim not measured here (gated: unconfirmed, source is paywalled or blocked).

## 4. Attention: use SDPA
```python
out = F.scaled_dot_product_attention(q, k, v, attn_mask=None, dropout_p=0.0, is_causal=True)
```
Dispatches to FlashAttention, memory-efficient attention or math kernels on CUDA (backend choice on a GPU not run). Check which ran:
```python
from torch.nn.attention import sdpa_kernel, SDPBackend
with sdpa_kernel(SDPBackend.FLASH_ATTENTION): out = F.scaled_dot_product_attention(q, k, v, is_causal=True)
```
Forcing a backend raises if unsupported: on the CPU build, `SDPBackend.EFFICIENT_ATTENTION` and `CUDNN_ATTENTION` raised `RuntimeError: No viable backend for scaled_dot_product_attention was found`, while `FLASH_ATTENTION` and `MATH` ran. The CUDA limits quoted in older notes (flash needs fp16/bf16, head dim <= 256, an explicit `attn_mask` rules flash out) did not apply to the CPU flash kernel, which accepted fp32, a boolean mask and head dim 512; check the limits for your GPU backend in the docs (not run) (gated: unconfirmed, source is paywalled or blocked). Use `is_causal=True` instead of a causal mask. `torch.nn.attention.flex_attention` imports on 2.14 (custom masks with compiled kernels; compiled use needs a compiler, not run).

## 5. Memory format for CNNs
```python
model = model.to(memory_format=torch.channels_last); x = x.to(memory_format=torch.channels_last)
```
`channels_last` conversion works (`is_contiguous(memory_format=torch.channels_last)` was True). The 10-30% speedup with AMP on tensor cores was not measured (gated: unconfirmed, source is paywalled or blocked). Not useful for transformers.

## 6. Fused / foreach optimizers
`torch.optim.AdamW(..., fused=True)` (`fused` and `foreach` are `bool | None` parameters; `fused=True` also stepped on CPU in 2.14). The "big win for many small parameter tensors" was not measured (gated: unconfirmed, source is paywalled or blocked).

## 7. torch.compile
`model = torch.compile(model)`; fix graph breaks (see the backends skill); consider `mode="max-autotune"` for inference (a suggestion, not benchmarked).

## 8. cuDNN autotune
`torch.backends.cudnn.benchmark = True` when input shapes are fixed (default reads False). With variable shapes it re-tunes each new shape: leave off (cuDNN behaviour not run) (gated: unconfirmed, source is paywalled or blocked).

## 9. Batch size and memory
Increase batch until near memory limit (with LR adjusted); use activation checkpointing (`torch.utils.checkpoint.checkpoint(block, x, use_reentrant=False)`) to fit larger batches/models.

## 10. Distributed
DDP `gradient_as_bucket_view=True`, `static_graph=True` when applicable; tune `bucket_cap_mb` (all three are `DistributedDataParallel.__init__` parameters on 2.14); overlap comms (verify in trace; not run).

## Disable debug features in production runs
`torch.autograd.set_detect_anomaly(False)`, `torch.autograd.profiler.emit_nvtx` off (both exist), no `CUDA_LAUNCH_BLOCKING`.

## Verify
Track one number (samples/s or tokens/s at fixed quality) in a table per change; keep only changes that help and don't change the loss curve.
