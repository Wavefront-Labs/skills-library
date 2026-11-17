---
id: computing-software.ai-ml-engineering.ollama.openai-compatibility-endpoints
name: openai-compatibility-endpoints
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [openai, v1-chat-completions, responses-api, base-url, v1chatcompletions]
level: practitioner
status: docs-checked
description: "Point an OpenAI client at Ollama /v1 endpoints (chat completions, responses, embeddings, audio) locally or on the cloud."
sources:
  - https://docs.ollama.com/api/openai-compatibility.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: reuse OpenAI SDKs with Ollama.

Local:

```python
from openai import OpenAI
client = OpenAI(base_url="http://localhost:11434/v1/", api_key="ollama")  # key required but ignored
```

Cloud: `base_url="https://ollama.com/v1"` with `api_key` set to `OLLAMA_API_KEY`. No Ollama installation is needed.

Endpoints on the page: `/v1/chat/completions`, `/v1/completions`, `/v1/models`, `/v1/models/{model}`, `/v1/embeddings`, `/v1/audio/speech`, `/v1/audio/transcriptions`, `/v1/audio/translations` and the Responses API.

`/v1/chat/completions` supports streaming, JSON mode, reproducible outputs, vision (base64 images; image URLs are not supported), tools, and thinking control through `reasoning_effort` or `reasoning.effort`; logprobs are listed as unsupported. Structured outputs work through `response_format`.

Responses API: only the non-stateful flavour; `previous_response_id` and `conversation` are not supported. The cloud API also lacks built-in web search through `/v1/responses` and custom/freeform tool-call replay.

Unsupported speech options return a 400 error rather than being ignored (speech capability page).

Download a model first locally with `ollama pull llama3.2`; direct cloud requests use identifiers from `https://ollama.com/api/tags` and need no pull. Through a signed-in local server pick a cloud model such as `gemma4:cloud`. For tools that expect default OpenAI model names such as `gpt-3.5-turbo`, copy a model to that name with `ollama cp`.

## Checked

2026-11-03. Endpoint list, supported-feature lists, Responses API limits, cloud base URL, `ollama pull` and `ollama cp` note confirmed against the OpenAI compatibility page. Narrowed the 400 claim to speech options and corrected the vision note (image URLs are unsupported).

Method: documentation only; no commands were run.
