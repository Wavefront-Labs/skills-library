---
id: computing-software.search-and-information-retrieval.meilisearch.binary-quantization
name: binary-quantization
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [binary-quantization, vector-compression, binary-quantized, meilisearch]
level: advanced
status: docs-checked
description: "Enable binaryQuantized on a Meilisearch embedder to cut vector storage to 1 bit per dimension; know when it pays off and that it is irreversible."
sources: ["https://www.meilisearch.com/docs/capabilities/hybrid_search/advanced/binary_quantization"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Binary quantization

Binary quantization (BQ) stores each embedding dimension as one bit instead of a 32-bit float, so a 1536-dimension vector shrinks from about 6 KB to 192 bytes, with faster indexing and approximate similarity. A large model with BQ often beats a small model at full precision; for example `text-embedding-3-large` (3072 dims) with BQ typically outperforms `text-embedding-3-small` at full precision while using less storage.

## When it fits

- More than 1M documents with embeddings.
- Models with 1400+ dimensions (more dimensions preserve more information).
- Disk, memory or indexing speed constraints.
Avoid it under 512 dimensions where quality loss is noticeable. Hybrid search softens the precision loss because keyword matching compensates.

## Enable it

PATCH `/indexes/<index>/settings/embedders` with, for example, `{"default": {"source": "openAi", "apiKey": "<OPEN_AI_API_KEY>", "model": "text-embedding-3-large", "binaryQuantized": true}}`. Setting just `{"default": {"binaryQuantized": true}}` also works on an existing embedder. It applies to any embedder source.

## Irreversible

Activating BQ converts all vectors and discards the full-precision originals. Recovering them requires re-indexing into a new embedder without BQ.

## Quality by dimensionality

1500+ dims: minimal loss. 512 to 1500: slight loss, acceptable. Under 512: not recommended (the docs mark `BAAI/bge-small-en-v1.5`, 384 dims, as not recommended).

## Checked

2026-11-03. Confirmed claim by claim against the Binary quantization page on the Meilisearch documentation site (names, defaults, limits, parameters and behaviours as stated in the skill). Removed: nothing; every concrete claim was found on the page.

Method: documentation only; no commands were run.
