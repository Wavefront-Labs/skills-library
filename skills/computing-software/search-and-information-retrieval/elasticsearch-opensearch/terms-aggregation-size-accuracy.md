---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.terms-aggregation-size-accuracy
name: terms-aggregation-size-accuracy
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, terms-aggregation-size-accuracy, es-aggs-bucket]
level: advanced
status: docs-checked
description: "Tune Elasticsearch terms aggregation size and shard_size, read sum_other_doc_count and doc_count_error_upper_bound, and avoid inaccurate orderings."
sources:
  - https://www.elastic.co/docs/reference/aggregations/search-aggregations-bucket-terms-aggregation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Terms aggregation size and accuracy (Elasticsearch)

**Goal:** correct top-N buckets.
- `{"aggs":{"top":{"terms":{"field":"brand","size":10,"shard_size":50}}}}`. Default `size` is 10, up to the `search.max_buckets` limit; a too-large `size` fails with a `max_buckets` message.
- Each shard returns its top `shard_size` terms, default `size * 1.5 + 10`. Raising `shard_size` is much cheaper than raising `size` but costs bytes over the wire and memory on the coordinating node. `shard_size` below `size` is reset to `size`.
- Counts can still be approximate even with a larger `shard_size`, and so can sub-aggregations. The guidance applies only to the default order (doc count, descending).
- `sum_other_doc_count` is the documents not in the returned top `size` terms; above 0 means buckets were discarded.
- `doc_count_error_upper_bound` appears per bucket only with `"show_term_doc_count_error": true`. It is the sum of the largest bucket on each shard that did not fit `shard_size`. It is -1 when ordered by a sub-aggregation or ascending count, and there is no error when ordered by `_key`.
- Order: avoid `"order": {"_count": "asc"}` (unbounded error; use `rare_terms`). Ordering by `_key` is safe. Ordering by a sub-aggregation is generally wrong, except max descending or min ascending. Pipeline aggregations cannot be used for ordering.
- `min_doc_count` is applied only after merging shard results, so frequent terms can go missing; raise `shard_size`. `shard_min_doc_count` prunes on the shard (keep it far below `min_doc_count` / number of shards).
- For more unique terms than you can return, use `composite`; for one huge request, split with `include` partitions (`partition`, `num_partitions`; cannot be combined with `exclude`).
- Text fields cannot be aggregated by default; use a keyword sub-field (fielddata is possible but can greatly increase memory).
- One terms aggregation cannot span several fields: use `copy_to`, `multi_terms` or a script. The last two disable the global ordinals optimization.
- `execution_hint`: `global_ordinals` (default for keyword) or `map` (only worth considering when very few documents match). Hints are ignored if not applicable, with no backward compatibility guarantee. `collect_mode` `breadth_first` defers child aggregations and is the default when cardinality exceeds `size` or is unknown.
- Mixed numeric types across indices promote integers to decimals and can lose precision.
- OpenSearch: not checked; the OpenSearch terms page was not used for these claims.

## Verify
- [ ] Compare top buckets from a one-shard index against the multi-shard index, with `show_term_doc_count_error` on.

## Checked
Checked 2026-11-08 against the Elasticsearch "Terms aggregation" page. Only Elasticsearch was checked. Removed: the claim that huge-cardinality fields use much heap through global ordinals (the page says global-ordinals memory is linear in the values in scope), and the unsourced suggestion that `execution_hint` fixes it.
Method: documentation only; no commands were run.
