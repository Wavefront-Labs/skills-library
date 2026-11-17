---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.edge-ngram-autocomplete
name: edge-ngram-autocomplete
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, edge-ngram-autocomplete, es-tokenizers-filters]
level: advanced
status: docs-checked
description: "Build search-as-you-type matching with an edge_ngram tokenizer or filter, or the search_as_you_type field type."
sources:
  - https://www.elastic.co/docs/reference/text-analysis/analysis-edgengram-tokenizer
  - https://www.elastic.co/docs/reference/text-analysis/analysis-edgengram-tokenfilter
  - https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/search-as-you-type
  - https://www.elastic.co/docs/reference/text-analysis/analysis-ngram-tokenfilter
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Edge n-gram autocomplete

**Goal:** prefix matching on typing, with predictable index size.
```
"analysis":{"filter":{"ac":{"type":"edge_ngram","min_gram":2,"max_gram":15}},
 "analyzer":{"autocomplete":{"tokenizer":"standard","filter":["lowercase","ac"]},
  "ac_search":{"tokenizer":"standard","filter":["lowercase"]}}}
```
- Map field with `analyzer: autocomplete` and `search_analyzer: ac_search`. Use the n-gram analyzer at index time only: the usual advice to use the same analyzer at search time does not apply to edge n-grams.
- Always set `min_gram` and `max_gram` explicitly: the edge_ngram filter defaults to 1 and 1 (custom filter 1 and 2), which is not useful for autocomplete.
- Grams are capped at `max_gram`, so a longer search term can match nothing (with `max_gram` 3, "apple" does not match indexed "app"). A `truncate` filter in the search analyzer fixes that but can return irrelevant hits ("app" matches "apply"); test both.
- Simpler option: field type `search_as_you_type`, which creates `._2gram`, `._3gram` (`max_shingle_size` 2 to 4, default 3) and `._index_prefix` sub-fields. Query with `multi_match` of type `bool_prefix` over the field and its shingle sub-fields; use `match_phrase_prefix` if term order matters.
- Each gram length adds terms to the index, so keep the min/max range tight. The `ngram` filter (not edge) is additionally limited by `index.max_ngram_diff`.
- Failure mode: using the autocomplete analyzer at search time too, which n-grams the query.

## Verify
- [ ] Query `{"match":{"name":"qui"}}` returns the document "Quick Fox".
- [ ] `_analyze` with the field shows the expected grams.

## Checked
Date: 2026-11-08
Method: Read the Elasticsearch edge_ngram tokenizer, edge_ngram token filter, search_as_you_type and ngram filter pages in full; OpenSearch was not checked.
