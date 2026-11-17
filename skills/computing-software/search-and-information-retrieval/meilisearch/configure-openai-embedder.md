---
id: computing-software.search-and-information-retrieval.meilisearch.configure-openai-embedder
name: configure-openai-embedder
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [openai-embedder, text-embedding-3, embedder-dimensions, meilisearch]
level: practitioner
status: docs-checked
description: "Set up the Meilisearch openAi embedder source, pick between text-embedding-3-small, large and ada-002, customize dimensions, and test with hybrid search."
sources: ["https://www.meilisearch.com/docs/capabilities/hybrid_search/how_to/configure_openai_embedder"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Configure the OpenAI embedder

Meilisearch has built-in support through `"source": "openAi"`.

## Models

| Model | Dimensions | Notes |
|---|---|---|
| `text-embedding-3-small` | 1,536 | cost-effective, good for most uses |
| `text-embedding-3-large` | 3,072 | higher accuracy for complex datasets |
| `text-embedding-ada-002` | 1,536 | legacy, still supported |

## Configure

PATCH `/indexes/<INDEX_NAME>/settings` with `{"embedders": {"my-openai": {"source": "openAi", "model": "text-embedding-3-small", "apiKey": "<OPEN_AI_API_KEY>", "documentTemplate": "A product named '{{doc.name}}' described as '{{doc.description}}'"}}}`. Meilisearch then embeds all documents; follow progress in the task queue.

## Dimensions

The 3-small and 3-large models accept a `dimensions` value, for example 512, to shrink vectors for lower storage and faster search at some accuracy cost; very low values can hurt quality.

## Operational notes

- Never commit the key; use environment variables or a secrets manager.
- Rate limits depend on the account tier. Free tiers can index slowly; Meilisearch retries automatically, but Tier 2 or higher is recommended in production.
- Test with `{"q": "something to stir soup with", "hybrid": {"semanticRatio": 0.5, "embedder": "my-openai"}}`; 0.5 balances keyword and semantic results.

## Checked

Method: docs-checked 2026-11-09 against the Configure OpenAI embedder page (raw mdx of github.com/meilisearch/documentation, read in full). All claims confirmed.
