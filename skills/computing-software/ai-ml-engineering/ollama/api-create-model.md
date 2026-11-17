---
id: computing-software.ai-ml-engineering.ollama.api-create-model
name: api-create-model
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [api-create, quantize, create-from, local-only, apicreate]
level: advanced
status: docs-checked
description: "Create a model with POST /api/create using from, system, template, parameters, messages, files and quantize."
sources:
  - https://docs.ollama.com/api/create.md
  - https://docs.ollama.com/modelfile.md
  - https://docs.ollama.com/import.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: build a model programmatically instead of with a Modelfile.

```
curl http://localhost:11434/api/create -d '{
  "model": "mario",
  "from": "llama3.2",
  "system": "You are Mario from Super Mario Bros."
}'
```

Fields from the reference (only `model` is required):

- `model`: name for the new model.
- `from`: existing model to build on.
- `template`, `renderer`, `parser`: prompt template and the named renderer and parser.
- `system`: system prompt to embed.
- `parameters`: key-value parameters such as `temperature`.
- `messages`: message history (each with `role` of system, user, assistant or tool, `content`, and optional `images`).
- `license`: a string or a list.
- `files`: source file names mapped to SHA-256 digests (split GGUF models must include each shard under its original split filename), and `draft_files` for draft models.
- `quantize`: quantization level applied during import (for example `nvfp4`), and `draft_quantize` for draft weights.
- `requires`: minimum Ollama version.
- `capabilities`: capabilities added without removing inherited or inferred ones.
- `stream`: default true; streams status updates.

The response is status objects with `status`, and for transfers `digest`, `total` and `completed`.

The CLI form is `ollama create mario -f ./Modelfile`. The Modelfile has matching instructions for several of these fields (`FROM`, `TEMPLATE`, `SYSTEM`, `PARAMETER`, `MESSAGE`, `LICENSE`, `REQUIRES`, `CAPABILITY`).

## Checked

2026-11-08. The request fields, defaults, status response fields and `files` rule against the create reference (docs.ollama.com/api/create); the matching Modelfile instructions against the Modelfile page; import-time quantization context against the import page. Removed the claim that the cloud API does not offer model creation (no cited page says so), the claim that "every field maps to a Modelfile instruction" (renderer, parser, files and quantize have no listed instruction), and the statement that `"stream": false` returns only the final status (the reference only says it controls streaming).

Method: documentation only; no commands were run.
