---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.bm25-parameters-k1-b
name: bm25-parameters-k1-b
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, bm25-parameters-k1-b]
level: practitioner
status: docs-checked
description: "Set BM25 k1 and b per field with a custom similarity in index settings, and compare scores with explain and dfs_query_then_fetch."
sources:
  - https://www.elastic.co/docs/reference/elasticsearch/index-settings/similarity
  - https://docs.opensearch.org/latest/mappings/mapping-parameters/similarity/
  - https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tune BM25 parameters k1 and b

**Goal:** adjust term-frequency saturation and length normalisation for a corpus.
```
"settings":{"similarity":{"my_bm25":{"type":"BM25","k1":1.2,"b":0.75}}}
"mappings":{"properties":{"title":{"type":"text","similarity":"my_bm25"}}}
```
- Elasticsearch BM25 options: `k1` controls non-linear term frequency saturation (default 1.2); `b` controls to what degree document length normalizes tf values (default 0.75); `discount_overlaps` defaults to true.
- BM25 is the default similarity in both products. Elasticsearch calls custom similarities an expert feature. Similarity applies to `text` and `keyword` fields.
- Only the Elasticsearch page documents the `k1`, `b` and `discount_overlaps` options; the OpenSearch page cited confirms BM25 as default and that other similarities (DFR, DFI, IB, LM Dirichlet, LM Jelinek Mercer, scripted) are defined in index settings first.
- Scores are shard-local by default: `query_then_fetch` uses local term and document frequencies for the shard (faster, less accurate); `search_type=dfs_query_then_fetch` uses global frequencies across all shards (slower, more accurate).

## Verify
- [ ] Compare ranking with different `b` values on a short and a long document using `?explain=true` on the search request.

## Checked
Date: 2026-11-07
- Elasticsearch similarity settings page, read in full: BM25 (default) options and defaults, `PUT` settings plus mapping `similarity` example, `explain=true` search example.
- OpenSearch similarity mapping parameter page, read from the start through the example: BM25 default and the list of supported types.
- Elasticsearch search API page: searched for `search_type`; confirmed `query_then_fetch` and `dfs_query_then_fetch` wording. OpenSearch search page: searched, same two values and wording.
- Removed: "default since 5.0", the claim that tiny indices with many shards give unstable scores, the lower-b and higher-k1 effect sentences (replaced by the page's wording), and the Lucene docs source.
Method: documentation only; no commands were run.
