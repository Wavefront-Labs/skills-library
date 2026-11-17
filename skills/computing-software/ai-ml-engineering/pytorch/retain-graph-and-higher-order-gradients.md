---
id: computing-software.ai-ml-engineering.pytorch.retain-graph-and-higher-order-gradients
name: retain-graph-and-higher-order-gradients
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, autograd, retain-graph, higher-order-gradients, create-graph, autograd-grad, gradient-penalty]
level: practitioner
status: verified
description: "Use retain_graph and create_graph correctly: multiple backward passes, gradient penalties, Hessian-vector products and the memory cost of keeping graphs."
sources:
  - https://pytorch.org/docs/stable/generated/torch.autograd.grad.html
  - https://pytorch.org/docs/stable/notes/autograd.html
  - https://pytorch.org/docs/stable/generated/torch.autograd.functional.hvp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# retain_graph, create_graph and higher-order gradients

**Goal:** differentiate through gradients (WGAN-GP, MAML, Hessian-vector products) or call backward twice without the classic "Trying to backward through the graph a second time" error.

## What the flags do
- `retain_graph=True`: do not free saved tensors after backward, so the same graph can be backpropagated again. Costs memory until the graph goes out of scope.
- `create_graph=True`: record the backward computation itself, so the resulting gradients have `grad_fn` and can be differentiated again. Implies `retain_graph=True`.

## Two losses, one graph
Prefer summing: `(loss_a + loss_b).backward()` is one pass and frees memory. Use `loss_a.backward(retain_graph=True); loss_b.backward()` only when you must inspect gradients between them.

## Gradient penalty (WGAN-GP)
```python
interp = (eps * real + (1 - eps) * fake).requires_grad_(True)
out = critic(interp)
grads, = torch.autograd.grad(out.sum(), interp, create_graph=True)
gp = ((grads.flatten(1).norm(2, dim=1) - 1) ** 2).mean()
(loss_critic + 10 * gp).backward()
```
`torch.autograd.grad` returns gradients without touching `.grad`; `create_graph=True` lets `gp` backprop into critic weights.

## Hessian-vector product
```python
loss = f(params)
g, = torch.autograd.grad(loss, params, create_graph=True)
hv, = torch.autograd.grad(g, params, grad_outputs=v)     # H @ v, no full Hessian
```
Or `torch.autograd.functional.hvp` (there is no `torch.func.hvp`; use `torch.func.jvp(torch.func.grad(f), (x,), (v,))[1]`); for batched or per-sample work use `torch.func` (`jacrev(jacfwd(f))`).

## Gotchas
- **Memory:** a retained graph keeps every activation. Delete references (`del loss`) after the last backward.
- **In-place ops** after the first backward but before the second invalidate saved tensors (version-counter error).
- **Non-differentiable second derivatives:** ReLU has zero second derivative; some custom ops return no double-backward (`RuntimeError: ... does not support double backward`). Use smooth activations (Softplus/GELU) for curvature methods.
- `allow_unused=True` when some inputs do not affect the output, else `RuntimeError: One of the differentiated Tensors appears to not have been used`.

## Verify
- [ ] Compare HVP against finite differences on a tiny model: `(grad(p + h v) - grad(p - h v)) / 2h`.
- [ ] Peak memory with `torch.cuda.max_memory_allocated()` before/after adding the penalty.
