---
id: computing-software.ai-ml-engineering.pytorch.freezing-layers-and-partial-fine-tuning
name: freezing-layers-and-partial-fine-tuning
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, freeze-layers, requires-grad-false, partial-fine-tuning, transfer-learning, optimizer-param-groups]
level: practitioner
status: verified
description: "Freeze and unfreeze parts of a PyTorch model correctly: requires_grad_(False), BN handling, what the optimizer sees, and verifying frozen weights do not move."
sources:
  - https://pytorch.org/tutorials/beginner/finetuning_torchvision_models_tutorial.html
  - https://pytorch.org/docs/stable/notes/autograd.html#setting-requires-grad
  - https://pytorch.org/docs/stable/optim.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Freezing layers and partial fine-tuning

## Freeze
```python
for p in model.backbone.parameters():
    p.requires_grad_(False)
opt = torch.optim.AdamW((p for p in model.parameters() if p.requires_grad), lr=1e-3)
```
- Frozen params get no `.grad`, saving gradient memory and backward compute for those layers (autograd stops at the earliest layer that needs grad).
- PyTorch optimizers skip parameters whose `.grad` is None, so frozen params are not decayed. Filtering still matters: an optimizer built before freezing keeps state for them, and passing them makes unfreezing later ambiguous. Build the optimizer after freezing.
- `torch.no_grad()` around the backbone forward also works and saves activation memory, but you can't then unfreeze without code changes.

## BatchNorm is not frozen by requires_grad
`requires_grad_(False)` stops gamma/beta updates but `running_mean/var` still update in train mode. To truly freeze, also put BN modules in eval mode after every `model.train()` call (see train-vs-eval skill).

## Unfreezing later (gradual)
```python
for p in model.backbone.layer4.parameters(): p.requires_grad_(True)
opt.add_param_group({"params": model.backbone.layer4.parameters(), "lr": 1e-4})
```
Adding a param group keeps existing optimizer state; recreating the optimizer resets Adam moments for the head too. If an LR scheduler exists, `add_param_group` after the scheduler was built makes `sched.step()` fail (tested: `ValueError: zip() argument 2 is shorter than argument 1` with LambdaLR), so recreate the scheduler.

## Partial fine-tuning choices
- Linear probe: freeze all but the head. Fast, robust to small data, a good baseline.
- Top-k blocks: unfreeze the last few blocks; often most of the gain for half the compute.
- Bias-only (BitFit) or norm-only tuning: tiny parameter counts, surprisingly strong for transformers.
- LoRA/adapters (PEFT) when the model is large and you need many task variants.

## Gotchas
- DDP with frozen params is fine, but params that require grad yet receive none in some steps need `find_unused_parameters=True`.
- `model.eval()` does not freeze anything; it only changes dropout/BN behaviour.
- Freezing embeddings while training a tied LM head also freezes the head (same tensor).

## Verify
```python
before = {n: p.clone() for n, p in model.named_parameters() if not p.requires_grad}
train_one_step()
assert all(torch.equal(before[n], p) for n, p in model.named_parameters() if n in before)
print(sum(p.numel() for p in model.parameters() if p.requires_grad), "trainable")
```
