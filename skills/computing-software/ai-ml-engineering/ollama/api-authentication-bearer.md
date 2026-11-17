---
id: computing-software.ai-ml-engineering.ollama.api-authentication-bearer
name: api-authentication-bearer
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [api-key, bearer, ollama-api-key, signin]
level: practitioner
status: docs-checked
description: "Authenticate to ollama.com with an Authorization Bearer OLLAMA_API_KEY header, and use signin for cloud models via local."
sources:
  - https://docs.ollama.com/api/authentication.md
  - https://docs.ollama.com/cloud.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: call Ollama's cloud securely.

The local API at `http://localhost:11434` needs no authentication.

Direct cloud inference at `https://ollama.com/api` and `https://ollama.com/v1` requires an API key; no local installation is needed. Create a key at ollama.com/settings/keys, export it, and send it as a bearer token:

```
export OLLAMA_API_KEY="your_api_key"
curl https://ollama.com/api/chat \
  -H "Authorization: Bearer $OLLAMA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "gemma4:31b", "messages": [{"role": "user", "content": "Hi"}], "stream": false}'
```

Rules from the authentication and cloud pages:

- Use `Authorization: Bearer`; this also applies to the hosted Anthropic-compatible `/v1/messages` endpoint, and `x-api-key` alone is not supported.
- Keys do not expire; revoke them in the API keys settings.
- Keep the key out of browser code and source control.

Signing in: run `ollama signin`; Ollama then authenticates cloud requests for you, including through the local API, for example model `gpt-oss:120b-cloud` sent to `http://localhost:11434/api/generate`. Signing in is also needed to publish models or download private ones.

## Checked

Method: 2026-11-08 read both pages in full. Removed the unsupported OpenAI-client api_key placeholder detail; the signin, bearer and key-lifecycle claims match the pages.
