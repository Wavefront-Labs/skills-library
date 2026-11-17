---
id: computing-software.ai-ml-engineering.llama-cpp.build-sycl-intel
name: build-sycl-intel
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, sycl, intel-gpu, oneapi, level-zero]
level: advanced
status: docs-checked
description: "Build and run the SYCL backend on Intel GPUs: compilers, device selection and split modes."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/docs/backend/SYCL.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# SYCL (Intel GPU)

SYCL supports Intel GPUs (Data Center Max, Flex, Arc, built-in GPU and iGPU). Install the oneAPI toolkit, source its environment, check devices with `sycl-ls` (look for a `[level_zero:gpu]` entry), then build on Linux:

```bash
source /opt/intel/oneapi/setvars.sh
cmake -B build -DGGML_SYCL=ON -DCMAKE_C_COMPILER=icx -DCMAKE_CXX_COMPILER=icpx
cmake --build build --config Release
```

Add `-DGGML_SYCL_F16=ON` for the FP16 build. The page says FP32 and FP16 perform differently per model, so test both, and rebuild after changing it (default OFF).

Other CMake options on the page: `GGML_SYCL_TARGET` (default INTEL), `GGML_SYCL_DEVICE_ARCH` (optional, can improve performance), `GGML_SYCL_SUPPORT_XMX` (default ON; set OFF for AOT builds for iGPUs without XMX), `GGML_SYCL_GRAPH`, `GGML_SYCL_DNN` and `GGML_SYCL_HOST_MEM_FALLBACK` (all default ON; the fallback needs Linux kernel 6.8+).

Windows: open the Intel oneAPI command prompt for Visual Studio 2022. The page builds with Ninja and `-DGGML_SYCL=ON -DCMAKE_C_COMPILER=cl -DCMAKE_CXX_COMPILER=icx -DCMAKE_BUILD_TYPE=Release`, or with the `x64-windows-sycl-release` preset; a Visual Studio generator route is also shown.

Device selection:

- `ONEAPI_DEVICE_SELECTOR`: the default SYCL backend is `level_zero`. `level_zero:0` selects device 0, `level_zero:1` device 1, `"level_zero:0;level_zero:1"` both.
- llama.cpp flags: single device `--split-mode none --main-gpu DEVICE_ID`; multiple devices `--split-mode layer` (default); `--split-mode tensor` (tensor parallelism) shards each layer across the selected GPUs, requires flash attention (auto-enabled with the default `--flash-attn auto`; `--flash-attn off` is rejected with it) and is currently optimised for 2 GPUs. `--split-mode row` is not supported.
- `ZES_ENABLE_SYSMAN=1` lets the backend get GPU free memory; the page recommends it with `--split-mode layer`.

Run (from the page):

```bash
ZES_ENABLE_SYSMAN=1 ./build/bin/llama-completion -no-cnv -m models/llama-2-7b.Q4_0.gguf -p "Building a website can be done in 10 simple steps:" -n 400 -e -ngl 99 -sm none -mg 0 --load-mode auto
```

`SYCL_CACHE_PERSISTENT=1` is not recommended by the backend (it can crash). Docker usage is described on a separate "Docker with SYCL" page.

## Checked

Date: 2026-11-08. Confirmed against docs/backend/SYCL.md (Linux and Windows sections, CMake options, environment variables, troubleshooting). Removed: the `-sm tensor (experimental)` label, the `-intel` Docker tag claim, `llama-cli` as the example binary (the page uses `llama-completion`) and the closing log-check remark.

Method: docs-only read of cited pages, 2026-11-08
