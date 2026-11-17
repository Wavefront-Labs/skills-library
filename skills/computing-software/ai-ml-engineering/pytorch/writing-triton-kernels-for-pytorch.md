---
id: computing-software.ai-ml-engineering.pytorch.writing-triton-kernels-for-pytorch
name: writing-triton-kernels-for-pytorch
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, custom-ops, triton-kernel, triton, autotune, triton-op, gpu-kernels]
level: practitioner
status: docs-checked
description: "Write and integrate Triton GPU kernels in PyTorch: program ids, masked loads/stores, block sizes, autotuning, benchmarking with do_bench, and torch.compile-friendly registration."
sources:
  - https://triton-lang.org/main/getting-started/tutorials/01-vector-add.html
  - https://triton-lang.org/main/python-api/triton.html
  - https://pytorch.org/tutorials/recipes/torch_compile_user_defined_triton_kernel_tutorial.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing Triton kernels for PyTorch

**Goal:** a fused GPU kernel in Python that beats a chain of PyTorch ops (fewer memory round-trips), without writing CUDA C++.

## Kernel
```python
import torch, triton, triton.language as tl

@triton.autotune(configs=[triton.Config({"BLOCK": b}, num_warps=w) for b in (256, 1024, 4096) for w in (4, 8)],
                 key=["n"])
@triton.jit
def scaled_gelu_kernel(x_ptr, y_ptr, scale, n, BLOCK: tl.constexpr):
    pid = tl.program_id(axis=0)
    offs = pid * BLOCK + tl.arange(0, BLOCK)
    mask = offs < n                                   # guard the tail block
    x = tl.load(x_ptr + offs, mask=mask, other=0.0).to(tl.float32)
    y = 0.5 * x * (1 + tl.erf(x * 0.7071067811865476)) * scale
    tl.store(y_ptr + offs, y.to(y_ptr.dtype.element_ty), mask=mask)

def scaled_gelu(x: torch.Tensor, scale: float) -> torch.Tensor:
    assert x.is_cuda and x.is_contiguous()
    y = torch.empty_like(x); n = x.numel()
    grid = lambda meta: (triton.cdiv(n, meta["BLOCK"]),)
    scaled_gelu_kernel[grid](x, y, scale, n)
    return y
```
- Each program instance handles one `BLOCK` of elements; `tl.constexpr` values are compile-time constants.
- Masks on loads/stores guard memory operations against out-of-bounds accesses when the input size is not a multiple of `BLOCK` (as in the Triton vector-add tutorial).
- `key` on `triton.autotune` lists the argument names whose change in value triggers re-evaluation of all configs.

## Benchmark and test
```python
ref = torch.nn.functional.gelu(x) * scale
torch.testing.assert_close(scaled_gelu(x, scale), ref, rtol=1e-3, atol=1e-3)
ms = triton.testing.do_bench(lambda: scaled_gelu(x, scale))
```
Compare against eager and against `torch.compile` of the reference; a hand kernel must beat both to be worth maintaining.

## torch.compile integration
The `torch.library.triton_op` docstring says to prefer plain Triton kernels with no `torch.library` wrapper because that is simpler, and to use `triton_op` only when you want an operator that behaves like a built-in one. Unlike `custom_op` (opaque to `torch.compile` and `torch.export`), `triton_op` makes the Triton implementation visible to them. Register with `torch.library.triton_op("mylib::scaled_gelu", mutates_args=())`; every kernel called inside must be launched through `torch.library.wrap_triton(kernel)[grid](...)`. `mutates_args` must be accurate, otherwise behaviour is undefined.

## Verify
- [ ] Matches the PyTorch reference across sizes including non-multiples of BLOCK and different dtypes.
- [ ] Faster than both eager and `torch.compile` reference at production shapes.
- [ ] Autotune key covers the dimensions that change in production.

## Checked
2026-11-01. Confirmed in the Triton vector-add tutorial source (program_id, constexpr, masked load/store, `triton.cdiv` grid lambda, `triton.testing.do_bench`), triton `runtime/autotuner.py` (`key`, `Config` with `num_warps`) and the `torch/_library/triton.py` docstrings for `triton_op` and `wrap_triton`.
Removed: the fp32-accumulation rule, the "corrupts memory silently" wording, the Inductor-generates-Triton remark, the claim that jit kernels can be called directly in compiled functions, the PyTorch 2.6 version gate, and the "autograd" support wording.
Method: documentation only; no commands were run.
