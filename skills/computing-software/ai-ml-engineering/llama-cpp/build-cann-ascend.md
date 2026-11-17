---
id: computing-software.ai-ml-engineering.llama-cpp.build-cann-ascend
name: build-cann-ascend
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, cann, ascend, npu, acl-graph]
level: advanced
status: docs-checked
description: "Build for Huawei Ascend NPUs with CANN and tune runtime behaviour through GGML_CANN environment variables."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/docs/backend/CANN.md", "https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# CANN (Ascend NPU)

Install the CANN driver and toolkit, verify with `npu-smi info`, source the environment script (`source /usr/local/Ascend/cann/set_env.sh`, adjust the path if needed), then:

```bash
cmake -B build -DGGML_CANN=on -DCMAKE_BUILD_TYPE=release
cmake --build build --config release
```

The backend page lists Linux (verified on Ubuntu 22.04 and OpenEuler 22.03) and devices including Atlas A2 Infer (910B, for example Atlas 300I A2) and Atlas Infer (310P, for example Atlas 300I Duo) as supported. Data types: on 910B, FP16, BF16, Q8_0 and Q4_0 are supported; on 310P, only FP16 is fully supported (BF16 no, quantized matmul not implemented). The page has a model support table; check it for your model.

ACL graph execution needs a build option: add `-DUSE_ACL_GRAPH=ON` at build time. `GGML_CANN_ACL_GRAPH` (enabled by default) only has an effect if that option was set at compile time.

Runtime environment variables:

- `GGML_CANN_MEM_POOL`: memory pool strategy, default `vmm` (virtual memory manager pool, falls back to `leg` if VMM is unavailable); `prio` is a priority-queue pool; `leg` is a fixed-size buffer pool.
- `GGML_CANN_DISABLE_BUF_POOL_CLEAN`: disables automatic pool cleanup; only effective with `prio` or `leg`.
- `GGML_CANN_WEIGHT_NZ`: convert matmul weights from ND to NZ format; enabled by default.
- `GGML_CANN_ACL_GRAPH`: ACL graph execution instead of op-by-op mode; enabled by default.
- `GGML_CANN_GRAPH_CACHE_CAPACITY`: maximum compiled graphs kept in the LRU cache, default 12.
- `GGML_CANN_PREFILL_USE_GRAPH`: ACL graph execution during prefill, default false; only effective when flash attention is enabled.
- `GGML_CANN_OPERATOR_FUSION`: fuse compatible operators (such as ADD + RMS_NORM), default false.
- `GGML_CANN_NO_PINNED`: when set (any value), skips pinned host buffers and uses pageable memory; use it if pinned allocation fails.

Device selection: single device `--split-mode none --main-gpu DEVICE_ID` (`-sm none -mg 0`); multiple devices `--split-mode layer` (the default). Test run from the guide: `./build/bin/llama-cli -m PATH_TO_MODEL -p "Building a website can be done in 10 steps:" -ngl 32`; the log shows `CANN model buffer size` lines when the backend is in use.

Docker: build with `docker build -t llama-cpp-cann -f .devops/llama-cli-cann.Dockerfile .`, then run passing `--device /dev/davinci0`, `/dev/davinci_manager`, `/dev/devmm_svm` and `/dev/hisi_hdc` plus the driver volume mounts shown on the page.

## Checked

Date: 2026-11-08. Confirmed against docs/backend/CANN.md and the CANN section of docs/build.md. Corrected: `GGML_CANN_WEIGHT_NZ` and `GGML_CANN_ACL_GRAPH` default to enabled, and `GGML_CANN_PREFILL_USE_GRAPH` needs flash attention. Removed: `ASCEND_RT_VISIBLE_DEVICES` (not on the page) and the blanket statement about model support.

Method: docs-only read of cited pages, 2026-11-08
