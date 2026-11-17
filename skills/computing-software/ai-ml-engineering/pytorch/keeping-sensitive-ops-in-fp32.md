---
id: computing-software.ai-ml-engineering.pytorch.keeping-sensitive-ops-in-fp32
name: keeping-sensitive-ops-in-fp32
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, fp32-accumulation, mixed-precision, numerical-stability, softmax-precision, autocast, bf16]
level: practitioner
status: verified
description: "Keep numerically sensitive ops in fp32 under mixed precision: softmax, norms, loss reductions, attention logits, optimizer state and running statistics, and how to force it."
sources:
  - https://pytorch.org/docs/stable/amp.html#autocast-op-reference
  - https://pytorch.org/docs/stable/notes/numerical_accuracy.html
  - https://docs.nvidia.com/deeplearning/performance/mixed-precision-training/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Keeping sensitive ops in fp32

Low precision is generally acceptable for matmul inputs (accumulation precision is hardware and library specific; see the vendor documentation). Trouble comes from ops that **reduce** many values or exponentiate: rounding errors accumulate, small values vanish, large values overflow (fp16 `torch.tensor(70000.)` is `inf`).

## What autocast already does
CUDA autocast runs these in fp32 automatically (all confirmed in the AMP docs' "CUDA Ops that can autocast to float32" list): `softmax`, `log_softmax`, `layer_norm`, `group_norm`, `norm`, `exp`, `log`, `pow`, `sum`, `prod`, `cumsum`, `mse_loss`, `cross_entropy`, `nll_loss`, `binary_cross_entropy_with_logits`, `cosine_similarity`. The CPU autocast list is much shorter and does not include most of these (on torch 2.14 CPU, `softmax`, `sum` and `exp` of bf16 stayed bf16), so keep them in fp32 yourself on CPU. Verify the list covers your code paths.

## Where you must do it yourself
- **Manual reductions**: `x.sum()`, `x.mean()` on bf16 tensors created outside autocast or in custom code. Use `x.float().sum()` or `torch.sum(x, dtype=torch.float32)`.
- **Hand-written attention**: `scores = q @ k.transpose(-1, -2) / sqrt(d)` then `scores.float().softmax(-1).to(v.dtype)` (ran: result stays bf16).
- **Custom norms** (RMSNorm written by hand): compute variance in fp32: `x32 = x.float(); x32 * torch.rsqrt(x32.pow(2).mean(-1, keepdim=True) + eps)` then cast back.
- **Loss computed after leaving autocast** on bf16 logits: `F.cross_entropy(logits.float(), y)`. For big vocabularies, chunk to avoid a full fp32 logits copy.
- **Metrics / running statistics** (EMA, accuracy counters, BN running mean): keep buffers fp32.
- **Positional encodings / rotary**: compute frequencies in fp32; bf16 represents integers exactly only up to 256 (checked: 257 rounds to 256, 301 to 300), so bf16 position indices lose resolution beyond that.

## Forcing a region to fp32
```python
with torch.autocast("cuda", dtype=torch.bfloat16):
    h = backbone(x)
    with torch.autocast("cuda", enabled=False):
        out = sensitive_head(h.float())     # inputs must be cast explicitly
```

## Weights and optimizer
- Master weights and optimizer moments stay fp32 under AMP (params are fp32, only activations are cast). If you `model.to(torch.bfloat16)` for pure-bf16 training, use an optimizer with fp32 state or stochastic rounding, or small updates get rounded away (lr * grad below bf16 resolution of the weight; checked: `1.0 - 1e-3` is still exactly `1.0` in bf16, `0.999` in fp32).
- FSDP2 `torch.distributed.fsdp.MixedPrecisionPolicy(param_dtype=bf16, reduce_dtype=torch.float32)` keeps gradient reduction in fp32 (the class and both argument names exist in torch 2.14; no multi-GPU run was possible).

## Diagnose
- Loss plateaus higher than fp32 run, or NaN only under AMP: compare per-layer outputs with fp32 using forward hooks, find the first layer with large relative error.
- `torch.backends.cuda.matmul.allow_bf16_reduced_precision_reduction = False` rules out reduced-precision reductions in bf16 matmuls (the flag exists and defaults to `True` in 2.14; the effect needs a GPU to see).
