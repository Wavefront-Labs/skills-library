---
id: computing-software.ai-ml-engineering.llama-cpp.build-cuda-backend
name: build-cuda-backend
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, cuda, nvidia, cmake-cuda-architectures, ggml-cuda]
level: practitioner
status: docs-checked
description: "Build with CUDA: GGML_CUDA, architecture selection, compiler options and tuning build flags."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# CUDA build

Install the NVIDIA CUDA toolkit, then:

```bash
cmake -B build -DGGML_CUDA=ON
cmake --build build --config Release
```

This also builds the CPU backend by default.

Build options from docs/build.md:

- Default target: llama.cpp is built for the GPUs connected at build time. `-DGGML_NATIVE=OFF` builds for all CUDA GPUs (the binary should run on all CUDA GPUs with optimal performance, though some just-in-time compilation may be required); it gives a large binary that takes longer to compile.
- If nvcc cannot detect the GPU you may see `nvcc warning : Cannot find valid GPU for '-arch=native', default arch is used`. Look up your Compute Capability and list it: `-DCMAKE_CUDA_ARCHITECTURES="86;89"` (the page's example for RTX 3080 Ti/3070 at 8.6 and RTX 4090 at 8.9).
- Several CUDA installs: `-DCMAKE_CUDA_COMPILER=/opt/cuda-11.7/bin/nvcc -DCMAKE_INSTALL_RPATH="/opt/cuda-11.7/lib64;\$ORIGIN" -DCMAKE_BUILD_WITH_INSTALL_RPATH=ON` (the page's example for CUDA 11.7). An old CUDA with a new glibc can fail on `cospi`/`sinpi`/`rsqrt` exception specifications; the page's workaround is to patch `crt/math_functions.h` to add `noexcept (true)`.
- `-DGGML_CUDA_CCCL_VERSION=vMAJOR.MINOR.PATCH`: use a specific CCCL instead of the one bundled with the toolkit. CUB DeviceTopK needs CCCL 3.4.3 or newer; older versions use the sort fallback.
- Performance options (all compile-time):
  - `GGML_CUDA_FORCE_MMQ` (default false): force the custom quantized matmul kernels instead of FP16 cuBLAS even without int8 tensor cores (V100, CDNA, RDNA3+). MMQ is on by default for GPUs with int8 tensor cores. Large-batch speed is worse but VRAM use is lower.
  - `GGML_CUDA_FORCE_CUBLAS` (default false): force FP16 cuBLAS instead of the custom kernels. May have numerical overflow issues (not V100, CDNA, RDNA4, which use FP32 compute by default) and uses more memory; prompt processing may be faster on recent datacenter GPUs.
  - `GGML_CUDA_FA_QUANTS`: `all` or a `;`-separated list of `type_K-type_V` pairs for which FlashAttention CUDA kernels are compiled. Default `q4_0-q4_0;q8_0-q8_0;f16-f16;bf16-bf16`; `f16-f16` is always compiled; missing combinations fall back to the f16-f16 kernel with a warning; `all` makes compilation much longer. Legal types: f16, bf16, q4_0, q4_1, q5_0, q5_1, q8_0. `GGML_CUDA_FA_ALL_QUANTS` is a deprecated alias for `GGML_CUDA_FA_QUANTS=all`.
- On Windows on ARM, an all-MSVC CUDA build may have a slower CPU backend; the project's release workflow uses a split build (CPU backend with clang, CUDA backend with MSVC).

Runtime variables are covered in the cuda-runtime-environment skill. Use `-ngl` to offload layers.

## Checked

Date: 2026-11-08. Confirmed against the CUDA section of docs/build.md. Removed because the page does not mention them: `GGML_CUDA_NCCL`, `GGML_CUDA_COMPRESSION_MODE`, `CMAKE_CUDA_HOST_COMPILER`, the claim that `GGML_CUDA_FA_QUANTS=ON` is valid (the page takes `all` or a pair list), and the Docker `-cuda` image tags.

Method: docs-only read of cited pages, 2026-11-08
