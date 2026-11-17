---
id: computing-software.ai-ml-engineering.model-training.learning-rate-range-test-and-batch-size-scaling
name: learning-rate-range-test-and-batch-size-scaling
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, learning-rate-finder, lr-range-test, batch-size-scaling, linear-scaling-rule, warmup, critical-batch-size]
level: practitioner
status: draft
description: "Find a good learning rate with an LR range test and rescale LR when batch size changes: linear and sqrt rules, warmup, and the critical batch size limit."
sources:
  - https://arxiv.org/abs/1506.01186
  - https://arxiv.org/abs/1706.02677
  - https://arxiv.org/abs/1812.06162
  - https://github.com/davidtvs/pytorch-lr-finder
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LR range test and batch-size scaling

**Goal:** pick a learning rate in one short run instead of a grid, and keep training stable when you change the batch size or GPU count.

## LR range test (Smith, 2015)
1. Start from the initial weights; set LR very small (1e-7).
2. Train for ~100-300 iterations, multiplying LR exponentially each step up to ~1-10.
3. Record smoothed loss per step; stop when loss exceeds ~4x its minimum.
4. Plot loss vs LR (log x-axis). Pick an LR roughly **one order of magnitude below** the loss minimum, or at the steepest descent point.

```python
from torch_lr_finder import LRFinder
finder = LRFinder(model, optimizer, criterion, device="cuda")
finder.range_test(train_loader, start_lr=1e-7, end_lr=10, num_iter=200)
finder.plot(); finder.reset()          # reset restores the initial weights and optimizer state
```
Keras and fastai have equivalents (`lr_find`). The suggested value is a starting point for a short sweep (e.g. 3 values around it), not a final answer; with warmup + cosine schedules the peak LR can usually sit near the suggestion.

## Rescaling LR with batch size
- **Linear scaling rule** (Goyal et al., 2017): multiply LR by `k` when the batch grows by `k` (SGD). Needs **warmup** (e.g. 5 epochs linear from small LR) to avoid early divergence. Held up to batch 8k on ImageNet ResNet-50.
- **Adam/AdamW**: square-root scaling (`lr * sqrt(k)`) is a safer default; verify with a short range test at the new batch size.
- Data-parallel training multiplies the global batch by the number of GPUs: going from 1 to 8 GPUs without adjusting LR is equivalent to an 8x smaller per-example LR.
- Gradient accumulation counts toward the global batch the same way.

## Critical batch size
Beyond a point, larger batches stop reducing the number of steps needed (McCandlish et al., 2018, "gradient noise scale"). Past it, extra GPUs just burn compute. Signs: doubling batch (with tuned LR) no longer halves steps-to-target-loss. The critical batch grows during training and with task difficulty.

## Gotchas
- BatchNorm statistics depend on per-GPU batch, not global; tiny per-GPU batches hurt BN (use SyncBatchNorm or GroupNorm).
- Very large batches can generalise slightly worse at the same epoch count; compensate with longer training or more regularisation.
- Re-run the range test after architecture or optimizer changes; old LRs don't transfer.

## Verify
- [ ] Loss-vs-LR plot saved with the chosen LR marked.
- [ ] After changing global batch size, LR scaled and warmup present; first 1k steps stable.
- [ ] Steps-to-target-loss measured to confirm the larger batch actually helps.
