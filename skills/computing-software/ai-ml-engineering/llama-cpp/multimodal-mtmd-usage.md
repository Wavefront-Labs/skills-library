---
id: computing-software.ai-ml-engineering.llama-cpp.multimodal-mtmd-usage
name: multimodal-mtmd-usage
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, multimodal, mtmd, mmproj, vision-models]
level: practitioner
status: docs-checked
description: "Run vision and audio models with libmtmd, the mmproj file and llama-mtmd-cli or llama-server."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/docs/multimodal.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Multimodal models (libmtmd)

llama.cpp supports image, audio and video input through `libmtmd`. The tools are `llama-cli`, `llama-server` (via the OpenAI-compatible chat completions API) and `llama-mtmd-cli` (for testing and development).

Enable it with either method:

- `-hf` with a supported model. `--no-mmproj` loads the model with multimodal disabled; `--mmproj local_file.gguf` uses a custom projector file instead.
- `-m model.gguf --mmproj file.gguf` to give the text model and the multimodal projector separately.

The projector is offloaded to the GPU by default; add `--no-mmproj-offload` to disable that.

```bash
llama-mtmd-cli -hf ggml-org/gemma-3-4b-it-GGUF
llama-server -hf ggml-org/gemma-3-4b-it-GGUF
llama-server -m gemma-3-4b-it-Q4_K_M.gguf --mmproj mmproj-gemma-3-4b-it-Q4_K_M.gguf
llama-server -hf ggml-org/gemma-3-4b-it-GGUF --no-mmproj-offload
```

Pre-quantized models (mostly Q4_K_M) are in the ggml-org multimodal GGUFs collection on Hugging Face; some models need a large context window, e.g. `-c 8192`. OCR models are trained with specific prompt and input structure; the page links per-model discussions for PaddleOCR-VL, GLM-OCR, Deepseek-OCR, Dots.OCR and HunyuanOCR.

## Checked

2026-11-04: confirmed against the llama.cpp `docs/multimodal.md` page. Removed `--mmproj-url`, `--image`/`--audio`/`--video` flags, `--image-min/max-tokens`, `--video-fps`, the model-conversion command and projector-quantization advice, and the `GET /props` remark (not on this page).
Method: documentation only; no commands were run.
