---
id: computing-software.search-and-information-retrieval.qdrant.discovery-api
name: discovery-api
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [discovery, context-pairs, target, context, explore-discovery]
level: advanced
status: docs-checked
description: "Steer search with a target and context pairs of positive and negative examples using the discovery API."
sources:
  - "https://qdrant.tech/documentation/search/explore/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Discovery (available as of v1.7) uses `context`, a set of positive-negative pairs. Each pair divides the space into a positive and a negative zone, and the search prefers points that lie in more positive zones. It is exposed through the Query API as the discover query.

```http
POST /collections/{collection_name}/points/query
{
  "query": {
    "discover": {
      "target": [0.2, 0.1, 0.9, 0.7],
      "context": [
        { "positive": 100, "negative": 718 },
        { "positive": 200, "negative": 300 }
      ]
    }
  },
  "limit": 10
}
```

Two kinds of search:

- Discovery search (target plus context) returns points more similar to the target but constrained by the context. The discovery score is the sigmoid of the target similarity plus the sum of per-pair ranks, so the number of positive zones a point is in dominates and closeness to the target comes second. It suits combining multimodal, vector-constrained searches, constraining the vector space the way filters constrain payload.
- Context search (context pairs only) returns points in the best zone. Its score is a triplet-loss style sum per pair, bounded between -1.0 and 0.0, where 0.0 is the best and many points can tie. Results are any points not closer to a negative example, giving a constrained, diverse set rather than a cluster around one point.

Notes from the docs:

- Examples can be point ids or raw vectors, and the arrangement of positives and negatives in pairs is up to you.
- Ids given as examples are excluded from the results.
- Scores are always descending (larger is better) regardless of the metric.
- Search time grows linearly with the number of examples.
- Because the space is hard-constrained, accuracy drops at default settings; the docs suggest raising the `ef` search parameter above 64 (for example `"params": { "ef": 128 }`) versus the default of 16.

## Checked

Method: docs-checked 2026-11-09 against the Qdrant Explore page (landing_page repo, search/explore.md, read in full) and its discovery-basic HTTP snippet. Removed the unconfirmed advice to prefer recommend for simple similarity and the iterative-UI framing; corrected the context-mode description and added the ef note.
