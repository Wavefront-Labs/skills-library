---
id: computing-software.ai-ml-engineering.pytorch.train-vs-eval-mode-dropout-batchnorm
name: train-vs-eval-mode-dropout-batchnorm
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, train-eval-mode, batchnorm-eval, dropout, running-stats, model-eval]
level: practitioner
status: verified
description: "Know exactly what model.train() and model.eval() change in PyTorch: dropout, BatchNorm running stats, momentum, small batches and frozen BN fine-tuning."
sources:
  - https://pytorch.org/docs/stable/generated/torch.nn.Module.html#torch.nn.Module.eval
  - https://pytorch.org/docs/stable/generated/torch.nn.BatchNorm2d.html
  - https://pytorch.org/docs/stable/generated/torch.nn.Dropout.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# train() vs eval(): dropout and BatchNorm

`model.train()` / `model.eval()` set `self.training` recursively. Only modules that read that flag change behaviour; gradients are unaffected.

## What changes
| Module | train() | eval() |
|---|---|---|
| `Dropout` | zero with prob p, scale survivors by 1/(1-p) | identity |
| `BatchNorm*` | normalise with batch stats; update `running_mean/var` | normalise with running stats; no update |
| `InstanceNorm` (track_running_stats=True) | like BN | like BN |
| `LayerNorm`, `GroupNorm` | same in both | same in both |
| Custom modules | whatever checks `self.training` | |

## Classic bugs
- **Forgot eval() for validation**: metrics noisy and worse; BN running stats get polluted by validation data. Always `model.eval()` + `torch.no_grad()` for eval, then `model.train()` before the next train step.
- **Forgot train() after eval**: dropout off and BN frozen for the rest of training. Put `model.train()` at the top of each epoch.
- **Train/eval gap with BN**: running stats lag the weights (momentum 0.1). If eval loss is much worse than train loss with identical data, recompute stats: run a few hundred train batches in train mode under `no_grad` (or `torch.optim.swa_utils.update_bn(loader, model)`).
- **Batch size 1 in train mode**: `ValueError: Expected more than 1 value per channel when training`. Use GroupNorm/LayerNorm, larger batches, or freeze BN.
- **Tiny per-GPU batches under DDP**: per-GPU batch stats are noisy; convert with `nn.SyncBatchNorm.convert_sync_batchnorm(model)`.

## Fine-tuning with frozen BN
Detection/segmentation fine-tunes often use batch 2-8 per GPU, too small for BN stats:
```python
def freeze_bn(m):
    if isinstance(m, nn.modules.batchnorm._BatchNorm):
        m.eval()
        for p in m.parameters(): p.requires_grad_(False)
model.train(); model.apply(freeze_bn)      # must re-apply after every model.train()
```
Because `model.train()` flips BN back, override `train()` in your module or re-call `freeze_bn` each epoch.

## Monte Carlo dropout
For uncertainty, keep dropout on at inference while BN stays in eval:
```python
model.eval()
for m in model.modules():
    if isinstance(m, nn.Dropout): m.train()
```

## Verify
`assert not model.training` inside the eval function; `all(not m.training for m in model.modules())` after eval(); compare two eval forward passes on the same input: they must be identical.
