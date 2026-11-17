---
id: computing-software.ai-ml-engineering.pytorch.building-extension-wheels-cuda-arch-list
name: building-extension-wheels-cuda-arch-list
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, torch-cuda-arch-list, cpp-extension, wheel-building, abi-compatibility, cuda-toolkit]
level: practitioner
status: docs-checked
description: "Build distributable PyTorch C++/CUDA extension wheels: TORCH_CUDA_ARCH_LIST, +PTX, ninja, MAX_JOBS and the py_limited_api option of torch.utils.cpp_extension."
sources:
  - https://github.com/pytorch/pytorch/blob/main/torch/utils/cpp_extension.py
  - https://docs.pytorch.org/tutorials/advanced/cpp_custom_ops.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Building extension wheels (TORCH_CUDA_ARCH_LIST and ABI)

**Goal:** a wheel for your custom CUDA op that installs and runs on the GPUs and PyTorch versions your users have.

## setup.py
```python
from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension
setup(
    name="my_ops",
    ext_modules=[CUDAExtension("my_ops._C", ["csrc/ops.cpp", "csrc/kernel.cu"])],
    cmdclass={"build_ext": BuildExtension},
)
```
Build against the installed torch (no build isolation) so the compile sees the same headers your users will run.

## GPU architectures
- `TORCH_CUDA_ARCH_LIST` lists the compute capabilities to build for, for example `"8.0 8.6"` or `"8.0 8.6+PTX"`.
- `+PTX` embeds PTX for that capability so the kernels can runtime-compile for any GPU with a capability at or above it. Forward compatibility is the gain; PyTorch's own docs say PTX compiled for newer GPUs can modestly reduce performance, so list exact capabilities when you know them.
- Unset, the build targets the GPUs visible at build time (plus PTX), so a CI machine without the right GPU gives the wrong set. Set the variable explicitly on CI.
- Each extra architecture builds a separate kernel image, so builds get slower and binaries bigger.

## Version and ABI matching
- The extension links against libtorch; build against the torch version (and CUDA build) your users will install, and pin or matrix on it.
- For longer-lived binaries, `py_limited_api=True` on the extension builds against the Python limited API. PyTorch's docs warn that libtorch_python cannot be built with it: use only libtorch APIs (ATen, dispatcher) and expose ops to Python by registering them through the dispatcher (see the custom ops tutorial).

## Build speed
- `BuildExtension` uses ninja by default (`use_ninja=True`); set the `MAX_JOBS` environment variable to control the number of parallel workers.

## Verify
- [ ] Fresh venv with the intended torch version: import the wheel and run the op on each target GPU type.

## Checked
2026-11-01. Confirmed in the torch/utils/cpp_extension.py source (docstrings of BuildExtension, CUDAExtension, CppExtension and _get_cuda_arch_flags): TORCH_CUDA_ARCH_LIST usage, +PTX behaviour, default to visible GPUs, more architectures means slower builds, ninja default and MAX_JOBS, py_limited_api warning. Removed (not confirmed in fetched sources): compute-capability-to-GPU-model table, nvcc flags, ABI flag claims, pip/build flags, auditwheel and cuobjdump steps, ccache, manylinux advice.
Method: documentation only; no commands were run.
