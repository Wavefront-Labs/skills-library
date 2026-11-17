---
id: computing-software.ai-ml-engineering.pytorch.torch-library-custom-op-and-register-fake
name: torch-library-custom-op-and-register-fake
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, custom-ops, torch-library, custom-op, register-fake, register-autograd, torch-compile]
level: practitioner
status: verified
description: "Wrap opaque code (NumPy, C libraries, external kernels) as PyTorch custom ops with torch.library.custom_op so torch.compile and export work: fake impls, autograd, mutation."
sources:
  - https://pytorch.org/tutorials/advanced/python_custom_ops.html
  - https://pytorch.org/docs/stable/library.html
  - https://pytorch.org/tutorials/advanced/custom_ops_landing_page.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# torch.library.custom_op with register_fake

**Goal:** call code PyTorch can't trace (NumPy, a C library, a hand-written kernel) without graph breaks in `torch.compile` and with correct autograd.

## Define the op
```python
import torch, numpy as np
from torch import Tensor

@torch.library.custom_op("mylib::np_sin", mutates_args=())
def np_sin(x: Tensor) -> Tensor:
    return torch.from_numpy(np.sin(x.detach().cpu().numpy())).to(x.device)

@np_sin.register_fake
def _(x: Tensor) -> Tensor:
    return torch.empty_like(x)          # shapes/dtypes/devices only - no real computation
```
- Name is `"namespace::opname"` (a name without `::` raised `ValueError: not enough values to unpack`); type annotations are required (they define the op schema): a missing one raised `ValueError: infer_schema(func): Parameter x must have a type annotation`.
- `mutates_args` must list every input the op modifies in place (e.g. `mutates_args=("out",)`); lying here is caught by `opcheck`: an op that mutated `x` but declared `mutates_args=()` failed `test_schema` with "Argument x is not defined as mutable but was mutated". Mutating ops return `None`; `mutates_args=("out",)` with `out.copy_(...)` worked as expected.
- The **fake** (meta) implementation lets the compiler and `torch.export` propagate shapes without running the real code. For data-dependent output shapes, use `torch.library.get_ctx().new_dynamic_size()` (run: a `nonzero`-style op exported with an unbacked output size). Without a fake impl, `torch.export.export` and `opcheck` raise `There was no fake impl registered for <CustomOpDef(...)>`.

## Autograd
```python
def setup_context(ctx, inputs, output):
    (x,) = inputs
    ctx.save_for_backward(x)

def backward(ctx, grad):
    (x,) = ctx.saved_tensors
    return grad * torch.cos(x)

np_sin.register_autograd(backward, setup_context=setup_context)
```
Backward should be built from PyTorch ops (or other custom ops) so it is itself traceable.

## Per-device implementations
`@np_sin.register_kernel("cuda")` adds a device-specific implementation while keeping one op (`register_kernel(device_type)` was run with `"cpu"`: the CPU kernel replaced the NumPy one for CPU tensors; the `"cuda"` call has the same form).

## Why not just call the function?
Code the compiler cannot trace needs a custom op: it becomes a single node the compiler treats as a black box with known shapes. Caveat measured on torch 2.14: Dynamo now traces simple NumPy calls itself (`torch._dynamo.explain` reported 0 graph breaks for `np.sin` on a CPU tensor), so NumPy alone no longer forces a graph break, but default (non-strict) `torch.export` of the same module failed with `.numpy() is not supported for tensor subclasses`. The Inductor backend needs a C++ compiler, which the test host lacks (`InvalidCxxCompiler: Compiler: cl is not found`), so compile checks used `backend="aot_eager"`.

## Verify
- [ ] `torch.library.opcheck(np_sin, (torch.randn(3, requires_grad=True),))` passes (it returns a dict `{'test_schema': 'SUCCESS', 'test_autograd_registration': 'SUCCESS', 'test_faketensor': 'SUCCESS', 'test_aot_dispatch_dynamic': 'SUCCESS'}` and raises `OpCheckError` on failure).
- [ ] `torch.compile(fn, fullgraph=True)` around code calling the op compiles without graph breaks (run with `backend="aot_eager"`: OK).
- [ ] Gradients match `torch.autograd.gradcheck` on double-precision inputs.
