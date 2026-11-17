---
id: computing-software.ai-ml-engineering.pytorch.gradient-flow-checks
name: gradient-flow-checks
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, gradient-flow, vanishing-gradients, exploding-gradients, dead-relu, gradient-norm, debugging]
level: practitioner
status: verified
description: "Check gradient flow per layer in PyTorch: log grad norms and update ratios, spot dead and exploding layers, dead ReLUs and frozen parameters, and decide on the fix."
sources:
  - https://pytorch.org/docs/stable/generated/torch.nn.utils.clip_grad_norm_.html
  - https://karpathy.github.io/2019/04/25/recipe/
  - https://cs231n.github.io/neural-networks-3/#ratio
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gradient flow checks

## Per-layer gradient norms
```python
def grad_report(model):
    rows = []
    for n, p in model.named_parameters():
        if p.requires_grad:
            g = p.grad
            rows.append((n, p.norm().item(), None if g is None else g.norm().item()))
    return rows
loss.backward()
for n, w, g in grad_report(model):
    print(f"{n:60s} w={w:9.3e} g={'NONE' if g is None else f'{g:9.3e}'}")
```
Run on the first steps and at intervals; log to TensorBoard/W&B per layer (Weights & Biases `wandb.watch` can log gradient histograms; check its docs for the current arguments).

## What to look for
| Symptom | Likely cause |
|---|---|
| `grad is None` | parameter unused in forward, detached path, `requires_grad=False` by mistake |
| Grad exactly 0 every step | dead ReLUs, masked-out branch, `argmax`/rounding in path |
| Norm shrinks by orders of magnitude toward early layers | vanishing: deep plain nets, sigmoid/tanh saturation, missing residuals/norm |
| Norm grows toward early layers or spikes | exploding: bad init, high LR, RNN without clipping, missing norm |
| One layer's norm much larger than neighbours | that layer dominates updates; check its init or LR group |

## Update-to-weight ratio
```python
for n, p in model.named_parameters():
    if p.grad is not None:
        ratio = (lr * p.grad).norm() / (p.norm() + 1e-12)
```
Around 1e-3 is the cs231n rough heuristic for the update-to-parameter ratio ("somewhere around 1e-3"; lower suggests the LR is too low, higher too high). For Adam, compute the actual update `p_after - p_before` instead of lr x grad.

## Dead units
```python
acts = {}
model.layer3.register_forward_hook(lambda m, i, o: acts.__setitem__("l3", (o > 0).float().mean(0)))
```
A large fraction of units never active across a batch indicates dead ReLUs: lower LR, use LeakyReLU/GELU, check init and bias.

## Global norm and clipping
`total = torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)` returns the pre-clip norm; log it every step. Frequent clipping (norm >> max_norm most steps) hides a problem rather than fixing it. Spikes in the global norm usually precede loss spikes.

## Fixes in order
Check data and loss first, then init (`nn.init.kaiming_normal_` for ReLU nets), normalisation layers, residual connections, LR and warm-up, gradient clipping. Under AMP fp16, unscale before measuring (`scaler.unscale_(opt)`), or norms include the loss scale.
