---
id: computing-software.ai-ml-engineering.llama-cpp.server-chat-completions
name: server-chat-completions
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, chat-completions, openai-compatible, response-format, jinja]
level: practitioner
status: docs-checked
description: "Use POST /v1/chat/completions: response_format for JSON, template kwargs, timings and usage objects."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# POST /v1/chat/completions

OpenAI-compatible chat endpoint with synchronous and streaming modes. The README makes no strong claim of full OpenAI spec compatibility. Models with a supported chat template work best; by default the ChatML template is used. llama.cpp `/completion`-specific features such as `mirostat` are also supported.

```python
import openai
client = openai.OpenAI(base_url="http://localhost:9931/v1", api_key="sk-no-key-required")
r = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Write a limerick"}])
```

Extra fields:

- `response_format`: `{"type": "json_object"}` for plain JSON, or `{"type": "json_object", "schema": {...}}` / `{"type": "json_schema", "schema": {...}}` for schema-constrained output.
- `chat_template_kwargs`: extra parameters for the templating system, for example `{"enable_thinking": false}`.
- `reasoning_effort`: `none` disables reasoning; other values are made available to the Jinja template.
- `reasoning_format`: the reasoning format to parse; `none` outputs the raw generated text.
- `parallel_tool_calls`: enable parallel tool calls; only supported on some models, verified from the Jinja template.

Tool calling (OpenAI-style function calling) needs the `--jinja` flag, and may need a `--chat-template-file` override for a tool-use compatible template.

The response carries a `timings` object (`cache_n`, `prompt_n`, `prompt_ms`, `prompt_per_second`, `predicted_n`, `predicted_per_second`, ...) and a standard `usage` object including `prompt_tokens_details.cached_tokens`. Total tokens in context equal `prompt_n + cache_n + predicted_n`.

`POST /v1/chat/completions/input_tokens` counts tokens for a chat completion body. `POST /v1/completions` is the OpenAI-compatible completions route and `GET /v1/models` the OpenAI-compatible model info route.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the llama.cpp server README sections for `/v1/chat/completions`, its timings and usage notes, `/v1/chat/completions/input_tokens`, `/v1/completions` and `/v1/models`. Removed: "only models with a supported chat template work" (the page says they work optimally and ChatML is the default) and the claim that streaming mode returns the same timings object, which the page does not state.
