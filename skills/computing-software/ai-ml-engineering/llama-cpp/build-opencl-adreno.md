---
id: computing-software.ai-ml-engineering.llama-cpp.build-opencl-adreno
name: build-opencl-adreno
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, opencl, adreno, qualcomm, kernel-cache]
level: advanced
status: docs-checked
description: "Enable the OpenCL backend for Qualcomm Adreno GPUs with the embed and Adreno kernel options."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/docs/backend/OPENCL.md", "https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# OpenCL (Adreno)

The OpenCL backend was designed first for Qualcomm Adreno GPUs. Because OpenCL is portable it can also run on certain Intel GPUs without SYCL support, though performance is not optimal. The page lists verified setups: Android (Snapdragon 8 Gen 3, 8 Elite), Windows 11 Arm64 (Snapdragon X Elite) and Ubuntu 22.04 on WSL2 with an Intel 12700H. Verified Adreno GPUs include 750, 810, 830, 840, X1-85 and X2-90. A6x GPUs with a recent driver and compiler work (usually IoT platforms); A6x in phones likely does not, due to outdated drivers.

Build outline: install the OpenCL headers and ICD loader (Khronos repositories) for your target, then configure llama.cpp with `-DGGML_OPENCL=ON`.

- Android: use the NDK toolchain (`-DCMAKE_TOOLCHAIN_FILE=.../android.toolchain.cmake -DANDROID_ABI=arm64-v8a -DANDROID_PLATFORM=android-28 -DBUILD_SHARED_LIBS=OFF -DGGML_OPENCL=ON`, generator Ninja). The Android guide expects Git, CMake 3.29, Ninja and Python3.
- Windows 11 Arm64: Clang must be used, building with Visual Studio's `cl` is not supported; Visual Studio (or Build Tools) is still needed for its libraries. Pass `-DCMAKE_TOOLCHAIN_FILE=.../cmake/arm64-windows-llvm.cmake -DCMAKE_PREFIX_PATH=<opencl install> -DBUILD_SHARED_LIBS=OFF -DGGML_OPENCL=ON`; the page uses PowerShell 7.
- Linux: same as Windows without the toolchain file.

CMake options:

| Option | Default | Meaning |
|---|---|---|
| `GGML_OPENCL_EMBED_KERNELS` | ON | embed OpenCL kernels in the executable |
| `GGML_OPENCL_USE_ADRENO_KERNELS` | ON | use kernels optimised for Adreno |
| `GGML_OPENCL_USE_ADRENO_BIN_KERNELS` | OFF | allow the binary kernel library for Adreno |

Binary kernel library: currently targets Snapdragon X2 GPUs (X2-90, X2-85, X2-45) and holds MUL_MAT_ID kernels for Q4_0, Q4_1, Q4_K and MXFP4. Download it manually from Qualcomm's software center page named in OPENCL.md, configure with `-DGGML_OPENCL_USE_ADRENO_BIN_KERNELS=ON`, and put `adreno-opencl-kernels.dll` next to the executables.

Program binary cache: compiled `cl_program` binaries are cached on disk. `GGML_OPENCL_KERNEL_CACHE_DIR` unset, empty, `1` or `default` uses the platform default directory (for example `%LOCALAPPDATA%\llama.cpp\cl-cache` on Windows); `0`, `off`, `none` or `disable(d)` turns it off; any other value is used as the directory path. `GGML_OPENCL_KERNEL_CACHE_DEBUG=1` prints a HIT/MISS/SAVE trace to stderr.

Supported data types: Q1_0, Q4_0, Q4_1, Q5_0, Q5_1, Q8_0, Q4_K, Q5_K, Q6_K, MXFP4 and IQ4_NL. The page recommends downloading GGUF models directly from Hugging Face. Known issue: flash attention does not always improve performance.

## Checked

Date: 2026-11-08. Confirmed against docs/backend/OPENCL.md and the OpenCL section of docs/build.md. Corrected: the old skill said Q4_0 is the main supported type (the page lists eleven) and recommended embedding as an explicit flag; removed `--device`, `-ngl 99` and the `LD_LIBRARY_PATH` advice, which are not on the page.

Method: docs-only read of cited pages, 2026-11-08
