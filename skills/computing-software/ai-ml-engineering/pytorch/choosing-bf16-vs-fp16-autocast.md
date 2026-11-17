---
id: computing-software.ai-ml-engineering.pytorch.choosing-bf16-vs-fp16-autocast
name: choosing-bf16-vs-fp16-autocast
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, bf16-vs-fp16, autocast, mixed-precision, bfloat16, float16]
level: practitioner
status: verified
description: "Choose bf16 or fp16 for PyTorch autocast by hardware, model and numerical range, and know which choice needs a GradScaler and why bf16 can still underperform."
sources:
  - https://pytorch.org/docs/stable/amp.html
  - https://pytorch.org/docs/stable/notes/amp_examples.html
  - https://cloud.google.com/tpu/docs/bfloat16
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# bf16 vs fp16 autocast

| | fp16 | bf16 |
|---|---|---|
| Exponent / mantissa bits | 5 / 10 | 8 / 7 (`torch.finfo(...).eps` is 2^-10 and 2^-7) |
| Max value | 65504 | ~3.4e38 (same as fp32) |
| Precision (`finfo.eps`) | 9.8e-4 (~3 digits) | 7.8e-3 (~2 digits) |
| Needs loss scaling | yes (GradScaler) | no |
| Hardware | Ask the runtime: `torch.cuda.is_bf16_supported()` (False on a CPU-only build) | same |

## Decision
1. `torch.cuda.is_bf16_supported()` is True: use **bf16**. No overflow, no scaler, fewer failure modes. This is what most LLM training uses.
2. It returns False: use **fp16 + GradScaler** (or fp32).
3. Inference only: fp16 is often fine and gives slightly better accuracy than bf16 when activations stay in range; check for overflow (inf) in attention logits and large residual streams.
4. Models trained in bf16 can hold activations above 65504, which become `inf` in fp16 (`torch.tensor(70000.).half()` gives `inf`, `.bfloat16()` gives 70144). Run them in bf16 or fp32.

## Usage
```python
dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
scaler = torch.amp.GradScaler("cuda", enabled=(dtype == torch.float16))
with torch.autocast("cuda", dtype=dtype):
    loss = loss_fn(model(x), y)
scaler.scale(loss).backward(); scaler.step(opt); scaler.update()
```
Writing the loop this way lets the same code run on both (run with `"cpu"` as the device string on torch 2.14: the scaler is enabled only for fp16, scale stays 65536.0 after one step, and `loss.dtype` is float32 under both dtypes). Keep model weights and optimizer state in fp32; autocast casts per op.

## Where bf16 can still hurt
- 7-bit mantissa: small updates to large weights round away. Measured: bf16 `1.0 + 1e-3` is `1.0`, and one pure-bf16 `SGD(lr=1e-3)` step on a weight of 1.0 with gradient 1.0 leaves it at exactly 1.0 (fp16 gives 1.0010 for the sum). Keep master weights fp32 (autocast does); pure bf16 training (`model.to(torch.bfloat16)`) loses small updates.
- Losses and softmax: on CUDA, autocast runs `softmax`, `log_softmax`, `cross_entropy` and `sum` in fp32 (CUDA fp32 op list in the amp docs). On CPU (`device_type="cpu"`, torch 2.14) `cross_entropy` returned fp32 but `softmax`, `log_softmax` and `sum` stayed bf16, so cast to fp32 yourself there. Custom reductions (`sum` over long sequences) should be cast to fp32.
- Metrics computed on bf16 logits (e.g. AUC with many ties) lose resolution; cast to float first.

## fp16-specific failure modes
- Overflow: inf/NaN loss; GradScaler skips the step and lowers the scale. Repeated skips (scale collapsing toward 1) mean real overflow in forward, not gradients: find the layer with hooks.
- Underflow of small gradients without scaling: `torch.tensor(1e-8).half()` is `0.` (bf16 keeps 1.0e-8), so tiny gradients vanish and training stalls silently.

## Verify
Train 1-2k steps in fp32 and in your chosen dtype; loss curves should overlap within noise. Log `scaler.get_scale()` for fp16: it should stabilise, not keep halving.
