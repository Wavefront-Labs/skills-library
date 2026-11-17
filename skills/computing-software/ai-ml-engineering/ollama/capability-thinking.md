---
id: computing-software.ai-ml-engineering.ollama.capability-thinking
name: capability-thinking
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [thinking, think-parameter, reasoning, hidethinking, think]
level: practitioner
status: docs-checked
description: "Request reasoning traces with the think field (true, false, null or a named level) and read message.thinking separately from content."
sources:
  - https://docs.ollama.com/capabilities/thinking.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: enable, hide or tune model thinking.

Thinking-capable models emit a `thinking` field separate from the final answer. Set `think` on chat or generate requests:

- `true`: request thinking output
- `false`: request none, if the model permits
- `null`: use the model default
- a string: a supported level from `thinking.values`, using the exact value from `/api/show`. Numbers are not supported.

```
curl http://localhost:11434/api/chat -d '{
  "model": "qwen3",
  "messages": [{"role": "user", "content": "How many letter r are in strawberry?"}],
  "think": true,
  "stream": false
}'
```

Chat returns `message.thinking` and `message.content`; generate returns `thinking` and `response`.

Discover controls first: `curl http://localhost:11434/api/show -d '{"model": "gpt-oss"}'` returns `thinking` with `values` (booleans, or levels like `["low","medium","high"]`) and `default`. `values: [false]` means thinking unsupported; if `thinking` is missing the model has no metadata and may think anyway. Unsupported level names use the model default.

Streaming: thinking tokens arrive before answer tokens, so on the first `thinking` chunk show a thinking section, then switch when `content` arrives.

Python and JavaScript clients expose the same field (`response.message.thinking`).

## Checked

Method: 2026-11-08 read the full thinking page. Removed unsupported claims (CLI --hidethinking, OpenAI reasoning_effort and Anthropic thinking mappings); the rest matches the page.
