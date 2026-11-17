---
id: computing-software.ai-ml-engineering.pytorch.lazy-modules-and-shape-inference
name: lazy-modules-and-shape-inference
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, lazy-modules, lazylinear, shape-inference, uninitialized-parameter, dry-run]
level: practitioner
status: verified
description: "Use PyTorch lazy modules (LazyLinear, LazyConv2d) to infer in_features from the first batch, with the dry-run, optimizer, init and checkpoint ordering they require."
sources:
  - https://pytorch.org/docs/stable/generated/torch.nn.modules.lazy.LazyModuleMixin.html
  - https://pytorch.org/docs/stable/generated/torch.nn.LazyLinear.html
  - https://pytorch.org/docs/stable/generated/torch.nn.parameter.UninitializedParameter.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Lazy modules and shape inference

`nn.LazyLinear(out_features)`, `nn.LazyConv2d(out_channels, k)`, `nn.LazyBatchNorm2d()` etc. create `UninitializedParameter`s and fill in the input dimension on the first forward. Useful when the flattened size after a conv stack is tedious to compute.

```python
model = nn.Sequential(
    nn.LazyConv2d(32, 3), nn.ReLU(), nn.MaxPool2d(2),
    nn.Flatten(), nn.LazyLinear(10))
model(torch.zeros(1, 3, 64, 64))      # dry run materialises every lazy param
print(model)                           # now shows Conv2d(3, 32, ...) / Linear(30752, 10)
```

## Ordering rules
1. **Dry run before creating the optimizer.** The `LazyModuleMixin` docs attach the optimizer after the dry run. (In the tested build an optimizer created first still stepped, because the parameter object is materialised in place, but do not rely on it.) Uninitialized parameters raise on `numel()` so parameter counting fails before the dry run.
2. Apply `.to(device)` / dtype changes after construction and before the dry run (the docs say transforms "can and should" come before dry runs); the dry-run input must have the dtype and device you train with.
3. Dry run before custom init (`model.apply(init_fn)`), DDP/FSDP wrapping, `torch.compile`, and before counting params.
4. Loading a checkpoint into an unmaterialised lazy model is allowed: `load_state_dict` infers shapes from the saved tensors (tested: weights materialised with the right shape and keys matched). The module class stays `LazyLinear` until a forward pass. Lazy modules are initialised after regular ones, so random init order differs from the non-lazy model (see the mixin docstring).

## Detect leftovers
```python
from torch.nn.parameter import UninitializedParameter
assert not any(isinstance(p, UninitializedParameter) for p in model.parameters())
from torch.nn.modules.lazy import LazyModuleMixin
assert not any(isinstance(m, LazyModuleMixin) and m.has_uninitialized_params() for m in model.modules())
```
After the dry run each lazy module converts itself to its regular class (`cls_to_become`).

## When not to use
- Published models / libraries: explicit shapes make the architecture readable and checkpoints self-describing.
- Variable input sizes where the inferred dimension depends on input size: the first batch fixes it and later shapes error (tested: `mat1 and mat2 shapes cannot be multiplied (1x7200 and 30752x10)`).
- DDP/FSDP: run the dry run before wrapping, with identically shaped input on every rank, so parameter shapes agree.

## Alternative without lazy modules
Compute the size once:
```python
with torch.no_grad():
    n = features(torch.zeros(1, 3, 64, 64)).flatten(1).shape[1]
head = nn.Linear(n, 10)
```
