---
id: computing-software.ai-ml-engineering.vllm.context-extension
name: context-extension
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [context-extension, rope-parameters, yarn, hf-overrides, max-model-len]
level: practitioner
status: docs-checked
description: "Extend a model's context with YaRN rope_parameters via --hf-overrides and a larger --max-model-len."
sources:
  - https://docs.vllm.ai/en/latest/features/context_extension/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: serve a model beyond its trained context length.

The old `--rope-scaling` parameter is no longer supported. Use `--hf-overrides` with `rope_parameters` instead.

Online example extending Qwen3-0.6B four-fold with YaRN:

```bash
vllm serve Qwen/Qwen3-0.6B \
  --hf-overrides '{"rope_parameters": {"factor": 4.0, "original_max_position_embeddings": 32768, "rope_theta": 1000000, "rope_type": "yarn"}}' \
  --max-model-len 131072
```

Then call it with the OpenAI client pointed at `http://localhost:8000/v1` using any dummy API key.

Parameters depend on the chosen `rope_type`; the page defers to the Hugging Face Transformers RoPE documentation for the full list. Common ones:
- `rope_type`: the RoPE implementation, for example `yarn`, `linear` or `dynamic`.
- `factor`: the factor by which to extend context.
- `original_max_position_embeddings`: the model's original maximum.

vLLM-specific: `max_model_len` is the new maximum sequence length (original times factor). It is used for KV cache pre-allocation and for the request limit at serving time, so set it consistently with `factor`.

An offline example script (`context_extension_offline.py`) uses the same YaRN method with a Qwen model and a simple chat call.

## Checked

2026-11-03. Confirmed against the Context Extension page (docs.vllm.ai/en/latest/): rope-scaling removal, hf-overrides example, rope parameters and max_model_len.

Method: documentation only; no commands were run.
