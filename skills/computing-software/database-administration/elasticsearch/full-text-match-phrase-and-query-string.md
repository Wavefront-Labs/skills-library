---
id: computing-software.database-administration.elasticsearch.full-text-match-phrase-and-query-string
name: full-text-match-phrase-and-query-string
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, match-phrase, query-string-query, match-query, simple-query-string, elasticsearch-query-dsl]
level: practitioner
status: verified
description: "Choose and tune Elasticsearch full-text queries: match (operator, fuzziness), match_phrase (slop), multi_match, query_string vs simple_query_string for user input."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/full-text-queries.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query-phrase.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Full-text queries (match / match_phrase / query_string)

**Goal:** analysed-text search that behaves the way users expect and never 400s on odd input.

## match
```json
GET products/_search
{ "query": { "match": { "title": { "query": "wireless noise cancelling headphones",
    "operator": "and", "minimum_should_match": "75%", "fuzziness": "AUTO" } } } }
```
- Default `operator: or` returns anything with one term: high recall, often noisy. `and` or `minimum_should_match` tightens.
- `fuzziness: AUTO` tolerates typos: edit distance 0 for terms of 0-2 characters, 1 for 3-5, 2 for 6 or more (`AUTO:3,6` by default; `AUTO:low,high` overrides); costs CPU on large term dictionaries.

## match_phrase
```json
{ "match_phrase": { "title": { "query": "noise cancelling", "slop": 1 } } }
```
Terms in order and adjacent; `slop` allows gaps/transpositions. A swapped pair ("cancelling noise" for "noise cancelling") needs `slop: 2`; `slop: 1` does not match it. Needs positions indexed (default for `text`). `match_phrase_prefix` for search-as-you-type on small fields; prefer `search_as_you_type` fields or `completion` for real autocomplete.

## multi_match
`"type": "best_fields"` (default), `"most_fields"`, `"cross_fields"` (terms spread across first/last name), `"phrase"`; boost with `"fields": ["title^3", "body"]`.

## query_string vs simple_query_string
| query_string | simple_query_string |
|---|---|
| Full Lucene syntax: `title:(red AND shoe) -kids`, wildcards, regex | Limited syntax `+ - | " * ( )` |
| Throws parse errors on invalid syntax | Never errors; ignores invalid parts |
| For power users/internal tools | Safe for public search boxes |

Leading wildcards (`*phone`) in `query_string` scan the term dictionary: set `allow_leading_wildcard: false` for user-facing endpoints.

## Analysis matters
Results depend on the field's analyzer. Test with:
```json
GET products/_analyze { "field": "title", "text": "Noise-Cancelling Headphones" }
```
and use `"explain": true` or the `_explain` API to see scoring.

## Verify
Run a set of known queries with expected top results (a small relevance test list) after every mapping/analyzer change; the Ranking Evaluation API (`_rank_eval`) automates this.
