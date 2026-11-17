---
id: computing-software.search-and-information-retrieval.qdrant.mmr-diversity
name: mmr-diversity
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [mmr, diversity, candidates-limit, reranking, rel-mmr]
level: advanced
status: docs-checked
description: "Diversify results with maximal marginal relevance, setting diversity and candidates_limit."
sources:
  - "https://qdrant.tech/documentation/search/search-relevance/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Maximal marginal relevance (MMR) reorders candidates to balance relevance against variety, so results are not near duplicates.

```json
{
  "query": { "nearest": [0.2, 0.1],
             "mmr": { "diversity": 0.5, "candidates_limit": 100 } },
  "limit": 10
}
```

Parameters:

- `nearest`: the query vector.
- `diversity`: 0.0 is pure relevance, 1.0 is full diversity (lambda is 1 minus diversity).
- `candidates_limit`: the number of candidates to preselect before the diverse subset is chosen.

The docs say MMR excels when the dataset has many redundant or very similar points for a query. It selects iteratively, starting with the most relevant point, then each next point with the best combination of relevance and separation from those already selected.

## Checked

2026-11-03. Confirmed on the Qdrant search relevance page: MMR purpose and algorithm, `mmr` inside a `nearest` query, `diversity` range and meaning, `candidates_limit`. Removed unconfirmed sizing rules and generic usage advice.

Method: documentation only; no commands were run.
