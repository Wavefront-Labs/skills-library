---
id: computing-software.ai-ml-engineering.ollama.api-embed-endpoint
name: api-embed-endpoint
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [api-embed, embeddings, truncate, dimensions, apiembed]
level: intro
status: docs-checked
description: "Create embeddings with POST /api/embed: single or array input, truncate, dimensions and keep_alive."
sources:
  - https://docs.ollama.com/api/embed.md
  - https://docs.ollama.com/capabilities/embeddings.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: vectorise text for search and RAG.

```
curl http://localhost:11434/api/embed -d '{
  "model": "embeddinggemma",
  "input": ["Why is the sky blue?", "Why is the grass green?"]
}'
```

Request fields:

- `model` and `input` (required): a string or an array of strings.
- `truncate`: default true. When true, inputs that exceed the context window are truncated; when false the call returns an error.
- `dimensions`: number of dimensions to generate.
- `keep_alive`: model keep-alive duration.
- `options`: runtime options.

Response: `embeddings` is an array of vectors, one per input, plus `model`, `total_duration` and `load_duration` (nanoseconds) and `prompt_eval_count` (input tokens processed). The endpoint returns L2-normalised (unit-length) vectors, per the embeddings capability page.

Practice from that page: use cosine similarity for most semantic search and use the same embedding model for indexing and querying. Vector length depends on the model, typically 384 to 1024 dimensions.

From the CLI, `ollama run embeddinggemma "Hello world"` prints a JSON array, and text piped into `ollama run` works too.

## Checked

2026-11-08. Request fields and defaults, response fields, L2 normalisation, batch input, tips, vector length and the CLI embedding example against the embed reference (docs.ollama.com/api/embed) and the embeddings capability page. Removed the claim that the OpenAI-compatible `/v1/embeddings` endpoint is available (neither cited page says so). Noted that response durations are nanoseconds.

Method: documentation only; no commands were run.
