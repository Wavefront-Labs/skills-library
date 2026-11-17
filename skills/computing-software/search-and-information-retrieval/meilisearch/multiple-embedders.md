---
id: computing-software.search-and-information-retrieval.meilisearch.multiple-embedders
name: multiple-embedders
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [multiple-embedders, hybrid-embedder-selection, image-embedder, meilisearch]
level: advanced
status: docs-checked
description: "Configure several named Meilisearch embedders on one index (text, image, fast and precise) and target one with hybrid.embedder, including federated use."
sources: ["https://www.meilisearch.com/docs/capabilities/hybrid_search/advanced/multiple_embedders"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multiple embedders on one index

Add several keys under the `embedders` setting; each is a named embedder with its own vectors, chosen per query with `hybrid.embedder`.

## Why

Text plus image search with different models, a large precise model alongside a small fast one for search-as-you-type, a small full-precision model next to a large binary-quantized one, a language-specific model with a multilingual fallback, or combining everything in federated search.

## Configure

PATCH `/indexes/products/settings/embedders` with a `text` embedder (`source: openAi`, `model: text-embedding-3-small`) and an `image` embedder (`source: rest`, a `url`, `indexingFragments`, `searchFragments`, `request` with `inputs` and `model`, and `response` mapping `embedding`).

## Query

- Text: `{"q": "comfortable running shoes", "hybrid": {"embedder": "text", "semanticRatio": 0.5}}`.
- Image: `{"media": {"image": "<image URL>"}, "hybrid": {"embedder": "image", "semanticRatio": 1.0}}`.

## Federation

In `/multi-search` with `"federation": {}`, send one query per mode, each with `federationOptions.weight`: full-text (`semanticRatio` 0.0, weight 1.0), semantic text (1.0, weight 0.8) and image (1.0, weight 0.5). Results merge into one ranked list.

## Costs

Each embedder stores its own vectors, so disk use and indexing time grow. Binary quantization can be applied per embedder, and composite embedders can use a local model for search and a cloud API for indexing.

## Checked

Method: docs-checked 2026-11-09 against the Multiple embedders page (raw mdx of github.com/meilisearch/documentation, read in full). All claims confirmed.
