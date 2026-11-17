---
id: computing-software.web-development.hasura.hasura-jsonb-and-text-search-operators
name: hasura-jsonb-and-text-search-operators
category: computing-software
field: web-development
product: hasura
tags: [hasura, queries, jsonb, text-search, operators, postgis, ltree]
level: practitioner
status: docs-checked
description: "Use Hasura Postgres filter operators for jsonb columns, pattern and regex text search, PostGIS spatial and ltree hierarchy matching in where clauses."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/queries/postgres/filters/jsonb-operators.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/queries/postgres/filters/text-search-operators.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/queries/postgres/filters/postgis-operators.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/queries/postgres/filters/ltree-operators.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/queries/postgres/filters/index.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick the right specialised operator.

JSONB operators (docs list): `_contains`, `_contained_in`, `_has_key`, `_has_keys_any`, `_has_keys_all`, `_jsonb_path_exists`, `_jsonb_path_match`. Example:

```graphql
query ($jsonFilter: jsonb) {
  authors(where: { address: { _contains: $jsonFilter } }) { id name }
}
```
Pass variables as JSON, e.g. {"jsonFilter": {"pincode": 560095}}.

Other jsonb shapes from the docs: `_has_key: "phone"`, `_has_keys_any: ["admin", "editor"]`, `_jsonb_path_exists: "$[*] ? (@.quantity > 5)"` and `_jsonb_path_match: "$.price < 50"` (JSONPath strings).

Text operators: `_like`, `_nlike`, `_ilike`, `_nilike`, `_similar`, `_nsimilar`, `_regex`, `_nregex`, `_iregex`, `_niregex`. Wildcards use SQL syntax such as `%amet%`. `_like`, `_similar` and `_regex` are case-sensitive; use `_ilike` and `_iregex` for case-insensitive matching. To match text inside a jsonb column, cast it with `_cast` (documented on the filters index page):

```graphql
authors(where: { address: { _cast: { String: { _ilike: "%bengaluru%" } } } })
```

PostGIS spatial operators for `geometry` columns: `_st_contains`, `_st_crosses`, `_st_equals`, `_st_intersects`, `_st_3d_intersects`, `_st_overlaps`, `_st_touches`, `_st_within`, `_st_d_within`, `_st_3d_d_within`. `_st_d_within` and `_st_intersects` also work on `geography` columns. `_st_d_within` takes `{distance: 3, from: $point}`. Raster columns have `_st_intersects_rast`, `_st_intersects_geom_nband` and `_st_intersects_nband_geom`.

ltree operators (for `ltree`, `lquery` and `ltxtquery` columns): `_ancestor`, `_ancestor_any`, `_matches` (for example `"*.Astronomy.*"`), `_matches_any`, `_descendant`, `_descendant_any`, `_matches_fulltext`. The API reference lists the Postgres equivalents of each group.

## Checked

2026-11-04. Confirmed against the cited pages: jsonb, text-search, postgis and ltree pages plus filters index for _cast: operator lists, example argument shapes, case sensitivity, geography support, raster operators. Removed or corrected: the partly-read self-correction gotcha and the Verify step; added the filters index page (where _cast is documented) to sources.

Method: documentation only; no commands were run.
