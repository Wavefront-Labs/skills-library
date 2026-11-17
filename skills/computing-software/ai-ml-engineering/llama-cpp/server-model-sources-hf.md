---
id: computing-software.ai-ml-engineering.llama-cpp.server-model-sources-hf
name: server-model-sources-hf
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, hugging-face, model-download, hf-token, offline]
level: practitioner
status: docs-checked
description: "Load models from Hugging Face with -hf, choose a quant tag, set tokens, and run offline."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Model sources and downloads

- `-m FILE`: local GGUF file.
- `-mu URL`: download a model from a direct URL.
- `-hf <user>/<model>[:quant]`: download from Hugging Face. The quant tag is optional and defaults to Q4_K_M, falling back to the first file in the repo if that is absent. The multimodal projector (`mmproj`) is downloaded automatically when available; `--no-mmproj` disables it.
- `-hff FILE`: pick a specific file in the repo.
- `-hft TOKEN` (env `HF_TOKEN`): Hugging Face access token; the default is the value of the `HF_TOKEN` environment variable.
- `-dr, --docker-repo`: pull from a Docker Hub model repository.
- `--offline`: never use the network; rely on the cache.

Examples:

```bash
llama-server -hf <user>/<model>
llama-server -hf <user>/<model>:Q4_K_M
```

Cached models are controlled by the `LLAMA_CACHE` environment variable. Behind a corporate proxy, export `HTTP_PROXY` and `HTTPS_PROXY` first.

In router mode the cache is the default model source, and the README says to restart the server after adding a new model.

## Checked

2026-11-08. Confirmed in the llama.cpp server README: -m, -mu, -hf quant default and fallback, automatic mmproj download and --no-mmproj, -hff, -hft, -dr, --offline, LLAMA_CACHE, the proxy variables and the router cache behaviour. Removed: the specific example repositories (replaced by placeholders) and the claim about GET /models listing downloads.

Method: docs-only read of cited pages, 2026-11-08
