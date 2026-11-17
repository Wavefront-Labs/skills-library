---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.field-boosting-and-query-boost
name: field-boosting-and-query-boost
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, field-boosting-and-query-boost, es-boosting]
level: practitioner
status: docs-checked
description: "Raise relevance with field^N boosts, per-query boost, and constant_score or dis_max wrappers."
sources:
  - https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-multi-match-query
  - https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-match-query
  - https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-constant-score-query
  - https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-dis-max-query
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Field and query boosts

**Goal:** order results by business importance of fields.
- `"fields":["title^3","body"]` in multi_match gives `title` a boost of 3 (the caret syntax is also used by query_string).
- Most multi_match types (best_fields, most_fields, phrase, phrase_prefix, cross_fields, bool_prefix) accept a query-level `boost`.
- `boost` is a float, default 1.0: values between 0 and 1.0 lower the score, above 1.0 raise it. To push documents down, see the boosting query skill rather than negative boosts.
- `cross_fields` is usually only useful on short string fields that all have boost 1; with other boosts, term statistics blending stops being meaningful.
- `constant_score` takes a required `filter` and an optional `boost` (default 1.0): every match gets exactly that score.
- `dis_max` takes `queries` and an optional `tie_breaker` (0 to 1.0, default 0.0): score is the best clause plus tie_breaker times the other matching clauses.
- Without `fields`, multi_match uses `index.query.default_field` (default `*`).
- Failure mode: stacking many boosts makes scores hard to reason about; document the intent and test with a judgement set.

## Verify
- [ ] `explain=true` shows the boost factor applied in the score tree.

## Checked
Date: 2026-11-08
Method: Read the Elasticsearch multi_match, match, constant_score and dis_max query pages in full; OpenSearch was not checked.
