---
id: computing-software.ai-ml-engineering.llama-cpp.router-model-presets-ini
name: router-model-presets-ini
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, model-presets, ini-file, router-mode, preset-precedence]
level: advanced
status: docs-checked
description: "Write an INI preset file for router mode, with key syntax, precedence and preset-only options."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Model presets

```bash
llama-server --models-preset /path/to/my-models.ini
```

Each section defines a preset. Keys are command-line arguments without leading dashes: `--n-gpu-layers 123` becomes `n-gpu-layers = 123`. Short forms (`c`, `ngl`) and environment variable names (`LLAMA_ARG_N_GPU_LAYERS`) also work.

```ini
version = 1
[*]
c = 8192
n-gpu-layers = 8

[ggml-org/MY-MODEL-GGUF:Q8_0]
chat-template = chatml
jinja = true
c = 4096
model-draft = /path/to/draft.gguf

[custom_model]
model = /path/to/my-model-Q4_K_M.gguf
```

- `[*]` holds global settings shared by all presets.
- A section named after an existing model supplies defaults for it; otherwise the section needs at least a model path or HF repo.
- Negation uses the `no-` prefix for flags.
- Relative file paths are relative to the server's working directory; absolute paths are recommended.

Precedence, highest first: command-line arguments, model-specific preset options, global `[*]` options.

Preset-only options:

- `load-on-startup` (boolean): applies only at startup.
- `stop-timeout` (seconds): wait after an unload request before forcing termination, default 10.
- `dedup-cache-models` (boolean): hide the cached entry from `GET /models` when a preset uses `hf-repo` for an already downloaded model.

## Checked

2026-11-08. Confirmed in the llama.cpp server README: key syntax, short forms and env names, the example file structure, global section, negation prefix, path advice, precedence order and the three preset-only options with the stop-timeout default of 10. Nothing removed.

Method: docs-only read of cited pages, 2026-11-08
