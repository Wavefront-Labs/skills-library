---
id: computing-software.ai-ml-engineering.pytorch.cpp-cuda-extensions-load-inline
name: cpp-cuda-extensions-load-inline
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, custom-ops, cpp-extension, load-inline, cudaextension, torch-library-macro, cuda-kernels]
level: practitioner
status: docs-checked
description: "Build C++/CUDA extensions for PyTorch: JIT load_inline/load for iteration, setup.py CUDAExtension for packaging, TORCH_LIBRARY registration, arch lists and ABI pitfalls."
sources:
  - https://docs.pytorch.org/tutorials/advanced/cpp_custom_ops.html
  - https://github.com/pytorch/pytorch/blob/main/torch/utils/cpp_extension.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# C++/CUDA extensions (cpp_extension, load_inline)

**Goal:** add a native kernel to PyTorch when Python/Triton is not enough, and ship it reliably.

## Fast iteration: load_inline
```python
from torch.utils.cpp_extension import load_inline
cpp = "torch::Tensor add_one(torch::Tensor x);"
cuda = r"""
__global__ void k(const float* x, float* y, int n){ int i = blockIdx.x*blockDim.x + threadIdx.x; if(i<n) y[i]=x[i]+1.f; }
torch::Tensor add_one(torch::Tensor x){
  TORCH_CHECK(x.is_cuda() && x.dtype()==torch::kFloat32 && x.is_contiguous(), "expected contiguous float32 CUDA tensor");
  auto y = torch::empty_like(x); int n = x.numel();
  k<<<(n+255)/256, 256, 0, at::cuda::getCurrentCUDAStream()>>>(x.data_ptr<float>(), y.data_ptr<float>(), n);
  return y;
}"""
ext = load_inline(name="add_one_ext", cpp_sources=cpp, cuda_sources=cuda, functions=["add_one"],
                  extra_cuda_cflags=["-O3"], verbose=True)
ext.add_one(torch.randn(1024, device="cuda"))
```
`load(name, sources=["op.cpp", "op_kernel.cu"])` does the same for files. Builds go to a `torch_extensions/<name>` directory; set the `TORCH_EXTENSIONS_DIR` environment variable to choose the root.

## Packaging
```python
# setup.py
from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension
setup(name="myops", ext_modules=[CUDAExtension("myops._C", ["csrc/op.cpp", "csrc/op_kernel.cu"])],
      cmdclass={"build_ext": BuildExtension})
```
Register ops with the dispatcher so they work with `torch.compile`/export instead of exposing bare pybind functions:
```cpp
TORCH_LIBRARY(myops, m) { m.def("add_one(Tensor x) -> Tensor"); }
TORCH_LIBRARY_IMPL(myops, CUDA, m) { m.impl("add_one", &add_one); }
```
Then call `torch.ops.myops.add_one(x)` and add a Python fake implementation with `torch.library.register_fake("myops::add_one")`.

## Pitfalls
- `TORCH_CUDA_ARCH_LIST` controls which GPU architectures are compiled (see the cpp_extension docstrings).
- Launch kernels on the current stream (`at::cuda::getCurrentCUDAStream()`) and validate inputs with `TORCH_CHECK`.

## Verify
- [ ] Output matches a PyTorch reference implementation across shapes and dtypes.
- [ ] `torch.library.opcheck` passes for the registered op (the custom ops tutorial covers testing with it).

## Checked
2026-11-01. Confirmed in torch/utils/cpp_extension.py: `load`, `load_inline` (`functions`, `extra_cuda_cflags`), TORCH_EXTENSIONS_DIR, CUDAExtension and BuildExtension, TORCH_CUDA_ARCH_LIST; in the PyTorch custom C++/CUDA ops tutorial: TORCH_LIBRARY, TORCH_LIBRARY_IMPL, `m.def` schema strings, `getCurrentCUDAStream`, TORCH_CHECK, `torch.library.register_fake`, `opcheck`. Removed (not confirmed): cache directory under the home folder, ninja and CUDA-version requirement, wheel ABI claim, error-text quote, C10_CUDA_KERNEL_LAUNCH_CHECK, CI advice.
Method: documentation only; no commands were run.
