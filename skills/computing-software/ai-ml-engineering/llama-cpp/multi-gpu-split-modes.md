---
id: computing-software.ai-ml-engineering.llama-cpp.multi-gpu-split-modes
name: multi-gpu-split-modes
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, multi-gpu, split-mode, tensor-split, nccl]
level: advanced
status: docs-checked
description: "Use several GPUs with --split-mode layer, row or tensor and the related device flags."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/docs/multi-gpu.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Multiple GPUs

`-sm, --split-mode` options:

- `none`: use a single GPU (choose it with `-mg, --main-gpu`).
- `layer`: default; pipeline parallelism, each GPU holds a contiguous slice of layers and the KV cache for those layers.
- `row`: deprecated older row-split path; avoid it, `tensor` supersedes it.
- `tensor`: experimental tensor parallelism splitting weights and KV across GPUs; good performance is expected only with multiple NVIDIA GPUs on the CUDA backend.

Related flags:

- `-ts, --tensor-split 3,1`: proportion of the model each GPU gets, by device order.
- `-mg, --main-gpu N`: the single GPU used in `--split-mode none` (default 0).
- `--list-devices`: show devices.
- `-dev, --device DEV1,DEV2`: choose devices explicitly.
- `CUDA_VISIBLE_DEVICES` and similar variables restrict the visible devices.

Tensor mode requirements and limits from the page:

- It needs flash attention (`-fa on`) and a non-quantized KV cache.
- `--fit` is not supported with it.
- On some architectures it fails with "LLAMA_SPLIT_MODE_TENSOR not implemented for architecture"; use `layer` for those models.

NCCL is chosen at build time (`-DGGML_CUDA_NCCL=ON`, the default) and used automatically for cross-GPU reductions in tensor mode; without it a one-time warning says multi-GPU performance will be suboptimal. RCCL for ROCm is `-DGGML_HIP_RCCL=ON` and is off by default.

Example (`-ts 3,1` on two GPUs gives GPU 0 75 % and GPU 1 25 %):

```bash
llama-cli -m model.gguf -ts 3,1
```

## Checked

2026-11-04: confirmed against the llama.cpp `docs/multi-gpu.md` page: split modes, flags and defaults, tensor-mode limits, NCCL/RCCL. Fixed the `-mg` description and the layer/row wording; replaced the unconfirmed `-ngl 99 -sm layer` server example with the page's recipe.
Method: documentation only; no commands were run.
