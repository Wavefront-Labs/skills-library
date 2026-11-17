---
id: computing-software.ai-ml-engineering.llama-cpp.server-moe-cpu-offload
name: server-moe-cpu-offload
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, moe, cpu-moe, override-tensor, expert-offload]
level: advanced
status: docs-checked
description: "Keep Mixture-of-Experts weights on the CPU with --cpu-moe, --n-cpu-moe and --override-tensor."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# MoE and tensor placement

Mixture-of-Experts models can keep their large expert tensors in system RAM while attention layers use the GPU.

- `-cmoe, --cpu-moe`: keep all MoE weights on the CPU.
- `-ncmoe, --n-cpu-moe N`: keep the MoE weights of the first N layers on the CPU.
- `-cmoed, --cpu-moe-draft` and `-ncmoed, --n-cpu-moe-draft N`: the same for the draft model in speculative decoding.
- `-ot, --override-tensor <tensor name pattern>=<buffer type>,...`: override the buffer type of tensors chosen by a name pattern. Env `LLAMA_ARG_OVERRIDE_TENSOR`.
- `-otd, --override-tensor-draft`: the same for the draft model.
- `--override-kv KEY=TYPE:VALUE,...`: override model metadata, types `int`, `float`, `bool`, `str`.
- `--check-tensors`: validate model tensor data when loading.

Example:

```bash
llama-server -m /path/to/moe-model.gguf -ngl 99 --n-cpu-moe 20
```

`--moe-cache-mib N` sets a GPU cache for the MoE experts kept on the CPU (default 0, disabled). `-ncffn, --n-cpu-ffn N` keeps the dense FFN weights of the first N layers on the CPU (for dense models).

## Checked

2026-11-08. Confirmed in the llama.cpp server README: -cmoe, -ncmoe, the draft-model variants, -ot and its env variable, --override-kv types, --check-tensors, --moe-cache-mib and -ncffn. Removed: the regular-expression wording, the advice to combine with --fit and the startup-log check (not stated in the page).

Method: docs-only read of cited pages, 2026-11-08
