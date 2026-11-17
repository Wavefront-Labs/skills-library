---
id: computing-software.ai-ml-engineering.ollama.kv-cache-flash-attention
name: kv-cache-flash-attention
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [flash-attention, kv-cache-type, q8-0, q4-0, ollama-kv-cache-type]
level: advanced
status: docs-checked
description: "Enable Flash Attention and quantize the K/V cache with OLLAMA_KV_CACHE_TYPE (f16, q8_0, q4_0) to cut memory."
sources:
  - https://docs.ollama.com/faq.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: reduce memory used by long contexts.

Enable Flash Attention with `OLLAMA_FLASH_ATTENTION=1` (set to `0` to disable). The FAQ describes it as a feature that reduces memory use as context size grows.

Quantize the K/V context cache with `OLLAMA_KV_CACHE_TYPE`. Options:

- `f16`: default, high precision and full memory use.
- `q8_0`: 8-bit, uses about half the memory of `f16` with a very small precision loss; the FAQ recommends it when you need less memory.
- `q4_0`: 4-bit, about one quarter of the memory of `f16`, with a small to medium precision loss that may be more noticeable at higher context sizes.

```
OLLAMA_FLASH_ATTENTION=1 OLLAMA_KV_CACHE_TYPE=q8_0 ollama serve
```

Rules from the page:

- The setting is global, so it applies to all models the server runs.
- K/V cache quantization requires Flash Attention to be enabled.
- How much quality is lost depends on the model and task; the FAQ says models with a high GQA count (for example Qwen2) may see a larger impact.

## Checked

2026-11-03. Flash Attention variable, `OLLAMA_KV_CACHE_TYPE` types and memory ratios, global scope and Flash Attention requirement confirmed against the FAQ (docs.ollama.com/faq). Removed an unsupported claim that not every model supports cache quantization and an uncited closing tip; corrected the `q4_0` precision wording.

Method: documentation only; no commands were run.
