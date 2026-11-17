---
id: computing-software.search-and-information-retrieval.qdrant.vector-update-delete
name: vector-update-delete
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [update-vectors, delete-vectors, delete-points, filter, pts-delete]
level: practitioner
status: docs-checked
description: "Update or delete named vectors on existing points, and delete points by ID or by filter."
sources:
  - "https://qdrant.tech/documentation/manage-data/points/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Existing points can be changed without resending everything.

Update vectors only (payload is untouched):

```http
PUT /collections/{collection_name}/points/vectors
{ "points": [ { "id": 1, "vector": { "image": [0.2, 0.1] } } ] }
```

Delete one named vector from points:

```http
POST /collections/{collection_name}/points/vectors/delete
{ "points": [1, 2], "vector": ["image"] }
```

Delete points by id, or select them with a filter:

```http
POST /collections/{collection_name}/points/delete
{ "filter": { "must": [ { "key": "city", "match": { "value": "London" } } ] } }
```

With strict mode `unindexed_filtering_update` set to false, a filtered update such as delete by payload on an unindexed field is rejected.

## Checked

2026-11-03. Confirmed on the Qdrant points and configuration pages: the update-vectors and delete-vectors endpoints, delete by filter, and the `unindexed_filtering_update` strict-mode setting. Removed the unconfirmed write-ahead-log, vacuum and alias advice.

Method: documentation only; no commands were run.
