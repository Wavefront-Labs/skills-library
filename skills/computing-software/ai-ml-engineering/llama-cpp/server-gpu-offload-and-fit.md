---
id: computing-software.ai-ml-engineering.llama-cpp.server-gpu-offload-and-fit
name: server-gpu-offload-and-fit
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, gpu-offload, n-gpu-layers, fit, memory]
level: practitioner
status: docs-checked
description: "Control how many layers go to the GPU with -ngl and let --fit size arguments to free device memory."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md", "https://github.com/ggml-org/llama.cpp/blob/master/docs/development/token_generation_performance_tips.md", "https://github.com/ggml-org/llama.cpp/blob/master/tools/llama-bench/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# GPU offload and --fit

- `-ngl, --n-gpu-layers N|auto|all`: layers kept in VRAM. Default `auto`; env `LLAMA_ARG_N_GPU_LAYERS`.
- `-fit, --fit [on|off]`: adjust unset arguments so the model fits in device memory. Default `on`. It only changes values you did not set explicitly.
- `-fitt, --fit-target MiB`: free memory to leave per device, default 1024. Comma-separated values give per-device margins.
- `-fitc, --fit-ctx N`: minimum context size that `--fit` may reduce to, default 4096.
- `-sm, --split-mode`, `-ts, --tensor-split` and `-mg, --main-gpu` control multi-GPU placement.
- `-dev, --device <dev1,dev2,..>` selects the devices to offload to (`none` means do not offload). `--list-devices` prints what is available.
- `--no-host`: bypass the host buffer so extra buffers can be used.

The token-generation performance-tips doc says a very large N (its example is `-ngl 200000`) offloads the maximum possible number of layers, and that the diagnostic lines printed before inference show whether the GPU is being used.

`-sm tensor` (split weights and KV across GPUs) is marked experimental. `llama-bench` also has `-fitt, --fit-target` and `-fitc, --fit-ctx`, where `-fitt` defaults to off.

## Checked

2026-11-08. Confirmed in the llama.cpp server README: -ngl, -fit, -fitt, -fitc, -sm, -ts, -mg, -dev, --list-devices and --no-host with their defaults; in the performance-tips doc the -ngl 200000 example; in the llama-bench README the -fitt and -fitc options. Removed: the claim that --fit is unsupported with split mode tensor and the startup-log description (neither is stated in the pages).

Method: docs-only read of cited pages, 2026-11-08
