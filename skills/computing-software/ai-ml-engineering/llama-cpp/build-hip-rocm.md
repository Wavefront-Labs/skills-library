---
id: computing-software.ai-ml-engineering.llama-cpp.build-hip-rocm
name: build-hip-rocm
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, hip, rocm, amd-gpu, gpu-targets]
level: practitioner
status: docs-checked
description: "Build for AMD GPUs with HIP, set GPU targets and use the HIP runtime environment variables."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HIP (AMD) build

Needs ROCm installed (from the distro package manager or the ROCm Quick Start for Linux). Linux example for a gfx1030-compatible GPU, as given in the build guide:

```bash
HIPCXX="$(hipconfig -l)/clang" HIP_PATH="$(hipconfig -R)" \
    cmake -S . -B build -DGGML_HIP=ON -DGPU_TARGETS=gfx1030 -DCMAKE_BUILD_TYPE=Release \
    && cmake --build build --config Release -- -j 16
```

- `GPU_TARGETS` is optional; omitting it builds for all GPUs in the current system.
- If you see `clang: error: cannot find ROCm device library; provide its path via '--rocm-path' ...`, search under `HIP_PATH` for a directory containing `oclc_abi_version_400.bc` and prefix the command with `HIP_DEVICE_LIB_PATH=<that directory>`.
- Windows (x64 Native Tools Command Prompt for VS, gfx1100 example): `set PATH=%HIP_PATH%\bin;%PATH%`, then `cmake -S . -B build -G Ninja -DGPU_TARGETS=gfx1100 -DGGML_HIP=ON -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ -DCMAKE_BUILD_TYPE=Release` and `cmake --build build`. gfx1100 corresponds to Radeon RX 7900 XTX/XT/GRE. Find your GPU string by matching `rocminfo` output (the `gfx` line) against the ROCm processor list; for example gfx1035 maps to gfx1030.

Runtime variables:

- `HIP_VISIBLE_DEVICES`: which GPU(s) are used.
- `HSA_OVERRIDE_GFX_VERSION`: for a GPU that is not officially supported, set it to a similar GPU, for example `10.3.0` on RDNA2 (gfx1030, gfx1031, gfx1035) or `11.0.0` on RDNA3. Not supported on Windows.
- `GGML_CUDA_ENABLE_UNIFIED_MEMORY=1` (Linux): uses unified memory so main memory is shared between CPU and integrated GPU. It hurts performance on non-integrated GPUs but enables working with integrated GPUs.

Use `--list-devices` to see the devices llama.cpp finds.

## Checked

Date: 2026-11-08. Confirmed against the HIP section of docs/build.md. Removed: `GGML_HIP_RCCL` and the `-rocm` Docker image tags (not on the page), and the statement that HSA_OVERRIDE_GFX_VERSION=10.3.0 applies to all gfx1030-class cards (the page names RDNA2 and RDNA3 values).

Method: docs-only read of cited pages, 2026-11-08
