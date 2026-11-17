---
id: computing-software.computer-graphics-engineering.computer-vision.vision-model-training-losses-and-schedules
name: vision-model-training-losses-and-schedules
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, cv-deep-learning, vision-training, focal-loss, dice-loss, learning-rate-schedule, mixed-precision]
level: practitioner
status: verified
description: "Train vision models reliably: losses (CE, focal, Dice, IoU), optimisers, warm-up + cosine schedules, mixed precision, EMA, gradient clipping and diagnosing loss curves."
sources: ["https://pytorch.org/docs/stable/optim.html", "https://pytorch.org/docs/stable/amp.html", "https://arxiv.org/abs/1708.02002", "https://arxiv.org/abs/1812.01187"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Training vision models (losses, schedulers)

## Losses by task
| Task | Loss |
|---|---|
| Classification | Cross-entropy (+ label smoothing 0.1) |
| Imbalanced / dense detection | Focal loss (gamma 2, alpha 0.25) |
| Segmentation | CE + Dice (Dice handles small foreground) |
| Box regression | GIoU/DIoU/CIoU + L1 |
| Embeddings | ArcFace / supervised contrastive / triplet with hard mining |

## Optimiser and schedule
```python
opt = torch.optim.AdamW(model.parameters(), lr=3e-4, weight_decay=0.05)
sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=3e-4, total_steps=steps, pct_start=0.05)
```
OneCycleLR starts at `max_lr / 25` (`div_factor`), reaches `max_lr` after `pct_start` of the steps and ends near
`initial_lr / 1e4`; its default `anneal_strategy="cos"` makes the warm-up cosine-shaped, not linear (run: 100 steps,
start 5.4e-5, peak 3e-4 at step 3, end 8e-8).
- Linear warm-up (a few hundred to few thousand steps) then cosine decay is a robust default.
- No weight decay on norm parameters (BN gamma/beta, as in Goyal et al.); many recipes exclude biases too.
- SGD + momentum 0.9 with lr 0.1 x batch/256 for CNNs from scratch.
- Scale lr with batch size (linear rule) and re-tune if you change batch by more than 4x.

## Stability and speed
```python
dev = "cuda" if torch.cuda.is_available() else "cpu"
scaler = torch.amp.GradScaler(dev)                  # needed for float16, not for bfloat16
with torch.autocast(dev, dtype=torch.float16):      # use torch.bfloat16 and skip the scaler lines if preferred
    loss = crit(model(x), y)
scaler.scale(loss).backward(); scaler.unscale_(opt)  # unscale before clipping
torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); scaler.step(opt); scaler.update()
```
The float16 path with the scaler ran on CPU (`GradScaler("cpu")` + `autocast("cpu", float16)`) and the bfloat16 path without a
scaler ran too; the CUDA variants were not run here. The PyTorch AMP docs say the optimizer's gradients must be unscaled before
clipping, and that bfloat16 autocast on CPU uses only `torch.autocast`. EMA of weights (`timm.utils.ModelEmaV3`, decay 0.9998) often adds
accuracy for free.

## Reading curves
- Train loss not decreasing: lr too high/low, labels wrong, preprocessing mismatch. Overfit one
  batch first: it must reach near-zero loss.
- Train down, val up early: overfitting -> augmentation, weight decay, more data.
- Spikes: lr too high, bad samples, missing clipping.

## Reproducibility
Seed everything, log config and git hash, save best + last checkpoints with optimiser state.

## Checked
PyTorch 2.14.1 CPU, torchvision 0.29.1, timm 1.0.30.
- Run: `CrossEntropyLoss(label_smoothing=0.1)`, `torchvision.ops.sigmoid_focal_loss` (defaults alpha 0.25, gamma 2), `generalized_box_iou_loss`, `distance_box_iou_loss`/`complete_box_iou_loss` exist, `OneCycleLR` trace and defaults, the GradScaler/autocast loops above, `timm.utils.ModelEmaV3` exists (default decay 0.9999; the skill's 0.9998 is a choice).
- Fetched (arXiv PDFs): RetinaNet paper (gamma = 2 worked best; for gamma = 2, alpha = 0.25 works best), Goyal et al. (linear scaling rule), Bag of Tricks (initial lr 0.1 x b/256, label smoothing, warm-up; no weight decay on BN gamma/beta in Goyal et al.); PyTorch AMP docs.
