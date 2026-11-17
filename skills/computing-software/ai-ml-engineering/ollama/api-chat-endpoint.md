---
id: computing-software.ai-ml-engineering.ollama.api-chat-endpoint
name: api-chat-endpoint
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [api-chat, messages, roles, tool-calls, apichat]
level: intro
status: docs-checked
description: "Call POST /api/chat with a messages array, tools, format, think and options, and read message.content in the reply."
sources:
  - https://docs.ollama.com/api/chat.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: multi-turn chat over HTTP.

```
curl http://localhost:11434/api/chat -d '{
  "model": "gemma3",
  "messages": [
    {"role": "user", "content": "why is the sky blue?"}
  ],
  "stream": false
}'
```

Required fields: `model` and `messages`, an array of objects each with a `role` (`system`, `user`, `assistant` or `tool`) and `content`. A message can also carry `images` (base64) for multimodal models and `tool_calls` produced by the model.

Optional fields: `tools` (function tool definitions with `type: function`, `name`, `description`, JSON-schema `parameters`), `format` (`json` or a JSON schema), `options` (seed, temperature, top_k, top_p, min_p, stop, num_ctx, num_predict, others allowed), `stream` (default true), `think` (boolean, model-defined string or null; check `/api/show` for supported values), `keep_alive`, `logprobs` and `top_logprobs`.

The reply has `message` with `role` (assistant), `content` and optionally `thinking` and `tool_calls`, plus `done`, `done_reason` and duration and token-count metrics (`total_duration`, `load_duration`, `prompt_eval_count`, `prompt_eval_cached_count`, `prompt_eval_duration`, `eval_count`, `eval_duration`). Streaming (the default) returns NDJSON events with partial `message` fields and `done: true` on the last.

The reference's samples cover default, non-streaming, structured outputs, tool calling, thinking and images.

## Checked

Method: 2026-11-08 read the full OpenAPI page at docs.ollama.com/api/chat.md. Removed unsupported claims (statelessness advice, tool_name on tool messages, preload without messages, cloud variant); the rest matches the page.
