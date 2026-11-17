---
id: computing-software.search-and-information-retrieval.meilisearch.ai-search-getting-started
name: ai-search-getting-started
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [hybrid-search, embedders, document-template, meilisearch]
level: practitioner
status: docs-checked
description: "Configure a first Meilisearch embedder (source, model, apiKey, documentTemplate) and run a hybrid search with semanticRatio and rankingScoreThreshold."
sources: ["https://www.meilisearch.com/docs/capabilities/hybrid_search/getting_started"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Getting started with AI-powered search

Embedders convert documents and queries into embeddings (vectors capturing meaning). Meilisearch generates and caches them automatically; only new or modified documents are re-embedded on later indexing.

## Build the embedder

Configure it in the `embedders` index setting (send it by updating the index settings). The key is the embedder name. Fields in the tutorial:

- `source`: `"openAi"` here; many other providers are supported.
- `model`: `text-embedding-3-small` (cost-effective) or `text-embedding-3-large` (more accurate, pricier).
- `apiKey`: your OpenAI key (any key tier works for the tutorial; use at least Tier 2 in production).
- `documentTemplate`: a Liquid template choosing what text is embedded, e.g. `An object used in a kitchen named '{{doc.name}}'`. Keep it short and use only semantically meaningful fields (a numeric `price` adds nothing).

## Search

Add both `q` and `hybrid` to a normal search request: `{"q": "plates for hot food", "hybrid": {"semanticRatio": 0.9, "embedder": "products-openai"}}`. Meilisearch runs keyword and semantic search and merges results with its scoring.

Semantic search can return weak matches when nothing fits. Add `rankingScoreThreshold` (0.0 returns everything, 1.0 only near-perfect matches); the docs suggest starting around 0.5 and adjusting.

## Checked

Method: docs-checked 2026-11-09 against the Getting started with AI-powered search page (raw mdx of github.com/meilisearch/documentation, read in full). Dropped the unconfirmed settings endpoint path.
