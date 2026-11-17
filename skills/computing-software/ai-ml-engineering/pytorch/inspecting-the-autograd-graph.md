---
id: computing-software.ai-ml-engineering.pytorch.inspecting-the-autograd-graph
name: inspecting-the-autograd-graph
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, grad-fn, autograd-graph-inspection, next-functions, torchviz, autograd, requires-grad]
level: practitioner
status: verified
description: "Walk and visualise PyTorch's autograd graph via grad_fn, next_functions and torchviz to find detached branches, unexpected saved tensors and why a parameter gets no grad."
sources:
  - https://pytorch.org/docs/stable/notes/autograd.html
  - https://pytorch.org/docs/stable/autograd.html#torch.Tensor.grad_fn
  - https://github.com/szagoruyko/pytorchviz
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Inspecting the autograd graph

Every tensor produced by a differentiable op on `requires_grad` inputs has `grad_fn` (a backward Node). Leaves (parameters, inputs) have `grad_fn=None` and `is_leaf=True`.

## Walk it
```python
loss = model(x).sum()
print(loss.grad_fn)                       # <SumBackward0>
def walk(fn, depth=0, seen=set()):
    if fn is None or fn in seen: return
    seen.add(fn)
    print("  " * depth + type(fn).__name__)
    for nxt, _ in fn.next_functions:
        walk(nxt, depth + 1, seen)
walk(loss.grad_fn)
```
- `AccumulateGrad` nodes are where gradients land in a leaf; `fn.variable` gives the parameter.
- `next_functions` is a tuple of `(node, input_index)`; `None` entries mean that input did not require grad.
- Saved tensors: attributes prefixed `_saved_` (e.g. `fn._saved_self`, `fn._saved_mat2`) show what the node holds for backward.

## Which parameters are reachable
```python
reached = set()
def collect(fn):
    if fn is None or fn in reached: return
    reached.add(fn)
    for n, _ in fn.next_functions: collect(n)
collect(loss.grad_fn)
leaf_ids = {id(n.variable) for n in reached if hasattr(n, "variable")}
for name, p in model.named_parameters():
    if p.requires_grad and id(p) not in leaf_ids: print("not in graph:", name)
```
This catches the usual causes of "parameter has no gradient": `.detach()`, `.item()`/`.numpy()` round trips, `torch.no_grad()` regions, integer casts, `argmax`, layers defined but unused in `forward`. DDP's `find_unused_parameters` errors point at the same issue.

## Visualise
```python
from torchviz import make_dot            # pip install torchviz graphviz
make_dot(loss, params=dict(model.named_parameters()), show_attrs=True, show_saved=True).render("graph", format="svg")
```
Good for small models or a single block; whole LLM graphs are unreadable. For compiled models, use `TORCH_LOGS=aot_graphs` (the `aot_graphs` log name exists in torch._logging) to print the joint forward/backward graph instead.

## Hooks on nodes
```python
loss.grad_fn.register_hook(lambda grad_inputs, grad_outputs: print([g.norm() if g is not None else None for g in grad_inputs]))
```
Node hooks fire during backward; `register_prehook` fires before computing. Use for debugging only.

## Gotchas
- The graph is freed after `backward()` unless `retain_graph=True`; walking `grad_fn` afterwards still works but saved tensors are gone (`RuntimeError: Trying to backward through the graph a second time`).
- In-place ops bump a version counter; a node whose saved tensor was modified raises at backward. `t._version` shows the counter.
- `torch.inference_mode()` tensors have no graph at all and cannot be used in autograd later.
