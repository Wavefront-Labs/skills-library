---
id: computing-software.ai-ml-engineering.pytorch.torch-func-vmap-grad-functional-call
name: torch-func-vmap-grad-functional-call
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, torch-func, vmap, jacrev, functional-call, per-sample-gradients]
level: practitioner
status: verified
description: "Use torch.func (vmap, grad, jacrev, jacfwd, functional_call) for per-sample gradients, Jacobians, Hessians and model ensembling without Python loops."
sources:
  - https://pytorch.org/docs/stable/func.html
  - https://pytorch.org/tutorials/intermediate/per_sample_grads.html
  - https://pytorch.org/tutorials/intermediate/ensembling.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# torch.func: vmap, grad, jacrev, functional_call

`torch.func` (formerly functorch) gives JAX-style composable transforms over PyTorch functions.

## functional_call: run a module with explicit params
```python
from torch.func import functional_call, grad, vmap
params = {k: v.detach() for k, v in model.named_parameters()}
buffers = {k: v.detach() for k, v in model.named_buffers()}
def loss_fn(params, buffers, x, y):
    out = functional_call(model, (params, buffers), (x.unsqueeze(0),))
    return F.cross_entropy(out, y.unsqueeze(0))
```

## Per-sample gradients (DP-SGD, influence, data valuation)
```python
per_sample_grads = vmap(grad(loss_fn), in_dims=(None, None, 0, 0))(params, buffers, xb, yb)
# dict of tensors, each with a leading batch dim
```
Avoids a Python loop of `backward()` calls (measure the speed-up on your model). BatchNorm in train mode mixes samples and is not vmap-able: use `eval()`, GroupNorm, or `torch.func.replace_all_batch_norm_modules_`.

## Jacobians and Hessians
```python
from torch.func import jacrev, jacfwd, hessian
J = jacrev(f)(x)            # reverse mode: cheap when outputs < inputs
J = jacfwd(f)(x)            # forward mode: cheap when inputs < outputs
H = hessian(f)(x)           # = jacfwd(jacrev(f))
Jb = vmap(jacrev(f))(xb)    # batched Jacobians
```
Hessian-vector products without materialising H: `torch.func.jvp(grad(f), (x,), (v,))[1]`.

## Model ensembling
```python
from torch.func import stack_module_state
params, buffers = stack_module_state(models)        # leading dim = n_models
base = copy.deepcopy(models[0]).to("meta")
def run(p, b, x): return functional_call(base, (p, b), (x,))
out = vmap(run, in_dims=(0, 0, None))(params, buffers, x)   # same batch to all models
```

## Gotchas
- Functions must be pure: no in-place writes to captured tensors, no `.item()` or data-dependent Python control flow inside vmap (raises "vmap: It looks like you're calling .item()"). Use `torch.where` instead of `if`.
- Randomness under vmap needs `randomness="different"` or `"same"`; default `"error"` raises on dropout.
- `grad` returns grads only for the first argument by default; use `argnums=(0, 1)` for more, `has_aux=True` to return extra outputs.
- Custom `autograd.Function`s need the `setup_context` style and `generate_vmap_rule = True` or a `vmap` staticmethod to work under transforms.

## Verify
Compare a few per-sample grads against a loop of `torch.autograd.grad` on single examples with `torch.testing.assert_close`.
