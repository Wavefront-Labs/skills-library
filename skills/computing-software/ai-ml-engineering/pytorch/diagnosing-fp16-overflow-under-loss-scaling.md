---
id: computing-software.ai-ml-engineering.pytorch.diagnosing-fp16-overflow-under-loss-scaling
name: diagnosing-fp16-overflow-under-loss-scaling
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, amp, fp16-overflow, gradscaler, loss-scaling, nan, inf]
level: practitioner
status: verified
description: "Diagnose fp16 inf/NaN under AMP: reading GradScaler scale history, skipped steps, activation overflow vs gradient overflow, and fixes from bf16 to fp32 islands."
sources:
  - https://pytorch.org/docs/stable/amp.html#gradient-scaling
  - https://pytorch.org/docs/stable/notes/amp_examples.html
  - https://docs.nvidia.com/deeplearning/performance/mixed-precision-training/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Diagnosing fp16 overflow under loss scaling

**Context:** fp16 max is 65504 and the smallest normal is about 6e-5 (`finfo.max`, `finfo.tiny` = 6.1e-05). GradScaler multiplies the loss by a scale (default 2^16 = 65536.0) so small gradients do not underflow, then skips steps whose gradients contain inf/NaN and halves the scale.

## Read the scaler first
```python
scaler = torch.amp.GradScaler("cuda")   # "cpu" also works on torch 2.14
...
scaler.scale(loss).backward()
scaler.unscale_(opt)                          # needed before clipping or inspecting grads
gn = torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
scaler.step(opt); scaler.update()
log({"scale": scaler.get_scale(), "grad_norm": gn.item()})
```
| Scale behaviour | Meaning |
|---|---|
| Drops a few times early, then climbs every 2000 steps (`growth_interval`) | Normal |
| Keeps halving to below 1 (25 inf steps took it to 0.00195) | Gradients are inf every step: real overflow in forward/backward, not a scaling issue |
| Loss is NaN and the scale also halves each step (3 NaN-loss steps took 65536 to 8192) | A NaN from the forward pass reaches the gradients; the scaler cannot tell it from overflow, so it skips and backs off. Find the NaN with the hook below; do not tune `init_scale` |

Count skipped steps: compare `scaler.get_scale()` before and after `update()`; a decrease means the step was skipped (an inf loss took 65536.0 to 32768.0 in a run) and the LR scheduler should arguably not advance.

## Find where it overflows
- Forward hook that flags non-finite outputs (run on a toy `exp(100*x)` layer: it raised `non-finite output in Big`):
```python
def hook(m, i, o):
    if isinstance(o, torch.Tensor) and not torch.isfinite(o).all():
        raise RuntimeError(f"non-finite output in {m.__class__.__name__}")
for m in model.modules(): m.register_forward_hook(hook)
```
- Also log `o.abs().max()` per layer; values approaching 1e4 in fp16 are a warning (max is 65504, and `exp` overflows early: fp16 `exp(11.)` is 59872 and `exp(12.)` is `inf`).
- Typical culprits: attention logits before softmax, large residual stream norms in deep transformers, unnormalized sums/means over long sequences, `exp`/`pow`, custom losses.

## Fixes
1. **Switch to bf16** where `torch.cuda.is_bf16_supported()` is True: same exponent range as fp32 (max 3.39e38), no scaler needed. This removes range overflow, not precision loss.
2. Run the risky op in fp32: `with torch.autocast("cuda", enabled=False): y = f(x.float())` (the `device_type` argument is required; calling `torch.autocast(enabled=False)` raises `TypeError`).
3. Scale attention correctly (1/sqrt(d)); `F.scaled_dot_product_attention` applies that scale by default (it ran on CPU) and the amp docs list it among autocast ops.
4. Add or move normalization (pre-norm, QK-norm), lower LR, add warmup.
5. Compute losses in fp32: `F.cross_entropy(logits.float(), y)` (on CUDA autocast already does this for `cross_entropy`).
6. Lower `init_scale` (e.g. `GradScaler(init_scale=2**10)`, an accepted argument) if you see many early skips; never disable the scaler for fp16.

## Verify
- [ ] Fewer than about 0.1% of steps skipped after warmup (a rule of thumb, not a measured standard).
- [ ] No non-finite activations with the hook enabled for 1000 steps.
