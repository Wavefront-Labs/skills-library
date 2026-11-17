---
id: computing-software.ai-ml-engineering.ollama.api-generate-endpoint
name: api-generate-endpoint
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [api-generate, prompt, suffix, raw, system, apigenerate]
level: intro
status: docs-checked
description: "Call POST /api/generate with prompt, system, suffix, raw, format, options and images, and read response, thinking and done_reason."
sources:
  - https://docs.ollama.com/api/generate.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: one-shot text completion over HTTP.

```
curl http://localhost:11434/api/generate -d '{
  "model": "gemma3",
  "prompt": "Why is the sky blue?",
  "stream": false
}'
```

Request fields documented in the reference:

- `model` (required) and `prompt`.
- `suffix`: for fill-in-the-middle models, text after the prompt and before the response.
- `images`: base64-encoded images for vision models.
- `format`: the string `"json"` or a JSON schema object (structured outputs).
- `system`: system prompt.
- `stream`: default true.
- `think`: boolean, null (model default) or a model-defined level string such as `"low"`; numbers are not supported.
- `raw`: true returns the raw response without prompt templating.
- `keep_alive`: for example `5m`, or `0` to unload immediately.
- `options`: runtime options such as `temperature`, `top_p`, `top_k`, `min_p`, `stop`, `seed`, `num_ctx`, `num_predict`.
- `logprobs` and `top_logprobs`: log probabilities of output tokens.

Response fields: `response` (generated text), `thinking`, `done`, `done_reason`, `created_at`, and the usage metrics (`total_duration`, `load_duration`, `prompt_eval_count`, `prompt_eval_cached_count`, `prompt_eval_duration`, `eval_count`, `eval_duration`; durations in nanoseconds). Streaming returns NDJSON chunks.

Load a model by sending only the model name; unload it with `"keep_alive": 0`.

## Checked

Method: 2026-11-08 read the full OpenAPI page at docs.ollama.com/api/generate.md. Claims matched; dropped the unsupported "use /api/chat for multi-turn" line and added option names and think semantics from the page.
