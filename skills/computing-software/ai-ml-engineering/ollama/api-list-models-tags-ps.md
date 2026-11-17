---
id: computing-software.ai-ml-engineering.ollama.api-list-models-tags-ps
name: api-list-models-tags-ps
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [api-tags, api-ps, list-models, running-models, apitags]
level: intro
status: docs-checked
description: "List installed models with GET /api/tags and running models with GET /api/ps, including size_vram and expires_at."
sources:
  - https://docs.ollama.com/api/tags.md
  - https://docs.ollama.com/api/ps.md
  - https://docs.ollama.com/cloud.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: inspect what is installed and what is loaded.

`GET /api/tags` ("List models") returns `models`, each with:

- `name` and `model`
- `modified_at` (ISO 8601)
- `size` (bytes on disk) and `digest` (SHA256)
- `details`: `format` (such as `gguf`), `family`, `families`, `parameter_size` (such as `7B`) and `quantization_level` (such as `Q4_0`)
- `remote_model` and `remote_host` when the model is remote

Against the cloud, `curl https://ollama.com/api/tags` lists cloud models, and for API requests to ollama.com you use the name it returns (such as `gemma4:31b`), per the cloud page. The CLI equivalent for local models is `ollama ls`.

`GET /api/ps` ("List running models") returns models currently loaded into memory:

- `name`, `model`, `size`, `digest`, `details`
- `expires_at`: when the model will be unloaded
- `size_vram`: VRAM usage in bytes
- `context_length`: the context length for the running model

```
curl http://localhost:11434/api/tags
curl http://localhost:11434/api/ps
```

Neither endpoint defines a request body. Unload with `keep_alive: 0` (see the keep-alive skill).

## Checked

2026-11-08. Response fields and endpoint descriptions against the tags and ps references; cloud tags and naming against the cloud page. Removed the "API form of `ollama ps`" claim for `/api/ps` as a documented equivalence (the FAQ uses `ollama ps` and the references describe the same data, but no page states the mapping); reworded "no request body" to what the references define.

Method: documentation only; no commands were run.
