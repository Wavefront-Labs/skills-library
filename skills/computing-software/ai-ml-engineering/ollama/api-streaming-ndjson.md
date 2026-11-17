---
id: computing-software.ai-ml-engineering.ollama.api-streaming-ndjson
name: api-streaming-ndjson
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [ndjson, stream, application-x-ndjson, stream-false, applicationx-ndjson]
level: practitioner
status: docs-checked
description: "Handle Ollama default NDJSON streaming over REST or disable it with stream false to get one JSON object."
sources:
  - https://docs.ollama.com/api/streaming.md
  - https://docs.ollama.com/capabilities/streaming.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: parse streamed responses correctly.

Certain endpoints such as `/api/generate` stream by default over REST. The content type is `application/x-ndjson`: one JSON object per line. Setting `"stream": false` on any endpoint that supports streaming returns a single `application/json` object instead.

```
curl http://localhost:11434/api/chat -d '{
  "model": "gemma3",
  "messages": [{"role": "user", "content": "Hi"}],
  "stream": false
}'
```

Streaming rules:

- Each generate chunk carries a piece in `response` with `"done": false`; the last has `"done": true` and a `done_reason` (example: `stop`).
- Chat chunks carry partial `message.content`; thinking-capable models emit `thinking` alongside, and tool requests arrive as streamed `tool_calls`.
- In the SDKs streaming is off by default; pass `stream=True` (Python) or `stream: true` (JavaScript).
- Accumulate the partial `thinking`, `content` and `tool_calls` yourself to keep conversation history; this matters most for tool calling, where thinking, the tool call and the tool result go back in the next request.
- Docs guidance: streaming gives lower perceived latency and suits long generations; non-streaming is simpler and suits short or structured outputs.

## Checked

Method: 2026-11-08 read both streaming pages in full. Removed unsupported claims (final chunk carries timing and token counts, mid-stream error objects with HTTP 200).
