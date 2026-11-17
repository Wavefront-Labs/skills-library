---
id: computing-software.ai-ml-engineering.pytorch.ema-and-swa-with-averagedmodel
name: ema-and-swa-with-averagedmodel
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, averagedmodel, ema-weights, swa, swalr, update-bn]
level: practitioner
status: verified
description: "Keep EMA or SWA weights in PyTorch with torch.optim.swa_utils.AveragedModel, choose decay, update BatchNorm stats, and evaluate and checkpoint the averaged model."
sources:
  - https://pytorch.org/docs/stable/optim.html#weight-averaging-swa-and-ema
  - https://arxiv.org/abs/1803.05407
  - https://pytorch.org/blog/pytorch-1.6-now-includes-stochastic-weight-averaging/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EMA and SWA with AveragedModel

Averaging weights along the trajectory (SWA paper, arXiv 1803.05407) tends to find flatter minima and generalise better; EMA is widely used for smoother diffusion/GAN samples. The gain varies by task, so measure it.

## EMA (exponential moving average)
```python
from torch.optim.swa_utils import AveragedModel, get_ema_multi_avg_fn
ema = AveragedModel(model, multi_avg_fn=get_ema_multi_avg_fn(0.999), use_buffers=True)
for step, (x, y) in enumerate(loader):
    loss = loss_fn(model(x), y); loss.backward(); opt.step(); opt.zero_grad()
    ema.update_parameters(model)
# evaluate ema.module (the averaged copy)
```
- Decay: 0.999 for ~10k+ steps, 0.9999 for very long runs (diffusion). Effective window ~ 1/(1-decay) steps. Short runs with high decay leave EMA stuck near init; use warmup on decay. timm's `ModelEmaV3` (`use_warmup=True`) computes `decay = 1 - (1 + step / warmup_gamma) ** -warmup_power` (defaults `warmup_gamma=1.0`, `warmup_power=2/3`), clamped to `[min_decay, decay]` (read from timm/utils/model_ema.py on GitHub).
- `use_buffers=True` averages BN running stats too, so no BN recompute is needed for EMA.
- Keep EMA on the same device; for huge models put it on CPU and update every k steps.

## SWA (stochastic weight averaging)
```python
from torch.optim.swa_utils import AveragedModel, SWALR, update_bn
swa = AveragedModel(model)
swa_sched = SWALR(opt, swa_lr=0.05, anneal_epochs=5)
for epoch in range(epochs):
    train_one_epoch(model)
    if epoch >= swa_start:
        swa.update_parameters(model); swa_sched.step()
    else:
        sched.step()
update_bn(train_loader, swa)       # recompute BN stats for the averaged weights
```
SWA averages equally over the later part of training (you choose `swa_start`) with a constant or cyclic LR. BN stats of averaged weights are wrong until `update_bn` runs one pass in train mode. If your loader yields dicts, write a small loop instead of `update_bn`.

## Checkpointing and serving
- Save `ema.state_dict()` (includes `n_averaged`) to resume; save `ema.module.state_dict()` for deployment. Keys of `ema.state_dict()` are prefixed `module.`.
- With DDP, wrap the averaged model around the unwrapped model (`model.module`) or keys get `module.module.` prefixes (tested with DDP on gloo, world size 1: `AveragedModel(ddp)` gave `module.module.weight`, `AveragedModel(ddp.module)` gave `module.weight`).

## Verify
Track validation metrics for both raw and EMA weights each epoch. EMA should be smoother and, late in training, equal or better; if EMA is much worse, the decay is too high for the run length or BN buffers aren't averaged.
