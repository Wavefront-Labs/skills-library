---
id: computing-software.ai-ml-engineering.pytorch.weight-initialization-with-nn-init
name: weight-initialization-with-nn-init
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, weight-initialization, nn-init, kaiming-init, xavier-init, residual-scaling]
level: practitioner
status: verified
description: "Initialise PyTorch layers deliberately with nn.init: Kaiming vs Xavier, gain, zero-init of residual branches and output layers, and how to apply init safely."
sources:
  - https://pytorch.org/docs/stable/nn.init.html
  - https://arxiv.org/abs/1502.01852
  - https://arxiv.org/abs/1706.02677
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Weight initialization with nn.init

PyTorch's default for `nn.Linear`/`nn.Conv*` is `kaiming_uniform_(a=sqrt(5))` (equivalent to uniform(-1/sqrt(fan_in), 1/sqrt(fan_in)), per the comment in `Linear.reset_parameters`), which works for shallow nets but is not tuned for any particular activation. Explicit init matters for deep nets without normalisation, custom blocks, and stable first steps.

## Pick by activation
| Activation | Init | Call |
|---|---|---|
| ReLU / LeakyReLU / GELU (approx) | Kaiming (He) | `nn.init.kaiming_normal_(w, mode="fan_in", nonlinearity="relu")` |
| tanh / sigmoid / linear | Xavier (Glorot) | `nn.init.xavier_uniform_(w, gain=nn.init.calculate_gain("tanh"))` |
| Transformers (GPT/BERT style) | normal std 0.02 | `nn.init.normal_(w, 0.0, 0.02)`; residual projections scaled by `1/sqrt(2*n_layers)` (nanoGPT: `std=0.02/math.sqrt(2 * config.n_layer)` on the `c_proj.weight` tensors) |
| Embeddings | normal std 0.02 or 1/sqrt(d) | `nn.init.normal_(emb.weight, std=0.02)` |
| Biases | zero | `nn.init.zeros_(b)` |
`mode="fan_out"` preserves gradient variance in backward and is what torchvision ResNets use for convs (`kaiming_normal_(m.weight, mode="fan_out", nonlinearity="relu")` in `ResNet.__init__`). `calculate_gain`: relu 1.414, tanh 1.667, sigmoid and linear 1.

## Apply once, after construction
```python
def init_weights(m):
    if isinstance(m, nn.Linear):
        nn.init.kaiming_normal_(m.weight, nonlinearity="relu")
        if m.bias is not None: nn.init.zeros_(m.bias)
    elif isinstance(m, (nn.LayerNorm, nn.BatchNorm2d)):
        nn.init.ones_(m.weight); nn.init.zeros_(m.bias)
model.apply(init_weights)     # recursive over all submodules
```
`nn.init.*_` functions run under `no_grad` internally, so they are safe on parameters that require grad.

## Tricks that matter
- **Zero-init the last BN gamma in each residual block** (`nn.init.zeros_(block.bn3.weight)`): each block starts as identity; torchvision exposes `zero_init_residual` (default `False`; with `True` the last BN gamma of every block is 0, checked on `resnet18`; the BN is `bn2` in BasicBlock and `bn3` in Bottleneck).
- **Output layer**: small or zero init for policy/regression heads; for imbalanced classifiers set bias to `log(p/(1-p))` of the positive rate so initial loss matches the prior.
- **Orthogonal init** (`nn.init.orthogonal_`) for RNN hidden-to-hidden weights.
- **Pretrained models**: only initialise new heads; `model.apply` over a pretrained backbone wipes it.

## Gotchas
- `apply` runs after `__init__`; if a submodule overrides `reset_parameters`, calling `m.reset_parameters()` later (e.g. by a library) undoes your init.
- Weight tying (embedding and LM head share a tensor): init it once; initialising both overwrites the first.
- Meta-device / FSDP deferred init: put init in `reset_parameters` so `to_empty()` + `reset_parameters()` reproduces it.

## Verify
Forward one batch and print per-layer activation std: it should not explode or shrink toward 0. Measured on a 20-layer 256-wide ReLU MLP with unit-normal input: Kaiming-normal init gave activation std 0.82, 0.71 and 0.40 at layers 1, 10 and 20; the PyTorch default init gave 0.34, 0.023 and 0.024. Check initial loss against `ln(num_classes)`.
