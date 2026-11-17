---
id: computing-software.search-and-information-retrieval.qdrant.formula-rescoring
name: formula-rescoring
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [formula, score-boosting, decay, rescoring, rel-formula]
level: advanced
status: docs-checked
description: "Boost or reorder Qdrant results with a formula query using $score, payload values, conditions, defaults and decay functions (v1.14.0+)."
sources:
  - https://qdrant.tech/documentation/search/search-relevance/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Score boosting (available as of v1.14.0) lets the Query API rescore points with a custom `formula` over dynamic payload values, conditions and the scores of prefetches.

```json
{
  "prefetch": { "query": [0.2, 0.8], "limit": 50 },
  "query": {
    "formula": {
      "sum": [ "$score", { "mult": [ 0.5, "popularity" ] } ]
    },
    "defaults": { "popularity": 0 }
  },
  "limit": 10
}
```

Expressions the docs list:

- `$score` is the prefetch score (same as `$score[0]`); `$score[0]`, `$score[1]`, ... pick a specific prefetch when there are several.
- A plain string is a payload key (jsonpath style, `key` or `key.subkey`); Qdrant extracts a number from it.
- A filter condition becomes 1.0 if met and 0.0 otherwise (for example `{ "key": "tag", "match": { "any": ["h1", "h2"] } }`).
- Constants, `sum`, `mult`, `div`, `abs`, `pow`, `sqrt`, `log10`, `ln`, `exp`, `acosh`, geo distance (Haversine), `datetime` and `datetime key` (to POSIX seconds), `decay`; `max` and `min` need v1.19.1.
- Decay functions `lin_decay`, `exp_decay` and `gauss_decay` map a value `x` to a score between 0 and 1 using `target` (default 0.0), `scale` (default 1.0, in x units, non-zero positive) and `midpoint` (default 0.5, exclusive range 0 to 1): the output is `midpoint` when `x` equals `target` plus or minus `scale`. Typical uses are proximity and recency boosts.

Defaults: a mapping from variable to value used when a payload key or prefetch score is missing. Place `defaults` alongside `formula` (not inside it) and include the `$` in score keys such as `"$score[1]"`; otherwise Qdrant silently ignores them.

Considerations from the docs:

- Formula queries can only be used as a rescoring step, so they need a `prefetch`.
- Results sort in descending order; negate Euclidean scores so closest sorts first.
- Non-numeric values give an error. The page says both that a missing variable without a default is 0.0 and that it errors, so always supply defaults.
- With `max`/`min`, a point missing from a prefetch scores 0.0 and can win; set a default far outside the score range (for example -1e30 for `max`).
- Multiplication and division are lazily evaluated: a 0 stops the remaining operations.
- Create payload indexes on payload variables used in the formula for performance.

## Checked

2026-11-08. Confirmed against the Search Relevance page, Score Boosting section (formula example, expression list, defaults placement, considerations, max/min, decay parameters). Page read by section; MMR and relevance feedback sections and client-language tabs skipped. Corrected: decay functions are options of the `decay` expression with documented `target`/`scale`/`midpoint`, and `defaults` are keyed by variable. Removed: unsourced advice on prefetch limit sizing, and the claim that `$score` means "the current point" (it is the prefetch score).
Method: documentation only; no commands were run.
