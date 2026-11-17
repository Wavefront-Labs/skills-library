---
id: computing-software.ai-ml-engineering.ollama.anthropic-compatibility-messages
name: anthropic-compatibility-messages
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [anthropic, v1-messages, anthropic-base-url, claude-code, v1messages]
level: practitioner
status: docs-checked
description: "Use Anthropic clients and Claude Code against Ollama with ANTHROPIC_BASE_URL and the /v1/messages endpoint."
sources:
  - https://docs.ollama.com/api/anthropic-compatibility.md
  - https://docs.ollama.com/integrations/claude-code.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: reuse Anthropic SDKs and tools with Ollama.

Environment for tools such as Claude Code:

```
export ANTHROPIC_AUTH_TOKEN=ollama   # required but ignored
export ANTHROPIC_BASE_URL=http://localhost:11434
```

The client appends `/v1/messages`, so the base URL has no path. Direct cloud access uses `https://ollama.com`, needs `Authorization: Bearer $OLLAMA_API_KEY` (an `x-api-key` header alone is not accepted) and `anthropic-version: 2023-06-01`.

```
curl http://localhost:11434/v1/messages \
  -H "x-api-key: ollama" -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{"model": "qwen3-coder", "max_tokens": 1024, "messages": [{"role": "user", "content": "Hello"}]}'
```

Supported on `/v1/messages`: messages, streaming, system prompts, multi-turn conversations, vision (base64 images), tools and tool results, thinking blocks, and fields such as `temperature`, `top_p`, `top_k`, `stop_sequences`, `thinking` and `output_config.effort`.

Read answers from `content[0].text`. Models must be pulled locally first, or be cloud models.

Claude Code via the CLI: `ollama launch claude`. Choose a model with a 64k or larger context window.

Compatible models support messages, streaming and function calling. The local server does not validate API keys.

## Checked

2026-11-03. Environment variables, cloud Bearer requirement, `anthropic-version`, supported features, `content[0].text`, `ollama launch claude`, 64k context and API-key behaviour confirmed against the Anthropic compatibility and Claude Code integration pages. Nothing removed.

Method: documentation only; no commands were run.
