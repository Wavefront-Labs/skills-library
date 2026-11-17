---
id: computing-software.search-and-information-retrieval.qdrant.group-by
name: group-by
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [group-by, group-size, with-lookup, deduplicate, search-groups]
level: practitioner
status: docs-checked
description: "Group results by a payload field with group_by, group_size and with_lookup to avoid many hits from one source."
sources:
  - "https://qdrant.tech/documentation/search/search/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`query_groups` returns results grouped by a payload value, for example one best chunk per document.

```http
POST /collections/{collection_name}/points/query/groups
{
  "query": [1.1, 1.2],
  "group_by": "document_id",
  "limit": 4,
  "group_size": 2,
  "with_lookup": "documents"
}
```

Facts from the docs:

- Only keyword and integer payload values are supported for `group_by`; other types are ignored. Create a dedicated index on the field for performance. If the field is an array, a point can appear in several groups.
- `limit` is the number of groups; `group_size` is how many points per group. The group size is best-effort.
- `with_lookup` names another collection from which to look up and attach the point matching each group.

The docs' example uses it to get the best N points for each document when point payloads carry a document ID.

## Checked

2026-11-03. Confirmed on the Qdrant search page: the groups API for best N points per document, `group_by` and `group_size` (best-effort), keyword and integer values only, array fields, the index recommendation. Removed the unconfirmed `offset` restriction, the 'saving a second request' claim and generic troubleshooting.

Method: documentation only; no commands were run.
