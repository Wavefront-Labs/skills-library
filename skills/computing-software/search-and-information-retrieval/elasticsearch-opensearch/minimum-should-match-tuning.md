---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.minimum-should-match-tuning
name: minimum-should-match-tuning
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, minimum-should-match-tuning]
level: advanced
status: docs-checked
description: "Set minimum_should_match to require a number or percentage of should clauses and avoid zero-result or noisy queries."
sources:
  - https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-minimum-should-match
  - https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-bool-query
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# minimum_should_match in bool queries

**Goal:** predictable precision.
- `{"bool":{"should":[...4 clauses...],"minimum_should_match":"2<75%"}}` or an integer such as `2`.
- Accepted forms: integer (`3`), negative integer (`-2`), percentage (`75%`, rounded down), negative percentage (`-25%`), a conditional `3<90%` (all optional clauses required up to 3, the percentage above that) and several conditions separated by spaces (`2<-25% 9<-3`).
- In a `match` query it applies to the clauses generated from the analysed text.
- A computed value is never used if it is below 1 or above the number of optional clauses, so an oversized value does not make the query return nothing.
- `75%` and `-25%` differ for 5 clauses: `75%` requires 3, `-25%` requires 4.
- Raising the value makes a query stricter, lowering it more permissive.

## Verify
- [ ] Hit count does not rise as the value rises on a test query.

## Scope
The Elasticsearch reference pages were checked; OpenSearch behaviour was not.

## Checked

Checked 2026-11-02 against the Elasticsearch reference `minimum_should_match` page and the Boolean query page. Confirmed: all accepted forms, rounding, the 5-clause example, the clamping rule. Corrected: the earlier claim that a value larger than the number of clauses returns no hits is wrong, the page says such a value is never used (the maximum is the clause count).

Method: documentation only; no commands were run.
