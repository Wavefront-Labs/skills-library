---
id: computing-software.ai-ml-engineering.pytorch.debugging-nan-and-oom
name: debugging-nan-and-oom
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, nan, inf, exploding-gradients, oom, cuda-out-of-memory, anomaly-detection, gradient-checkpointing, torch-profiler, memory-fragmentation, debugging, deep-learning, loss-spikes, numerical-stability]
level: advanced
status: gated
description: "Diagnose NaN/Inf losses and CUDA OOM in PyTorch: anomaly detection, gradient norms, autocast pitfalls, activation checkpointing and the memory profiler."
sources:
  - https://pytorch.org/docs/stable/autograd.html#anomaly-detection
  - https://pytorch.org/docs/stable/notes/cuda.html#memory-management
  - https://pytorch.org/docs/stable/checkpoint.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging NaN losses and CUDA OOM in PyTorch

**Goal:** find the root cause of a NaN/Inf loss or an out-of-memory crash fast, instead of guessing at learning rates.

## 1. NaN/Inf triage order
1. Check the **data** first: `torch.isnan(x).any()` / `isinf` on inputs and labels before the forward pass. A single corrupt row (div-by-zero feature, log(0) target) is the most common cause and training-code changes won't fix it.
2. Check the **loss function** for domain violations: `log`, `sqrt`, `/` on values that can hit 0 or negative. `BCELoss` on raw logits is not silent on torch 2.14: `F.binary_cross_entropy(torch.tensor([2.0,-1.0]), ...)` raises `RuntimeError: all elements of input should be between 0 and 1` (use `BCEWithLogitsLoss` on logits). `torch.log(torch.tensor(0.))` is `-inf` and an unguarded division gives Inf that surfaces a few steps later as NaN, whereas `BCELoss` itself clamps its log terms (probability exactly 0 for a target of 1 gave a loss of 100).
3. Turn on `torch.autograd.set_detect_anomaly(True)` for one run — it slows training a lot but raises `RuntimeError: Function 'SqrtBackward0' returned nan values in its 0th output` and attaches a traceback of the forward line that created that op (checked with `sqrt(0)*0`; without it the gradient was silently `[nan, 0.]`), not just the layer where you noticed it. Remove it afterward; never ship it on.
4. Log the **gradient norm** every step (`torch.nn.utils.clip_grad_norm_` returns the pre-clip norm: it returned 8.46 while the grads afterwards had norm 0.001 with `max_norm=1e-3`). A norm that spikes to 1e5+ a few steps before the NaN is an exploding-gradient run, not a bad batch — lower LR, add warmup, or clip at 1.0.
5. fp16 autocast gotcha: `GradScaler` reports `scaler.get_scale()` dropping toward 0 when every step overflows — that means the model is producing Inf activations before the scaler even gets involved; bf16 (no scaler) often sidesteps this since it has fp32's exponent range (max 3.39e38; fp16 `exp(12.)` is `inf`, `exp(11.)` is 59872).
6. Mixed precision + custom ops: any op not in the autocast allow-list runs in fp32 silently; a hand-written attention or custom CUDA kernel that assumes fp16 input ranges can overflow. Wrap the suspect block in `with torch.autocast("cuda", enabled=False):` to isolate it (the form without `device_type` raises `TypeError: autocast.__init__() missing 1 required positional argument: 'device_type'`).
7. Weight init: a `Linear` or `Embedding` layer left at default init times a huge LR can blow up in step 1 — check loss at step 1 specifically before blaming data.

## 2. CUDA OOM triage order
1. Read the **actual** error — "tried to allocate X, N already allocated by PyTorch, M reserved" tells you whether it's fragmentation (large reserved, small allocated) or genuine growth. All CUDA OOM, allocator and `memory_summary` claims in section 2 need a GPU and were not run (gated: unconfirmed, source is paywalled or blocked).
2. `torch.cuda.memory_summary()` right before the crash shows allocator blocks by size; bursty OOM with growing "reserved but unallocated" across steps is fragmentation — set `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` (or the older `max_split_size_mb`) before you touch batch size.
3. Evaluation OOM that training didn't hit: missing `torch.no_grad()`/`inference_mode()` around eval — activations for an unused backward pass pile up (outputs have `requires_grad=False` under both; without them the output carries a `grad_fn`). This is the single most common "works in training, dies in eval" bug.
4. Growing memory across epochs (not steps): a Python-side leak, usually accumulating tensors with `requires_grad=True` into a list or logging `loss` instead of `loss.item()` — the computation graph (and all its activations) stays alive as long as any tensor pointing into it is referenced.
5. Real capacity shortfall: reduce batch size, use **gradient accumulation** to keep the effective batch, or add **activation checkpointing** (`torch.utils.checkpoint.checkpoint`) on the heaviest blocks — recomputes forward activations during backward instead of storing them, trading extra compute for memory (the "~30%" figure is unmeasured here) (gated: unconfirmed, source is paywalled or blocked). `checkpoint(m, x, use_reentrant=False)` runs on CPU.
6. `torch.profiler.profile(profile_memory=True)` (ran on CPU with `ProfilerActivity.CPU`) with a few steps gives a timeline of allocations by op — use it before guessing which layer is the hog; attention and the final softmax/logits layer over a large vocab are frequent culprits.
7. Multi-process DataLoader workers each hold a CUDA context if they touch the GPU (e.g. GPU-side augmentation) — keep workers CPU-only, move to GPU only in the main process.

## Verify
- [ ] Inputs/labels checked for NaN/Inf before the forward pass on the failing batch.
- [ ] `set_detect_anomaly(True)` run once and removed afterward; the flagged op is understood, not just silenced.
- [ ] Gradient norm logged per step; spikes correlate with the NaN step (or don't — ruling data in or out).
- [ ] `torch.cuda.memory_summary()` or the memory profiler checked before changing batch size blindly.
- [ ] Eval code confirmed wrapped in `no_grad`/`inference_mode`.
- [ ] If accepted as a capacity limit: accumulation steps or checkpointing added and effective batch size unchanged.
