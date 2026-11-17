---
id: computing-software.search-and-information-retrieval.qdrant.inference-server-side
name: inference-server-side
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [inference, embeddings, inference-objects]
level: advanced
status: docs-checked
description: "Let Qdrant create embeddings from Inference Objects (Document, Image) instead of sending precomputed vectors."
sources:
  - "https://qdrant.tech/documentation/inference/inference-api/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

With Qdrant Cloud Inference or Qdrant's BM25 model, embeddings are generated server-side. Instead of precomputed vectors you pass Inference Objects when ingesting or querying; each holds the input plus the model to use.

Object types:

- `Document` for text: `text`, `model`, and optional `options` (extra model parameters).
- `Image` for image input: `image` (a URL or base64 string), `model`, and optional `options`.
- `Object` is reserved for other input types that may come later.

```js
// Document
{ text: "Your text", model: "<the-model-to-use>", options: {} }
```

Use an Inference Object wherever a query vector or point vector would go. Qdrant creates the vector with the configured model and then runs the search, all within a low-latency network. Using the same model for ingest and query keeps vectors comparable.

Notes from the docs:

- At ingest time the input used for inference is not stored. To keep the text, add it to the payload explicitly.
- A single request can run several inference operations across hosts, for example image embeddings from `jina-clip-v2` (hosted by Jina AI), text embeddings from `all-minilm-l6-v2` (hosted by Qdrant Cloud) and BM25 executed locally by the cluster, producing three named vectors for one point.
- If a request contains several identical Inference Objects, the embeddings are generated once and reused, which cuts latency and cost with external providers.

## Checked

Method: docs-checked 2026-11-09 against the Qdrant Inference API page (landing_page repo, inference/inference-api.md), read in full; code snippets are Hugo includes and were not read. Removed the unconfirmed upsert JSON example and model name, the FastEmbed section, the vector-size matching claim and the model record-keeping advice. Dropped the fastembed tag.
