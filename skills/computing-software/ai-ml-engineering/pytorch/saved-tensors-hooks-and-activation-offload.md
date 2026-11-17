---
id: computing-software.ai-ml-engineering.pytorch.saved-tensors-hooks-and-activation-offload
name: saved-tensors-hooks-and-activation-offload
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, saved-tensors-hooks, activation-offloading, save-on-cpu, autograd, activation-memory]
level: practitioner
status: verified
description: "Control what autograd saves for backward with torch.autograd.graph.saved_tensors_hooks and save_on_cpu to offload or compress activations and trade memory for transfer time."
sources:
  - https://pytorch.org/docs/stable/autograd.html#hooks-for-saved-tensors
  - https://pytorch.org/tutorials/intermediate/autograd_saved_tensors_hooks_tutorial.html
  - https://pytorch.org/docs/stable/checkpoint.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Saved tensor hooks and activation offload

During forward, autograd keeps tensors each op needs for backward (inputs of matmuls, activation outputs). These "saved tensors" are usually the bulk of activation memory. Saved tensor hooks let you transform them on save and restore them on unpack.

## Offload to CPU (built-in)
```python
from torch.autograd.graph import save_on_cpu
with save_on_cpu(pin_memory=True):
    out = model(x)          # every saved tensor is copied to pinned CPU memory
loss = criterion(out, y)
loss.backward()             # copied back to GPU when backward needs it
```
- `pin_memory=True` uses pinned host memory, which allows asynchronous copies (CUDA only; it ran fine on a CPU-only build).
- Cost: PCIe traffic roughly equal to activation size twice per step. Worth it when activations do not fit and recomputation (checkpointing) is more expensive than transfer, or combined with large batch on small GPU.
- Wrap only the memory-heavy blocks rather than the whole model.

## Custom hooks
```python
def pack(t):   return t.to(torch.float8_e4m3fn) if t.dtype == torch.bfloat16 else t   # compress
def unpack(t): return t.to(torch.bfloat16) if t.dtype == torch.float8_e4m3fn else t
with torch.autograd.graph.saved_tensors_hooks(pack, unpack):
    out = block(x)
```
Use cases: compress (lossy, check accuracy), save to disk for huge models, log what is saved:
```python
def pack(t): print(t.shape, t.dtype, t.device); return t
```
which is the fastest way to see what is eating activation memory.

## Rules
- `pack` must not modify the tensor in place; return a new object. `unpack` must return a tensor with the same size/dtype/device semantics the op expects.
- Hooks apply to tensors saved while the context is active; nesting uses the innermost.
- Parameters are also saved by ops like `linear`; offloading them wastes bandwidth. `pack` receives a plain `Tensor`, not an `nn.Parameter` (tested: `isinstance(t, nn.Parameter)` was False for a saved `Linear` weight), so compare `t.data_ptr()` against the parameters' pointers instead.
- Not compatible with every `torch.compile` setup; compiled regions use their own activation memory planning (see `torch._functorch.config.activation_memory_budget`).

## Checkpointing vs offloading
| | Memory saved | Cost |
|---|---|---|
| `torch.utils.checkpoint` (use_reentrant=False) | activations inside block | ~1 extra forward of that block |
| `save_on_cpu` | all saved tensors in scope | PCIe transfer, can overlap |
| Both | largest | both |

## Verify
Compare `torch.cuda.max_memory_allocated()` and step time for one step with and without the context.
