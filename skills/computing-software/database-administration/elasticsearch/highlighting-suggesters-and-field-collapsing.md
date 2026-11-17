---
id: computing-software.database-administration.elasticsearch.highlighting-suggesters-and-field-collapsing
name: highlighting-suggesters-and-field-collapsing
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, highlighting, field-collapsing, suggesters, completion-suggester, elasticsearch-query-dsl]
level: practitioner
status: verified
description: "Add search-result highlighting, did-you-mean and autocomplete suggesters, and field collapsing (one result per group) to Elasticsearch queries, with performance options."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/highlighting.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/search-suggesters.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/collapse-search-results.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Highlighting, suggesters and field collapsing

## Highlighting
```json
GET articles/_search
{ "query": { "match": { "body": "index lifecycle" } },
  "highlight": { "pre_tags": ["<mark>"], "post_tags": ["</mark>"],
    "fields": { "body": { "fragment_size": 150, "number_of_fragments": 3 }, "title": { "number_of_fragments": 0 } } } }
```
Highlighter types: `unified` (default, BM25-aware), `plain` (small fields), `fvh` (needs `term_vector: with_positions_offsets`, fastest on large docs at index-size cost). Large fields: set `index_options: offsets` to avoid re-analysing text at query time; `max_analyzed_offset` caps work (default 1,000,000 chars).

## Suggesters
Term (did-you-mean per word) and phrase suggesters:
```json
"suggest": { "fix": { "text": "elastcsearch lifecyle", "term": { "field": "body", "suggest_mode": "popular" } } }
```
Completion suggester (autocomplete, in-memory FST, very fast):
```json
PUT products/_mapping { "properties": { "suggest": { "type": "completion" } } }
"suggest": { "ac": { "prefix": "wirel", "completion": { "field": "suggest", "size": 5, "skip_duplicates": true, "fuzzy": { "fuzziness": 1 } } } }
```
Completion matches prefixes only from the start of inputs; supply multiple `input` variants per doc. For infix/as-you-type matching use `search_as_you_type` fields.

## Field collapsing
One hit per group (best product per brand, latest event per host):
```json
GET products/_search
{ "query": { "match": { "title": "headphones" } },
  "collapse": { "field": "brand", "inner_hits": { "name": "top3", "size": 3, "sort": [ { "price": "asc" } ] } },
  "sort": [ "_score" ] }
```
- Collapse field must be a single-valued `keyword` or numeric with doc values.
- `hits.total` counts all matching docs, not groups; get group counts with a `cardinality` aggregation.
- Not combinable with `scroll` (400 "cannot use `collapse` in a scroll context"); `search_after` works only when the sort is on the collapse field alone (a two-field sort returned 400 on 9.5).

## Verify
Check highlights escape HTML (`"encoder": "html"`) before rendering; confirm collapsed results return one hit per brand.
