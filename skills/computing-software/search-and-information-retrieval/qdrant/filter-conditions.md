---
id: computing-software.search-and-information-retrieval.qdrant.filter-conditions
name: filter-conditions
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [match, match-any, range, geo, values-count, filt-conditions]
level: practitioner
status: docs-checked
description: "Qdrant filter condition types: match, any, except, range, datetime range, geo shapes, values_count, is_empty, is_null, has_id, has_vector."
sources:
  - https://qdrant.tech/documentation/search/filtering/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Conditions available inside a filter clause:

- `match` with `value`: exact value for keyword, integer or bool.
- `match` with `any`: the stored value is one of the listed values (logical OR, like SQL IN).
- `match` with `except`: the stored value is none of the listed values (NOR, like NOT IN).
- `range` with `gt`, `gte`, `lt`, `lte`. A datetime range takes RFC 3339 strings (no need to convert to UNIX timestamps); timestamps are compared in UTC.
- `geo_bounding_box`, `geo_radius`, `geo_polygon`: location conditions. `radius` is in meters. For several stored locations, any matching includes the point.
- `values_count` with `gt`/`gte`/`lt`/`lte`: bounds on the number of values in a field; a non-array value counts as 1.
- `is_empty`: matches when the field does not exist or is null or `[]`. Combined with `must_not` it selects non-empty values.
- `is_null`: tests for a null value (not possible with `match`).
- `has_id`: point id is in the given list.
- `has_vector`: the point has the named vector (use the empty name `""` if the collection has no named vectors).
- `nested`: apply a filter to a single array element (see the nested index skill).

```json
{ "must": [
  { "key": "price", "range": { "gte": 10, "lt": 50 } },
  { "key": "location", "geo_radius": { "center": { "lon": 13.4, "lat": 52.5 }, "radius": 1000.0 } },
  { "key": "city", "match": { "any": ["Berlin", "Paris"] } }
] }
```

Use dot notation for nested keys (`country.name`) and `[]` to project array elements (`country.cities[].population`). When the stored value is an array, `any` is satisfied if at least one element is in the list, and `except` if at least one element is not in the list.

Substring match is computationally expensive and is rejected when strict mode is enabled (the default on Qdrant Cloud); prefer prefix or full-text match.

## Checked

2026-11-08. Confirmed against the Filtering page: match value/any/except semantics, range and datetime range, geo conditions and radius unit, values_count, is_empty/is_null, has_id, has_vector, key path syntax, substring-match note. Page read by section (clauses, match, range, geo, values count, empty/null, has id/vector); client-language tabs skipped. Corrected: `is_empty` also matches a missing field and null, not only an empty list. Removed: the claim that `any` "works naturally with tags" beyond the documented array behaviour.
Method: documentation only; no commands were run.
