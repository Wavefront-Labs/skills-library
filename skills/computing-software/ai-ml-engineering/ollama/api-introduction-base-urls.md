---
id: computing-software.ai-ml-engineering.ollama.api-introduction-base-urls
name: api-introduction-base-urls
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [rest-api, base-url, localhost-11434, python-js-libraries, api]
level: intro
status: docs-checked
description: "Pick the right Ollama API base URL (local http://localhost:11434/api or cloud https://ollama.com/api) and the official client libraries."
sources:
  - https://docs.ollama.com/api/introduction.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: send the first request to the right server.

Base URLs:

| API | Direct cloud | Local server |
| - | - | - |
| Ollama | `https://ollama.com/api` | `http://localhost:11434/api` |
| OpenAI compatibility | `https://ollama.com/v1` | `http://localhost:11434/v1` |
| Anthropic client base URL | `https://ollama.com` | `http://localhost:11434` |

The Anthropic client appends `/v1/messages` to its base URL.

Cloud requests need an API key (`Authorization: Bearer`) and no Ollama installation; local requests need no key. To use cloud models through your local server, sign in to Ollama. Creating or deleting models requires a local server.

Cloud example (read the answer from `message.content`):

```
curl https://ollama.com/api/chat \
  -H "Authorization: Bearer $OLLAMA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "gemma4:31b", "messages": [{"role": "user", "content": "Why is the sky blue?"}], "stream": false}'
```

For local inference use `http://localhost:11434/api/chat` with a downloaded model and omit the header.

Official libraries: Python (ollama-python) and JavaScript (ollama-js), usable with a local server or the hosted API. For direct cloud access set the host to `https://ollama.com` and supply the key as a bearer header.

Versioning: the API is not strictly versioned but is expected to be stable and backwards compatible; deprecations are rare and announced in release notes.

## Checked

Method: 2026-11-08 read the full introduction page. Removed unsupported claims (endpoint map, GET /api/version, wrapper method names); added the base URL table and versioning wording from the page. Note `stream` defaults to true on endpoints such as generate (see the streaming skill).
