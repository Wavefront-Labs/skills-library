---
id: computing-software.search-and-information-retrieval.qdrant.filter-clauses
name: filter-clauses
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [filtering, must, should, must-not, min-should, filt-clauses]
level: practitioner
status: docs-checked
description: "Combine conditions with must, should and must_not clauses in Qdrant filters, nest clauses, and use match any instead of repeated should."
sources:
  - https://qdrant.tech/documentation/search/filtering/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A filter combines conditions with clauses, which can be nested recursively to build any boolean expression.

```json
{ "filter": {
  "must":     [ { "key": "city", "match": { "value": "London" } } ],
  "should":   [ { "key": "color", "match": { "value": "red" } },
                { "key": "color", "match": { "value": "blue" } } ],
  "must_not": [ { "key": "banned", "match": { "value": true } } ]
} }
```

Clause meanings:

- `must`: true only if every listed condition holds (AND).
- `should`: true if at least one listed condition holds (OR).
- `must_not`: true if none of the listed conditions holds, equivalent to (NOT A) AND (NOT B) AND (NOT C).
- Several clauses in one filter are combined by AND.
- `min_should` also exists as a clause (the docs list it next to must, should and must_not); its parameters are not covered in the sections read, so look them up on the Filtering page before use.

Clauses nest, for example a `must_not` containing a `must`, so complex logic is possible.

Tip from the docs: if all conditions inside `should` target the same field, use `match` with `any` instead; it is faster, especially for many values.

## Checked

2026-11-08. Confirmed against the Filtering page: clause semantics for must, should and must_not, AND combination of clauses, nesting, the match-any tip. Page read by section; client-language tabs skipped. Removed unconfirmed claims: the `min_should` structure (`conditions`, `min_count`), the statement that filters apply during graph traversal, and that selective indexed filters stay fast.
Method: documentation only; no commands were run.
