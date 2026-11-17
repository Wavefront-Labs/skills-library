---
id: computing-software.ai-ml-engineering.pytorch.parametrizations-weight-norm-spectral-orthogonal
name: parametrizations-weight-norm-spectral-orthogonal
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, parametrizations, spectral-norm, weight-norm, orthogonal, register-parametrization, gan-stability]
level: practitioner
status: verified
description: "Constrain PyTorch weights with torch.nn.utils.parametrize: weight_norm, spectral_norm, orthogonal and custom parametrizations, caching, removal and state_dict keys."
sources:
  - https://pytorch.org/tutorials/intermediate/parametrizations.html
  - https://pytorch.org/docs/stable/generated/torch.nn.utils.parametrize.register_parametrization.html
  - https://pytorch.org/docs/stable/generated/torch.nn.utils.parametrizations.spectral_norm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Parametrizations (weight_norm / spectral_norm / orthogonal)

A parametrization replaces `module.weight` with a function of an underlying unconstrained tensor, recomputed on access. Use it to enforce constraints during training without projecting after each optimizer step.

## Built-ins (modern API)
```python
from torch.nn.utils import parametrizations as P
conv = P.spectral_norm(nn.Conv2d(64, 128, 3))     # Lipschitz <= ~1; GAN discriminators
lin  = P.weight_norm(nn.Linear(512, 512))         # w = g * v / ||v||
rnn_w = P.orthogonal(nn.Linear(256, 256))         # orthogonal matrix; RNN stability
```
Prefer `torch.nn.utils.parametrizations.*` over the old `torch.nn.utils.weight_norm` / `spectral_norm` hook-based versions, which are the legacy API (`torch.nn.utils.weight_norm` emits a deprecation warning; the `spectral_norm` docs say it will be deprecated). The hook-based `weight_norm` fails `copy.deepcopy` on a non-leaf weight (tested: "Only Tensors created explicitly by the user (graph leaves) support the deepcopy protocol"); the parametrized versions deepcopy fine.

## Custom
```python
import torch.nn.utils.parametrize as parametrize
class Symmetric(nn.Module):
    def forward(self, X): return X.triu() + X.triu(1).transpose(-1, -2)
parametrize.register_parametrization(layer, "weight", Symmetric())
```
- Optional `right_inverse(self, W)` lets you assign `layer.weight = W` and initialise the underlying tensor from it.
- Chain several: register twice; they compose in order.

## Inspect and remove
- `parametrize.is_parametrized(layer, "weight")`
- Underlying tensor: `layer.parametrizations.weight.original` (for weight_norm: `original0` = g, `original1` = v).
- Freeze to a plain weight for inference/export: `parametrize.remove_parametrizations(layer, "weight", leave_parametrized=True)`.

## Cost and caching
Each access to `layer.weight` recomputes the function (spectral_norm runs a power iteration step in training). If one forward accesses the weight many times (weight tying, RNN unroll):
```python
with parametrize.cached():
    out = model(x)
```

## state_dict
Keys change: `layer.weight` becomes `layer.parametrizations.weight.original` (plus `parametrizations.weight.0._u` and `._v` buffers for spectral_norm, `original0`/`original1` for weight_norm, `parametrizations.weight.0.base` for orthogonal). Loading a plain checkpoint into a parametrized model, or the reverse, needs key remapping or loading before registering.

## Gotchas
- spectral_norm in `eval()` uses stored `u`, `v` without updating; make sure the model was trained enough steps for the estimate to converge.
- Optimizer must be created after registering, since the parameters are new objects.
- Orthogonal on non-square matrices gives semi-orthogonal rows or columns depending on shape.
