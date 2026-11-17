---
id: computing-software.ai-ml-engineering.pytorch.lr-warmup-cosine-and-onecycle-schedules
name: lr-warmup-cosine-and-onecycle-schedules
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, warmup-cosine, onecyclelr, lr-scheduler, sequentiallr, learning-rate-schedule]
level: practitioner
status: verified
description: "Implement linear warmup plus cosine decay or OneCycleLR in PyTorch, step schedulers at the right granularity, and resume them correctly from checkpoints."
sources:
  - https://pytorch.org/docs/stable/optim.html#how-to-adjust-learning-rate
  - https://pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.OneCycleLR.html
  - https://pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.SequentialLR.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Warmup + cosine and OneCycle schedules

## Why warmup
Adam's second-moment estimates are noisy in the first steps and large models diverge at full LR. Linear warmup over 1-5% of steps (often 500-2000 steps for transformers) stabilises early training.

## Warmup + cosine with LambdaLR (most portable)
```python
import math
total = epochs * len(train_loader) // grad_accum
warm = int(0.03 * total)
min_ratio = 0.1
def lr_lambda(step):
    if step < warm:
        return (step + 1) / warm
    p = (step - warm) / max(1, total - warm)
    return min_ratio + (1 - min_ratio) * 0.5 * (1 + math.cos(math.pi * p))
sched = torch.optim.lr_scheduler.LambdaLR(opt, lr_lambda)
```
Built-in composition: `SequentialLR(opt, [LinearLR(opt, start_factor=1e-3, total_iters=warm), CosineAnnealingLR(opt, T_max=total - warm, eta_min=min_lr)], milestones=[warm])`. HF equivalent: `transformers.get_cosine_schedule_with_warmup(optimizer, num_warmup_steps, num_training_steps, num_cycles=0.5)`, which decays to 0 (use `get_cosine_with_min_lr_schedule_with_warmup` for a floor).

## OneCycleLR
```python
sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=1e-3, total_steps=total, pct_start=0.3,
                                            anneal_strategy="cos", div_factor=25, final_div_factor=1e4)
```
Ramps LR up then down, and inversely cycles momentum (`cycle_momentum=True`; for Adam it cycles beta1). Pick `max_lr` from an LR range test. Very effective for fixed-budget CNN training.

## Step at the right granularity
- Per-step schedules (warmup, cosine in steps, OneCycle): call `sched.step()` after every `opt.step()`. With gradient accumulation, step once per optimizer step, not per micro-batch.
- Per-epoch schedules (StepLR, CosineAnnealingLR with T_max=epochs): call once per epoch.
- `ReduceLROnPlateau.step(val_metric)` takes the metric.
- Call order: `opt.step()` then `sched.step()`. The reverse triggers a warning and skips the first LR value.
- OneCycleLR raises `Tried to step X times. The specified number of total steps is Y` if you step past total; compute total from the real loader length after `drop_last` and accumulation.

## Resume
Save and load `sched.state_dict()` with the optimizer. Rebuilding a LambdaLR and stepping it N times also works but is easy to get wrong. When changing total steps mid-run (extending training), the cosine phase jumps; prefer a fresh schedule from the current LR.

## Verify
Dry-run the schedule without training and plot it:
```python
lrs = []
for _ in range(total): lrs.append(sched.get_last_lr()[0]); opt.step(); sched.step()
```
(use a throwaway optimizer). Check warmup length, peak and final LR.
