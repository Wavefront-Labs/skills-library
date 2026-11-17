---
id: computing-software.search-and-information-retrieval.qdrant.full-text-bm25
name: full-text-bm25
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [full-text, bm25, scoring, inference, text-bm25]
level: advanced
status: docs-checked
description: "Rank documents by BM25 using a full-text index with scoring enabled or server-side BM25 inference."
sources:
  - "https://qdrant.tech/documentation/search/text-search/full-text-search/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Qdrant ranks by BM25 relevance from a full-text index on a payload field. The index holds what BM25 needs, including document length, so statistics come from your data.

Steps:

1. Create a full-text index on the field and set `scoring` to `true`. If points already hold the field, Qdrant builds the index from the stored payload without a re-upload.
2. Query with a text query on the indexed field. A point matches if its text contains at least one query term; points with none are not returned. Repeated query terms count once. To require or exclude terms, add a full-text filter.
3. A text query can also be a prefetch, for example to combine BM25 with dense vector search in hybrid search.

Tuning:

- `k` controls term frequency saturation (0 or greater, default 1.2). It is named `k`, not `k1`.
- `b` controls document length normalisation (0 to 1, default 0.75).
- Both are set per query, so no index rebuild is needed.
- Text processing (tokenizer, lowercasing, ASCII folding, stemming, stopwords) applies to both indexed and query text. The default is the `word` tokenizer and lowercasing, with no stemming or stopwords, so configure stemming and stopwords for your language to improve BM25 results.

Corpus statistics (document count, per-term document counts, average length) are computed over the shard being queried, so with several shards the same document can score slightly differently. After deletes or updates, statistics can include outdated data until the optimizer rebuilds segments, so scores may shift slightly; deleted points never appear. Per-tenant statistics are available through multitenancy settings.

For arrays of objects such as `reviews[].text`, set `nested` on the index to make a per-element index; each element then scores as its own document and a point takes its best element's score.

Migrating from the sparse vector BM25 model: create a scoring text index on the payload field, give it the same text processing (that model defaults to English stemming and stopwords, so set the `english` Snowball stemmer and `english` stopwords), then replace sparse queries with text queries. The index computes average document length, so `avg_len` is no longer needed and scores may differ. For learned sparse models such as SPLADE++ and miniCOIL use sparse vector search instead.

## Checked

Method: docs-checked 2026-11-09 against the Qdrant full-text search page (landing_page repo, search/text-search/full-text-search.md), read in full; code snippets are Hugo includes and were not readable. Removed the unconfirmed JSON index example, the inference-API BM25 route, the default-RRF fusion claim and the when-to-use list.
