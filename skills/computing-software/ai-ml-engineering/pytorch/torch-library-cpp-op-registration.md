---
id: computing-software.ai-ml-engineering.pytorch.torch-library-cpp-op-registration
name: torch-library-cpp-op-registration
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, torch-library-cpp, dispatcher, custom-ops, dispatch-keys, cpp-extension, autograd-kernel]
level: practitioner
status: gated
description: "Register C++/CUDA custom ops with TORCH_LIBRARY and TORCH_LIBRARY_IMPL: schemas, CPU/CUDA/Meta/Autograd dispatch keys, Python fake kernels and testing with opcheck."
sources:
  - https://pytorch.org/tutorials/advanced/cpp_custom_ops.html
  - https://pytorch.org/tutorials/advanced/dispatcher.html
  - https://pytorch.org/docs/stable/library.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# TORCH_LIBRARY C++ op registration and dispatch keys

Ops registered with the dispatcher work with autograd, `torch.compile`, `torch.export`, vmap and AOTInductor. Plain pybind11 functions do not.

## Define the schema and kernels
No C++ compiler or CUDA exists here, so the C++ and CUDA blocks in this skill were not compiled or run (gated: unconfirmed, source is paywalled or blocked). Everything on the Python side (`torch.library.Library`, `register_fake`, `register_autograd`, `opcheck`, schema types) was run on torch 2.14 with the same op schema and a Python CPU kernel `a*b+c`, which exercises the same dispatcher paths.
```cpp
// muladd.cpp
#include <torch/library.h>
at::Tensor muladd_cpu(const at::Tensor& a, const at::Tensor& b, double c) {
  TORCH_CHECK(a.sizes() == b.sizes()); TORCH_CHECK(a.device().is_cpu());
  auto out = torch::empty_like(a);
  // ... loop over a.contiguous() data_ptr<float>() ...
  return out;
}
TORCH_LIBRARY(myops, m) {                          // once per namespace
  m.def("muladd(Tensor a, Tensor b, float c) -> Tensor");
}
TORCH_LIBRARY_IMPL(myops, CPU, m)  { m.impl("muladd", &muladd_cpu); }
TORCH_LIBRARY_IMPL(myops, CUDA, m) { m.impl("muladd", &muladd_cuda); }   // in the .cu file
```
Schema types: `Tensor`, `Tensor?`, `Tensor[]`, `int`, `float` (double in C++), `bool`, `SymInt`, `str` (all seven parsed in `Library.define` on 2.14). Mutation must be declared: `Tensor(a!) out`. Measured: `opcheck` on an op declared `addinto(Tensor(a!) out, Tensor x) -> ()` passed all four tests, while the same kernel declared `addinto(Tensor out, Tensor x) -> ()` failed `test_schema` with `Argument out is not defined as mutable but was mutated`. Silent miscompiles from wrong schemas under `torch.compile` were not reproduced.

## Build and load
```python
# setup.py: CppExtension / CUDAExtension with py_limited_api=True for one wheel per Python ABI (not built here)
torch.ops.load_library("build/.../myops.so")      # or import the extension module
torch.ops.myops.muladd(a, b, 2.0)
```

## Dispatch keys you care about
| Key | Purpose |
|---|---|
| `CPU`, `CUDA`, `MPS` | backend kernels |
| `Meta` / fake | shape-only kernel for compile/export; usually written in Python with `@torch.library.register_fake("myops::muladd")` |
| `Autograd` | backward: either a C++ `torch::autograd::Function` registered at `Autograd`, or Python `torch.library.register_autograd("myops::muladd", backward, setup_context=...)` |
| `CompositeImplicitAutograd` | op written in terms of other ATen ops; autograd and backends come for free |
| `CompositeExplicitAutograd` | one kernel for all backends, autograd registered separately |

The dispatcher picks the highest-priority key present on the inputs: Python modes, Autograd, then backend. An op with only a CPU kernel and no Autograd registration did NOT fail on torch 2.14: the output had `requires_grad=True` and `backward()` ran, with `UserWarning: myops::muladd: an autograd kernel was not registered to the Autograd key(s) but we are trying to backprop through it. This may lead to silently incorrect behavior. This behavior is deprecated and will be removed in a future version of PyTorch` (the fallback mode `torch._C._get_autograd_fallback_mode()` read `warn`, and `"error"` raised `NYI: mode='error'`). In that test the kernel was Python so autograd traced through it; a real C++ kernel would not give correct gradients, so register `Autograd` explicitly.

## Fake kernel (required for compile/export)
Measured: `torch.compile(..., fullgraph=True)` over the op without a fake kernel raised `Unsupported: Operator does not support running with fake tensors`; after `register_fake` it compiled (`aot_eager`), and `torch.export.export` of a module calling the op returned an `ExportedProgram`.
```python
@torch.library.register_fake("myops::muladd")
def _(a, b, c):
    torch._check(a.shape == b.shape)
    return torch.empty_like(a)
```

## Test
```python
torch.library.opcheck(torch.ops.myops.muladd.default, (a, b, 2.0))
```
Checks schema mutation annotations, fake kernel vs real shapes, autograd registration and AOT dispatch: the result dict keys were `test_schema`, `test_autograd_registration`, `test_faketensor` and `test_aot_dispatch_dynamic` (all `SUCCESS` for the mutating op). With `torch.library.register_autograd("myops::muladd", backward, setup_context=...)` registered, `backward` returned grads of the right shape; `opcheck` on the muladd op (first input `requires_grad=True`, second not) still failed `test_aot_dispatch_dynamic` with "element 0 of tensors does not require grad and does not have a grad_fn" (cause not diagnosed), so do not assume `opcheck` passes first time for ops with autograd. Run for CPU and CUDA (CUDA not run), with and without `requires_grad`.

## Gotchas
- Never call `.item()` or allocate host memory in CUDA kernels on the hot path; use `at::cuda::getCurrentCUDAStream()` for launches (C++/CUDA advice, not run) (gated: unconfirmed, source is paywalled or blocked).
- Pure-Python ops (Triton kernels) should use `torch.library.custom_op` instead (`custom_op` exists on 2.14 with signature `custom_op(name, fn=None, /, *, mutates_args, ...)`); C++ registration is for C++/CUDA code.
