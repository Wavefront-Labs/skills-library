---
id: computing-software.ai-ml-engineering.ollama.keep-alive-and-preload
name: keep-alive-and-preload
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [keep-alive, preload, unload, ollama-keep-alive]
level: practitioner
status: docs-checked
description: "Control how long a model stays loaded with keep_alive or OLLAMA_KEEP_ALIVE and preload one with an empty request."
sources:
  - https://docs.ollama.com/faq.md
  - https://docs.ollama.com/api/generate.md
  - https://docs.ollama.com/api/ps.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: balance first-response latency against memory.

Default: a model stays in memory for 5 minutes after its last request.

Preload without generating text by sending an empty request:

```
curl http://localhost:11434/api/generate -d '{"model": "llama3.2"}'
curl http://localhost:11434/api/chat -d '{"model": "llama3.2"}'
```

or `ollama run llama3.2 ""`.

Per request, `keep_alive` accepts:

- a duration string such as `"10m"` or `"24h"`
- a number of seconds
- a negative number (for example `-1`) to keep the model loaded indefinitely
- `0` to unload immediately after the response

Preload and keep resident: `{"model": "llama3.2", "keep_alive": -1}`.

Unload explicitly:

```
curl http://localhost:11434/api/generate -d '{"model": "llama3.2", "keep_alive": 0}'
```

or `ollama stop llama3.2`.

Server-wide default: `OLLAMA_KEEP_ALIVE`, which takes the same value formats. The FAQ states that the `keep_alive` API parameter overrides the environment variable.

Check what is loaded and when it expires with `ollama ps` or `GET /api/ps` (the `expires_at` field).

The generate and chat references describe `keep_alive` as the model keep-alive duration, for example `5m`, or `0` to unload immediately; `/api/embed` accepts it too.

## Checked

2026-11-08. Default 5 minutes, empty-request preload, `ollama run llama3.2 ""`, the four `keep_alive` forms, `ollama stop`, `OLLAMA_KEEP_ALIVE` and the override rule against the FAQ (docs.ollama.com/faq); `keep_alive` on generate and embed and `expires_at` on `/api/ps` against the API pages. Added the FAQ's `-1` preload example and the ps source. Nothing removed.

Method: documentation only; no commands were run.
