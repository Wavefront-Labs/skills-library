---
id: computing-software.ai-ml-engineering.vllm.openai-compatible-server
name: openai-compatible-server
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [openai-compatible, api-key, extra-body, generation-config, x-request-id]
level: practitioner
status: docs-checked
description: "Run the OpenAI-compatible vLLM server, pass vLLM-only parameters, and avoid the api-key and generation-config traps."
sources:
  - https://docs.vllm.ai/en/latest/serving/online_serving/openai_compatible_server/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: serve a model over OpenAI-style HTTP and call it with the official OpenAI client.

```bash
vllm serve NousResearch/Meta-Llama-3-8B-Instruct --dtype auto --api-key token-abc123
```

Client: `OpenAI(base_url="http://localhost:8000/v1", api_key="token-abc123")`.

Supported APIs: Completions `/v1/completions` (no `suffix`), Chat Completions `/v1/chat/completions` (`user` ignored; `image_url.detail` unsupported), `/v1/chat/completions/batch`, Responses `/v1/responses`, Embeddings `/v1/embeddings`, Transcriptions `/v1/audio/transcriptions` and Translations `/v1/audio/translations`. `parallel_tool_calls=false` returns zero or one tool call; the default `true` does not guarantee several.

Traps:
- `--api-key` (or `VLLM_API_KEY`) only authenticates `/v1`, `/v2` and `/inference` paths. Other endpoints, notably `/invocations`, are unauthenticated; put a reverse proxy in front.
- The server applies the model repository's `generation_config.json` by default, which can override sampling defaults. Pass `--generation-config vllm` to disable that.

vLLM-only parameters such as `top_k` go in `extra_body={"top_k": 50}` or directly in the JSON payload. Example: `extra_body={"structured_outputs": {"choice": ["positive", "negative"]}}`.

Headers: `--enable-request-id-headers` enables `X-Request-Id`. `X-Vllm-Priority` (integer) overrides the body `priority` on Completions, Chat and Responses; non-zero priorities need priority scheduling on the server.

## Checked

2026-11-03. Confirmed against the OpenAI-Compatible Server page (docs.vllm.ai/en/latest/): supported endpoints and notes, API-key scope warning, generation config default, extra_body and headers.

Method: documentation only; no commands were run.
