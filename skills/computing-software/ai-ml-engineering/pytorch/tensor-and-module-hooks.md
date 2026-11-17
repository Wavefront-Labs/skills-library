---
id: computing-software.ai-ml-engineering.pytorch.tensor-and-module-hooks
name: tensor-and-module-hooks
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, autograd-hooks, forward-hooks, register-hook, register-forward-hook, activation-capture]
level: practitioner
status: verified
description: "Use PyTorch tensor and module hooks to capture activations, inspect or clip gradients and debug NaNs, and remove handles so hooks do not leak memory."
sources:
  - https://pytorch.org/docs/stable/generated/torch.nn.Module.html#torch.nn.Module.register_forward_hook
  - https://pytorch.org/docs/stable/generated/torch.Tensor.register_hook.html
  - https://pytorch.org/docs/stable/notes/autograd.html#backward-hooks-execution
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tensor and module hooks

## Hook types
| Hook | Signature | Typical use |
|---|---|---|
| `tensor.register_hook(fn)` | `fn(grad) -> grad or None` | inspect/modify grad of one tensor |
| `module.register_forward_pre_hook(fn)` | `fn(mod, args) -> new args or None` | input checks, casting |
| `module.register_forward_hook(fn)` | `fn(mod, args, output) -> new output or None` | capture activations, feature extraction |
| `module.register_full_backward_hook(fn)` | `fn(mod, grad_input, grad_output)` | per-module gradient stats |
| `tensor.register_post_accumulate_grad_hook(fn)` | `fn(param)` | optimizer-in-backward, per-param work after `.grad` is set |
All return a handle; call `handle.remove()` when done.

## Capture activations
```python
feats, handles = {}, []
def save(name):
    def hook(mod, args, out):
        feats[name] = out.detach()
    return hook
for name, mod in model.named_modules():
    if isinstance(mod, nn.Conv2d):
        handles.append(mod.register_forward_hook(save(name)))
with torch.no_grad():
    model(x)
for h in handles: h.remove()
```
`detach()` is essential; storing `out` keeps the graph alive and memory grows every call. For a cleaner feature extractor in torchvision use `torchvision.models.feature_extraction.create_feature_extractor`.

## Find where NaNs start
```python
def nan_check(name):
    def hook(mod, args, out):
        o = out if isinstance(out, torch.Tensor) else out[0]
        if not torch.isfinite(o).all():
            raise RuntimeError(f"non-finite output in {name}")
    return hook
for n, m in model.named_modules(): m.register_forward_hook(nan_check(n))
```
This syncs the GPU every module; use for debugging only.

## Gradient hooks
- Per-parameter gradient norm logging: `p.register_hook(lambda g, n=n: log(n, g.norm()))` (bind `n` as a default to avoid the late-binding closure bug where every hook logs the last name).
- Gradient clipping per-tensor or gradient reversal (domain adaptation): return `-lambda * grad`.
- Use `register_full_backward_hook`, not the deprecated `register_backward_hook`, which reports grads of the last op inside the module rather than the module's inputs.
- A full backward hook makes module inputs/outputs go through a BackwardHookFunction; in-place ops on those outputs then error.

## Gotchas
- Hooks are not saved in `state_dict`, so re-register them after loading a checkpoint into a fresh model. `copy.deepcopy` of a module keeps its forward hooks (tested), so a copied model fires the same hooks.
