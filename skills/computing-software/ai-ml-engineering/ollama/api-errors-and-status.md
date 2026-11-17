---
id: computing-software.ai-ml-engineering.ollama.api-errors-and-status
name: api-errors-and-status
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [status-codes, error-json, 429, 503, statuscodes]
level: practitioner
status: docs-checked
description: "Interpret Ollama API status codes and the error JSON body, including errors that arrive mid-stream with status 200."
sources:
  - https://docs.ollama.com/api/errors.md
  - https://docs.ollama.com/faq.md
  - https://docs.ollama.com/api/balance.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: handle failures reliably.

Errors return a JSON body of the form `{"error": "the model failed to generate a response"}`. Documented status codes:

- 200: success
- 400: bad request (missing parameters, invalid JSON)
- 404: model not found
- 429: too many requests (rate limit)
- 500: internal server error
- 502: bad gateway (for example when a cloud model cannot be reached)

The FAQ adds that a local server returns 503 when its request queue (`OLLAMA_MAX_QUEUE`, default 512) is full.

Streaming gotcha: if an error happens after a streamed response has begun, the HTTP status has already been sent and stays unchanged. The error arrives as an NDJSON line containing an `error` property, so a client must check every chunk:

```
{"error":"an error was encountered while running the model"}
```

Other endpoint-specific responses: `/api/balance` returns 401 for invalid credentials and 429 with a `Retry-After` header when over its rate limit.

## Checked

2026-11-03. Status code list, error JSON, mid-stream behaviour against the errors page; 503 and queue default against the FAQ (docs.ollama.com/faq); balance 401/429 against the balance page. Removed `/api/copy` and `/v1/systemone` status claims (pages not fetched).

Method: documentation only; no commands were run.
