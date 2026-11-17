---
id: computing-software.ai-ml-engineering.llama-cpp.cuda-runtime-environment
name: cuda-runtime-environment
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, cuda-env, unified-memory, cuda-visible-devices, cublas]
level: advanced
status: docs-checked
description: "Runtime environment variables that affect the CUDA backend."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# CUDA runtime environment variables

Set these before launching llama.cpp binaries. All are described in the CUDA section of docs/build.md.

- `CUDA_VISIBLE_DEVICES`: the guide's example hides the first device: `CUDA_VISIBLE_DEVICES="-0" ./build/bin/llama-server --model /srv/models/llama.gguf`.
- `CUDA_SCALE_LAUNCH_QUEUES`: sets the size of CUDA's command buffer, i.e. how many GPU operations can be queued before the CPU waits. The guide suggests `4x` (4 times the default size); a larger buffer reduces CPU-side stalls and particularly helps multi-GPU setups with pipeline parallelism, improving prompt processing throughput.
- `GGML_CUDA_ENABLE_UNIFIED_MEMORY=1`: enables unified memory on Linux, so work can swap to system RAM instead of crashing when VRAM is exhausted. On Windows the equivalent is System Memory Fallback in the NVIDIA control panel.
- `GGML_CUDA_P2P`: enables peer-to-peer access between GPUs so they transfer data directly instead of through system memory. Needs driver support (usually workstation/datacenter GPUs) and may cause crashes or corrupted outputs on some motherboards and BIOS settings (for example IOMMU).
- `GGML_CUDA_CUBLAS_COMPUTE_TYPE`: overrides the default speed-optimised compute type for cuBLAS matmuls. Legal values: `auto`, `f16`, `fp16`, `bf16`, `f32`, `fp32`.
- `GGML_CUDA_MMQ_PREC`: overrides the activation precision requested for NVFP4 and MXFP4 matmuls. Values: `auto` (per-tensor metadata, same as unset), `q8`, `q4`. On Blackwell, layers marked W4A16 run the W4A8 path; `q4` keeps the native W4A4 path (faster prompt processing, less accurate) and `q8` uses W4A8 for every layer.

Example:

```bash
CUDA_VISIBLE_DEVICES="-0" CUDA_SCALE_LAUNCH_QUEUES=4x ./build/bin/llama-server --model /srv/models/llama.gguf
```

The same section notes that MUSA uses `MUSA_VISIBLE_DEVICES` and HIP uses `HIP_VISIBLE_DEVICES`. `--list-devices` shows the devices llama.cpp can use.

## Checked

Date: 2026-11-08. Confirmed against the "Runtime CUDA environmental variables", Unified Memory and Peer Access sections of docs/build.md. Removed: the "more memory" cost for CUDA_SCALE_LAUNCH_QUEUES, the `-ts`/`-mg`/`-sm` flag line and the remark about other backends' variables, none of which are on the page; the old example now follows the page's `-0` form.

Method: docs-only read of cited pages, 2026-11-08
