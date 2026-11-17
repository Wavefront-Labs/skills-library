---
id: computing-software.search-and-information-retrieval.qdrant.recommend-api
name: recommend-api
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [recommend, positive, negative, strategy, explore-recommend]
level: practitioner
status: docs-checked
description: "Recommend similar points from positive and negative examples, with strategies and cross-collection lookup."
sources:
  - "https://qdrant.tech/documentation/search/explore/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Recommendation searches from multiple positive and negative examples instead of one query vector. Examples can be point ids or, as of v1.6, raw vectors. It is exposed through the Query API as the recommend query.

```http
POST /collections/{collection_name}/points/query
{
  "query": {
    "recommend": {
      "positive": [100, 231],
      "negative": [718, [0.2, 0.3, 0.4, 0.5]],
      "strategy": "average_vector"
    }
  }
}
```

Strategies:

- `average_vector` is the default. It averages positives and negatives separately, then searches with `avg_positive + avg_positive - avg_negative` (just `avg_positive` with no negatives). Preprocessing is fast, so performance is on par with regular search.
- `best_score` (v1.6.0) scores each candidate against every example, takes the best positive and best negative score, and keeps the positive (sigmoid-normalised) when it beats the negative, otherwise a negative score. Cost grows linearly with the number of examples and accuracy may suffer; the docs suggest raising `ef` above 32 (for example `"params": { "ef": 64 }`) versus the default of 16.
- `sum_scores` sums scores against positives and subtracts those against negatives; the docs cite a paper using it for relevance feedback (nDCG@20 up 5.6 points with 2 to 8 positive documents).

Details:

- `best_score` and `sum_scores` allow negative-only queries, which find the most dissimilar vectors; combined with filtering this suits outlier finding and data cleaning.
- With multiple named vectors, `using` selects the vector (v0.10.0).
- `lookup_from` (v0.11.6) fetches the example vectors from another collection with the same dimensionality and distance, by id, then searches the current collection; useful for item-to-user recommendation. It takes `collection` and `vector`.
- The batch recommendation API (v0.10.0) returns one result array per request.

## Checked

Method: docs-checked 2026-11-09 against the Qdrant Explore page (landing_page repo, search/explore.md, read in full) and the basic-recommend and recommend-lookup-from HTTP snippets. Removed the unconfirmed "ids are excluded" claim for recommend (the page states it for discovery only) and the genre-clusters advice; added formulas, ef note and version gates.
