---
id: computing-software.ai-ml-engineering.pytorch.gradscaler-with-clipping-accumulation-and-multiple-optimizers
name: gradscaler-with-clipping-accumulation-and-multiple-optimizers
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, gradscaler-unscale, gradscaler, gradient-clipping, fp16, amp]
level: practitioner
status: verified
description: "Use torch.amp.GradScaler correctly with gradient clipping, accumulation, multiple losses or optimizers, skipped steps and checkpoint resume in fp16 training."
sources:
  - https://pytorch.org/docs/stable/notes/amp_examples.html
  - https://pytorch.org/docs/stable/amp.html#gradient-scaling
  - https://pytorch.org/docs/stable/amp.html#torch.amp.GradScaler
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GradScaler: clipping, accumulation, multiple optimizers

GradScaler multiplies the loss by a scale so fp16 gradients don't underflow, then divides before the optimizer step. Defaults on torch 2.14 (`inspect.signature`): `init_scale=65536.0`, `growth_factor=2.0`, `backoff_factor=0.5`, `growth_interval=2000`. If any grad is inf/NaN, the step is skipped and the scale halves; after `growth_interval` clean steps it doubles (a run with `growth_interval=3` doubled at the third clean update). `torch.amp.GradScaler("cpu")` works on a CPU build, which is how every block here was run.

## Clipping: unscale first
```python
scaler.scale(loss).backward()
scaler.unscale_(opt)                                   # grads now in true units
torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
scaler.step(opt)                                       # won't unscale twice
scaler.update()
```
Clipping without `unscale_` compares scaled grads (x65536) with your threshold: effectively clipping everything. Measured on a toy Linear: the grad norm was 2.54 true and 166536 scaled (ratio 65536), and clipping the scaled grads to 1.0 then stepping moved the weights by 1.53e-6, which is `lr*1.0/65536`. `step` after `unscale_` uses the unscaled grads (checked against `w - lr*g`). Calling `unscale_` twice on one optimizer raises `RuntimeError: unscale_() has already been called on this optimizer since the last update().`

## Accumulation
Scale and backward every micro-batch; call `unscale_`/`step`/`update` only on the boundary step. `update()` once per optimizer step, not per micro-batch.

## Multiple losses / optimizers (GANs, multi-task)
```python
scaler.scale(loss_d).backward(retain_graph=True)
scaler.scale(loss_g).backward()
scaler.unscale_(opt_d); scaler.unscale_(opt_g)   # optional, if clipping
scaler.step(opt_d); scaler.step(opt_g)
scaler.update()                                   # once, after all steps
```
One scaler for all is correct; each `step` checks its own optimizer's grads for infs. Measured: with an inf loss on model b only, `step(opt_a)` updated a, `step(opt_b)` was skipped, and a single `update()` halved the scale to 32768.

## Skipped steps and schedulers
When a step is skipped, `scheduler.step()` still runs and PyTorch warns "Detected call of `lr_scheduler.step()` before `optimizer.step()`" (reproduced with an inf loss on the first iteration). Usually harmless. To be exact:
```python
scale_before = scaler.get_scale()
scaler.step(opt); scaler.update()
if scaler.get_scale() >= scale_before: sched.step()
```

## Checkpointing
Save `scaler.state_dict()` (keys: `scale`, `growth_factor`, `backoff_factor`, `growth_interval`, `_growth_tracker`) with the model and optimizer; a `load_state_dict` round trip restored scale 32768.0. Without it a new scaler restarts at 65536 and skips a burst of steps.

## Diagnose
- Scale keeps dropping to 1 or below: a real overflow in forward (activations > 65504). Find it with forward hooks checking `isfinite`; fix with bf16, fp32 for that op (`autocast(enabled=False)`), or normalisation.
- Many skipped steps at the start is normal (scale searching down from 65536).
- bf16 does not need GradScaler; using one is harmless but pointless.

## Verify
Log `scaler.get_scale()` and count skipped steps (`scale decreased`) per 1000 steps; it should be a handful at most after warmup.
