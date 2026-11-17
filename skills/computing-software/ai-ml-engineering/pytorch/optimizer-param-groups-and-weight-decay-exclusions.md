---
id: computing-software.ai-ml-engineering.pytorch.optimizer-param-groups-and-weight-decay-exclusions
name: optimizer-param-groups-and-weight-decay-exclusions
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, param-groups, adamw-weight-decay, weight-decay, layernorm-no-decay, optimizer]
level: practitioner
status: verified
description: "Build PyTorch optimizer parameter groups to exclude biases, norms and embeddings from weight decay and to give heads different learning rates."
sources:
  - https://pytorch.org/docs/stable/optim.html#per-parameter-options
  - https://pytorch.org/docs/stable/generated/torch.optim.AdamW.html
  - https://arxiv.org/abs/1711.05101
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parameter groups and weight-decay exclusions

AdamW applies decoupled weight decay to every parameter in a group. Decaying LayerNorm/BatchNorm scales and biases pulls them toward zero for no benefit and can hurt accuracy, so common recipes exclude them (nanoGPT's `configure_optimizers` decays only parameters with `dim() >= 2`, verified in its model.py).

## Standard split
```python
decay, no_decay = [], []
for n, p in model.named_parameters():
    if not p.requires_grad: continue
    if p.ndim < 2 or n.endswith(".bias") or "norm" in n.lower() or "embed" in n.lower():
        no_decay.append(p)
    else:
        decay.append(p)
opt = torch.optim.AdamW([
    {"params": decay, "weight_decay": 0.1},
    {"params": no_decay, "weight_decay": 0.0},
], lr=3e-4, betas=(0.9, 0.95), fused=True)
```
`p.ndim < 2` catches biases, norm weights and scalar gains in one rule. Whether to decay embeddings varies by recipe; nanoGPT decays them (2D), many BERT recipes don't.

## Different learning rates per group
```python
opt = torch.optim.AdamW([
    {"params": model.backbone.parameters(), "lr": 1e-5},
    {"params": model.head.parameters(), "lr": 1e-3},
], weight_decay=0.01)
```
Group dicts override the defaults passed after the list. Schedulers scale each group's `lr` by the same factor, preserving ratios.

## AdamW vs Adam(weight_decay)
`Adam(weight_decay=x)` adds L2 to the gradient, which interacts with the adaptive scaling and is weaker for large-gradient params. `AdamW` decays weights directly. Use AdamW; typical decay 0.01-0.1. SGD with momentum: L2 and decoupled decay are equivalent up to LR scaling; typical 1e-4 to 5e-4.

## Gotchas
- A parameter appearing in two groups raises `ValueError: some parameters appear in more than one parameter group`. Shared/tied weights show up twice in `named_parameters()` only once, but listing modules separately can duplicate them: dedupe by `id(p)`.
- Building groups from `model.named_parameters()` before wrapping in DDP/FSDP is fine for DDP; FSDP1 exposes flattened `FlatParameter`s unless `use_orig_params=True` (its docstring: original parameters enable per-original-parameter hyperparameters), so use that flag. FSDP2 `fully_shard` keeps the original names with `DTensor` parameters (tested on gloo, world size 1).
- Loading an optimizer state dict requires the same group structure and order.
- `fused=True` (CUDA) or `foreach=True` speeds up the step. In the installed source (`_default_to_fused_or_foreach`), `foreach` is chosen by default when all params are on a supported device, but `fused` is never chosen by default: you must pass `fused=True`.

## Verify
```python
for i, g in enumerate(opt.param_groups):
    print(i, g["lr"], g["weight_decay"], sum(p.numel() for p in g["params"]))
```
and check the param total matches the trainable count.
