---
id: computing-software.ai-ml-engineering.ollama.api-copy-delete-version
name: api-copy-delete-version
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [api-copy, api-delete, api-version, rename-model, apicopy]
level: intro
status: docs-checked
description: "Duplicate a model with POST /api/copy, remove it with DELETE /api/delete and check the server with GET /api/version."
sources:
  - https://docs.ollama.com/api/copy.md
  - https://docs.ollama.com/api/delete.md
  - https://docs.ollama.com/api-reference/get-version.md
  - https://docs.ollama.com/import.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: housekeeping calls over HTTP.

Copy (the API form of `ollama cp`):

```
curl http://localhost:11434/api/copy -d '{
  "source": "llama3.2",
  "destination": "llama3-backup"
}'
```

`source` (existing model name) and `destination` (new name) are both required. Responses: 200 with `{"status": "success"}`, 400 when the model could not be copied, and 404 when the source model is not found; errors carry an `error` message.

Delete (the API form of `ollama rm`):

```
curl -X DELETE http://localhost:11434/api/delete -d '{"model": "llama3:13b"}'
```

`model` is required. The reference documents only the 200 success response.

Version:

```
curl http://localhost:11434/api/version
```

returns `{"version": "..."}`, described as the version of Ollama.

Copying a model to your own namespace before `ollama push` is the sharing flow from the import page (`ollama cp mymodel myuser/mymodel`).

## Checked

2026-11-08. Request fields, status codes, response bodies and examples against the copy, delete and get-version references; the cp-before-push flow against the import page. Removed the claim that the API introduction says creating or deleting models needs a local server, the OpenAI `gpt-3.5-turbo` copy suggestion, and the decision/speech `REQUIRES` version numbers (v0.35.0, v0.40.9): none appear on the cited pages. Changed "an error" for 400 to the reference's wording.

Method: documentation only; no commands were run.
