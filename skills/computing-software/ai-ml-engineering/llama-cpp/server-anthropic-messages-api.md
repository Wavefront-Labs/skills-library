---
id: computing-software.ai-ml-engineering.llama-cpp.server-anthropic-messages-api
name: server-anthropic-messages-api
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, anthropic-messages, count-tokens, tool-use]
level: practitioner
status: docs-checked
description: "Use the Anthropic-compatible POST /v1/messages and /v1/messages/count_tokens routes on llama-server."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# POST /v1/messages

llama-server exposes an Anthropic Messages compatible endpoint with SSE streaming. Tool use requires the `--jinja` flag.

Fields:

- `model` (required) and `messages` (required, role plus content).
- `max_tokens`: default 4096.
- `system`: string or array of content blocks.
- `temperature`: 0 to 1, default 1.0; `top_p` default 1.0; `top_k`.
- `stop_sequences`, `stream` (default false).
- `tools` and `tool_choice` (`{"type": "auto"}`, `{"type": "any"}` or `{"type": "tool", "name": "..."}`); tools need `--jinja`.
- `extra_params`: llama.cpp parameters with no Anthropic field, such as `{"seed": 42, "min_p": 0.05}`; merged into the converted request.

```bash
curl http://localhost:9931/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: your-api-key" \
  -d '{"model": "gpt-4", "max_tokens": 1024,
       "system": "You are a helpful assistant.",
       "messages": [{"role": "user", "content": "Hello!"}]}'
```

`POST /v1/messages/count_tokens` accepts the same parameters (without `max_tokens`) and returns `{"input_tokens": 10}`-style output without generating.

Streaming uses Server-Sent Events. The README's example sends the key in an `x-api-key` header.

## Checked

2026-11-08. Confirmed in the llama.cpp server README: the endpoint, field list and defaults (max_tokens 4096, temperature 1.0, top_p 1.0, stream false), tools needing --jinja, tool_choice shapes, extra_params, the curl example and POST /v1/messages/count_tokens. Reworded: the API key header sentence.

Method: docs-only read of cited pages, 2026-11-08
