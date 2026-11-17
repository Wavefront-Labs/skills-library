---
id: computing-software.ai-ml-engineering.ollama.api-pull-push-models
name: api-pull-push-models
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [api-pull, api-push, insecure, progress, apipull]
level: practitioner
status: docs-checked
description: "Download with POST /api/pull and publish with POST /api/push, reading status, digest, total and completed progress."
sources:
  - https://docs.ollama.com/api/pull.md
  - https://docs.ollama.com/api/push.md
  - https://docs.ollama.com/import.md
  - https://docs.ollama.com/faq.md
  - https://docs.ollama.com/cloud.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: transfer models over the API.

```
curl http://localhost:11434/api/pull -d '{"model": "llama3.2"}'
curl http://localhost:11434/api/push -d '{"model": "myuser/mymodel"}'
```

Both take:

- `model` (required): the model to download or publish.
- `insecure`: allow transfers over insecure connections.
- `stream`: default true, streaming progress updates.

Progress objects carry `status` (a human-readable message), `digest` (the content digest, if applicable), `total` (bytes expected) and `completed` (bytes transferred so far). Both references include a non-streaming example with `"stream": false`.

A progress percentage is `completed / total` (the skill's arithmetic, not a documented field).

Pushing needs an ollama.com account, your public key added to that account, and a model named under your username (use `ollama cp mymodel myuser/mymodel` first). Details are in the import and sharing skill.

Cloud models do not need to be downloaded (cloud page).

CLI equivalents: `ollama pull <model>` and `ollama push <myuser/model>`.

The FAQ says Ollama pulls models over the Internet using HTTPS only; behind a proxy set `HTTPS_PROXY` for the server (see the proxy skill).

## Checked

2026-11-08. Request fields, defaults and progress fields against the pull and push references; account, key and cp steps against the import page; HTTPS and proxy against the FAQ; cloud models against the cloud page. Removed "creating or deleting models needs a local server" (not on the cited pages) and the claim about cloud identifiers (kept to what the cloud page says). Marked the percentage formula as derived.

Method: documentation only; no commands were run.
