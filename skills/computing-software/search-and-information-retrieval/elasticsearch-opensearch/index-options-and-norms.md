---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.index-options-and-norms
name: index-options-and-norms
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, index-options-and-norms]
level: advanced
status: docs-checked
description: "Reduce index size or enable phrase/highlight support with index_options, norms and doc_values choices per field."
sources:
  - https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/index-options
  - https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/norms
  - https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/doc-values
  - https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/mapping-index
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# index_options, norms and scoring storage

**Goal:** only store what queries need.
- `"norms":false` drops the normalization factors used for scoring; norms cost about one byte per document per field (even for documents missing the field), so disable them on fields used only for filtering or aggregations.
- You cannot change `norms` on an existing field (update mapping rejects it). Either update the index template and roll over (only new backing indices change) or reindex into an index with `norms: false`.
- `index_options`, each level includes the previous: `docs` (term exists), `freqs` (adds term frequency for scoring), `positions` (default; adds positions for phrase and proximity queries), `offsets` (adds character offsets; speeds up the unified highlighter).
- `"index":false` (default true) builds no search structures. Numeric, date, boolean, ip, geo_point and keyword fields can still be queried through doc values, but by slow full scan; other types are not queryable.
- `doc_values` is on by default for supporting types (not by default for `text` and `match_only_text`). `"doc_values":false` saves disk but only if you never sort, aggregate or script on the field.
- Failure mode: `norms:false` or the `docs` option alters scoring, and `docs`/`freqs` break phrase queries.

## Verify
- [ ] Index size (`GET _cat/indices?v&h=index,store.size`) shrinks after the change and the expected queries still work.

## Checked
Date: 2026-11-08
Method: Read the Elasticsearch index_options, norms, doc_values and index mapping parameter pages in full; OpenSearch was not checked.
