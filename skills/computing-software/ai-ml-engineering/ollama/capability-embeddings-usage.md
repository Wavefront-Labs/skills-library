---
id: computing-software.ai-ml-engineering.ollama.capability-embeddings-usage
name: capability-embeddings-usage
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [embeddings, vector-search, rag, cosine-similarity]
level: intro
status: docs-checked
description: "Generate normalised embeddings for semantic search and RAG, batch inputs and follow the page's consistency tips."
sources:
  - https://docs.ollama.com/capabilities/embeddings.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: build vectors for retrieval.

CLI: `ollama run embeddinggemma "Hello world"` or `echo "Hello world" | ollama run embeddinggemma`. Output is a JSON array.

API:

```
curl -X POST http://localhost:11434/api/embed -H "Content-Type: application/json" -d '{
  "model": "embeddinggemma",
  "input": "The quick brown fox jumps over the lazy dog."
}'
```

Python: `ollama.embed(model='embeddinggemma', input='...')` returns `embeddings`; `len(single['embeddings'][0])` is the vector length. JavaScript: `ollama.embed({ model, input })`.

Batch: pass an array of strings to `input` to get one vector per string in one call.

Facts from the page:

- Embeddings turn text into numeric vectors for a vector database, cosine-similarity search or RAG.
- Vector length depends on the model, typically 384 to 1024 dimensions.
- `/api/embed` returns L2-normalised (unit-length) vectors.

Tips:

- Use cosine similarity for most semantic search.
- Use the same embedding model for indexing and querying.

## Checked

Method: 2026-11-08 read the full embeddings capability page. All claims matched; removed the unsupported closing line about `truncate`, `dimensions` and `/v1/embeddings`.
