---
id: computing-software.ai-ml-engineering.model-training.discriminative-learning-rates-and-gradual-unfreezing
name: discriminative-learning-rates-and-gradual-unfreezing
category: computing-software
field: ai-ml-engineering
product: model-training
tags: [model-training, discriminative-learning-rates, gradual-unfreezing, layer-wise-lr-decay, transfer-learning, ulmfit]
level: practitioner
status: draft
description: "Fine-tune pretrained networks with discriminative (layer-wise) learning rates and gradual unfreezing, as in ULMFiT and LLRD for transformers, to reduce catastrophic forgetting."
sources:
  - https://arxiv.org/abs/1801.06146
  - https://arxiv.org/abs/1905.05583
  - https://docs.fast.ai/callback.schedule.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Discriminative learning rates and gradual unfreezing

Lower layers hold general features (edges, syntax) and need little change; upper layers and the new head need more. Giving them the same LR either under-trains the head or damages the base.

## Layer-wise LR decay (LLRD) for transformers
```python
def llrd_param_groups(model, base_lr=2e-5, head_lr=1e-3, decay=0.9, wd=0.01):
    layers = [model.base_model.embeddings] + list(model.base_model.encoder.layer)
    groups, n = [], len(layers)
    for i, layer in enumerate(layers):
        lr = base_lr * decay ** (n - 1 - i)                  # top layer gets base_lr, embeddings the least
        groups.append({"params": [p for p in layer.parameters() if p.requires_grad], "lr": lr, "weight_decay": wd})
    groups.append({"params": [p for n_, p in model.named_parameters() if n_.startswith("classifier")], "lr": head_lr})
    return groups
opt = torch.optim.AdamW(llrd_param_groups(model))
```
Typical decay 0.8-0.95 per layer. Known gains of ~0.5-1 point on GLUE-style tasks and more stable fine-tuning on small datasets. Combine with no-decay groups for biases/norms if you split further.

## Discriminative LRs for CNNs (fastai style)
Split into 3 groups (early blocks, late blocks, head) with LRs like `lr/100, lr/10, lr`. In fastai: `learn.fit_one_cycle(5, lr_max=slice(1e-5, 1e-3))`.

## Gradual unfreezing (ULMFiT)
1. Train only the head for an epoch (base frozen).
2. Unfreeze the top block, train an epoch.
3. Unfreeze the next block, and so on, until all layers train.
```python
groups = [model.head, model.block4, model.block3, model.block2, model.block1]
for p in model.parameters(): p.requires_grad_(False)
for stage, g in enumerate(groups):
    for p in g.parameters(): p.requires_grad_(True)
    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=lrs[stage])
    train(model, opt, epochs=1)
```
Rebuilding the optimizer per stage resets Adam state; alternatively add param groups with `opt.add_param_group`.

## When to use
- Small labelled datasets, large pretrained models, unstable fine-tuning (seed-dependent collapse).
- Domain shift where you want to keep general features.
- Less useful with huge datasets (full fine-tuning at one LR works) or PEFT methods (base already frozen).

## Gotchas
- Schedulers multiply each group's LR; warmup still applies to all groups.
- Checkpoints must store the optimizer with the same groups to resume.
- Combining LLRD with very low base LR can leave lower layers effectively frozen; that may be fine (check).

## Verify
Compare against uniform-LR fine-tuning across 3-5 seeds: LLRD should give equal or better mean and lower variance. Log per-group LRs at a few steps to confirm the schedule.
