---
id: computing-software.search-and-information-retrieval.qdrant.nested-payload-index
name: nested-payload-index
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [nested-index, nested-filter, arrays, objects, idx-nested]
level: advanced
status: docs-checked
description: "Filter arrays of objects element by element with a nested filter, and speed it up with per-element indexes using the nested parameter."
sources:
  - https://qdrant.tech/documentation/manage-data/indexing/
  - https://qdrant.tech/documentation/search/filtering/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

By default each condition of a filter is checked against the whole payload, so several conditions on fields inside one array can each match a different element. A nested object filter (available as of v1.2.0) requires a single element to satisfy all its conditions.

Payload:

```json
{ "id": 1, "diet": [ { "food": "leaves", "likes": false },
                     { "food": "meat", "likes": true } ] }
```

Filter (the `key` may be written `diet` or `diet[]`):

```json
{ "must": [ { "nested": { "key": "diet",
  "filter": { "must": [
    { "key": "food", "match": { "value": "meat" } },
    { "key": "likes", "match": { "value": true } } ] } } } ] }
```

A point matches if at least one element matches the whole nested filter.

Performance: regular payload indexes do not record which element a value belongs to, so they only narrow candidates and Qdrant then reads each candidate's payload to check the nested filter, which is slow when many candidates remain. Create per-element indexes by adding `nested` (the array key, `offers` or `offers[]`) to the index schema; every index type supports it:

```json
{ "field_name": "offers[].shop", "field_schema": { "type": "keyword", "nested": "offers" } }
```

If every condition in the nested filter is a match, range, geo, full-text, is_empty or is_null condition on a field with a per-element index of the same array, Qdrant answers from the indexes without reading payloads. If any condition is not covered, it reads payloads for the whole nested filter.

Constraints:

- `has_id` and `slice` conditions are not supported inside a nested filter; put them in an adjacent `must` clause.
- The indexed field must be inside the array elements (for example `offers[].price`).
- Only one array level: `nested` cannot point to an array inside another array such as `a[].b[]`.
- A per-element index cannot also be a tenant or principal index.
- Changing `nested` on an existing index rebuilds the index.
- Differences from a regular index outside nested filters: `is_empty` matches a point if any element lacks the field; a per-element full-text index treats each element as a separate document, so a full-text condition matches only if a single element matches it.

Paths: dot (`.`) steps into an object and `[]` into array elements, as in `country.cities[].population`.

## Checked

2026-11-08. Confirmed against the Indexing page (per-element index section: parameter, constraints, differences) and the Filtering page (Nested Key and Nested Object Filter sections: v1.2.0, semantics, performance, has_id and slice limitation). Not read in full: the full-text, HNSW and sparse sections of the Indexing page and the geo and datetime parts of Filtering. Corrected: the index is a normal field schema with a `nested` parameter, not a `nested` field type. Removed: the claim that unindexed nested filters scan payloads is now stated as the documented behaviour (read candidate payloads).
Method: documentation only; no commands were run.
