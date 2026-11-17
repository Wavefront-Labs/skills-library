---
id: computing-software.ai-ml-engineering.pytorch.custom-autograd-function
name: custom-autograd-function
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, custom-autograd-function, autograd-function, ctx-save-for-backward, gradcheck, setup-context]
level: practitioner
status: verified
description: "Write a torch.autograd.Function with forward, setup_context and backward, save tensors correctly, handle non-tensor args and verify gradients with gradcheck."
sources:
  - https://pytorch.org/docs/stable/notes/extending.html#extending-torch-autograd
  - https://pytorch.org/docs/stable/autograd.html#function
  - https://pytorch.org/docs/stable/generated/torch.autograd.gradcheck.gradcheck.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom autograd.Function

Use when the backward you want differs from what autograd would derive: a numerically stable gradient, a straight-through estimator, a kernel written outside PyTorch, or memory savings by recomputing.

## Template (PyTorch 2.x style)
```python
class ClampSTE(torch.autograd.Function):
    @staticmethod
    def forward(x, lo, hi):
        return x.clamp(lo, hi)

    @staticmethod
    def setup_context(ctx, inputs, output):
        x, lo, hi = inputs
        ctx.save_for_backward(x)
        ctx.lo, ctx.hi = lo, hi              # non-tensors go on ctx directly

    @staticmethod
    def backward(ctx, grad_out):
        (x,) = ctx.saved_tensors
        mask = (x >= ctx.lo) & (x <= ctx.hi)
        return grad_out * mask, None, None   # one return per forward input

y = ClampSTE.apply(x, -1.0, 1.0)             # never call forward() directly (it runs, but records no graph)
```
The older form `forward(ctx, ...)` with `ctx` as first argument still works; separate `setup_context` is required for `torch.func` transforms (vmap/grad) support.

## Rules
- Return exactly one gradient per input to `forward`; `None` for non-tensor or non-differentiable inputs.
- Save tensors with `ctx.save_for_backward` (inputs or outputs), not `ctx.x = x`. Only `save_for_backward` gets in-place modification checks and avoids reference cycles that leak memory.
- Use `ctx.needs_input_grad[i]` to skip expensive gradient work for inputs that don't need it.
- Outputs that are not differentiable (indices, masks): `ctx.mark_non_differentiable(idx)`.
- If forward modifies an input in place: `ctx.mark_dirty(x)`.
- Backward runs with grad mode off by default; to support double backward, write backward with differentiable PyTorch ops and decorate nothing extra, or use `@once_differentiable` to declare it is not.

## Verify gradients
```python
x = torch.randn(8, 4, dtype=torch.double, requires_grad=True)
torch.autograd.gradcheck(lambda t: MyFn.apply(t), (x,), eps=1e-6, atol=1e-4)
torch.autograd.gradgradcheck(lambda t: MyFn.apply(t), (x,))   # if double backward is supported
```
Use float64; float32 gradcheck fails on rounding alone. Straight-through estimators intentionally fail gradcheck; test them against the hand-derived mask instead. (The `ClampSTE` template above returns the true derivative of `clamp`, so it passes gradcheck in float64; tested. Float32 input gives `Jacobian mismatch`.)

## Gotchas
- Returning a view of an input from forward triggers view+inplace errors later; return `x.clone()` or a fresh tensor.
- Large saved activations: save inputs and recompute in backward to trade compute for memory.
