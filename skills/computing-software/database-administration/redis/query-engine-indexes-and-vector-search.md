---
id: computing-software.database-administration.redis.query-engine-indexes-and-vector-search
name: query-engine-indexes-and-vector-search
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, ft-create, redis-search, vector-search, redis-query-engine, redis-data-types]
level: practitioner
status: docs-checked
description: "Create Redis Query Engine indexes with FT.CREATE over hashes or JSON for text, tag, numeric and vector (KNN) search, and manage index memory and aliases."
sources:
  - https://redis.io/docs/latest/develop/interact/search-and-query/
  - https://redis.io/docs/latest/commands/ft.create/
  - https://redis.io/docs/latest/develop/interact/search-and-query/advanced-concepts/vectors/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Query engine indexes and vector search (FT.CREATE)

**Goal:** secondary indexes and full-text/vector search over Redis data. Built into Redis 8; RediSearch module (Redis Stack) on older versions.

## Create an index over hashes
```text
FT.CREATE idx:products ON HASH PREFIX 1 product: SCHEMA
  name TEXT WEIGHT 2.0
  brand TAG SORTABLE
  price NUMERIC SORTABLE
  embedding VECTOR HNSW 6 TYPE FLOAT32 DIM 384 DISTANCE_METRIC COSINE
```
Existing keys with the prefix are scanned and indexed (unless `SKIPINITIALSCAN` is given) and new matching keys are indexed automatically; `FT.INFO idx:products` shows `percent_indexed`.

## Query
```text
FT.SEARCH idx:products '@brand:{acme} @price:[10 50] lamp' SORTBY price ASC LIMIT 0 20 RETURN 2 name price
FT.AGGREGATE idx:products '*' GROUPBY 1 @brand REDUCE COUNT 0 AS n SORTBY 2 @n DESC
```
Vector KNN with pre-filter (DIALECT 2):
```text
FT.SEARCH idx:products '(@brand:{acme})=>[KNN 10 @embedding $vec AS score]' PARAMS 2 vec <float32 bytes> SORTBY score DIALECT 2
```

## Field types
| Type | Use |
|---|---|
| TEXT | tokenised, stemmed full text |
| TAG | exact values, comma-separated lists |
| NUMERIC | ranges, sorting |
| GEO / GEOSHAPE | points / polygons |
| VECTOR | `FLAT` or `HNSW` algorithm; needs `TYPE`, `DIM`, `DISTANCE_METRIC` |

## Operations
- Schema changes: `FT.ALTER idx SCHEMA ADD field TYPE` adds fields (the docs describe only adding); for other changes build a new index. Use `FT.ALIASADD`/`FT.ALIASUPDATE` to swap a rebuilt index in without app changes.
- Index memory: `FT.INFO` (`inverted_sz_mb`, `vector_index_sz_mb`); `M` and `EF_CONSTRUCTION` are HNSW tuning attributes.
- `FT.DROPINDEX idx` keeps documents; `DD` also deletes them.
- Cluster: search behaviour differs by edition and version, so check the query-engine documentation for your deployment (`FT.PROFILE` reports a coordinator section on multi-shard setups).

## Verify
`FT.INFO idx:products` shows `num_docs` equal to the expected key count and `hash_indexing_failures` 0; `FT.PROFILE` explains slow queries.

## Checked
Date: 2026-10-23. Documentation release: Redis documentation at redis.io/docs/latest and the redis/docs and redis/redis 8.2 repositories as read on 2026-10-23.
Confirmed from the command pages: FT.CREATE `ON HASH|JSON`, `PREFIX count prefix`, field types TEXT/TAG/NUMERIC/GEO/VECTOR/GEOSHAPE, `WEIGHT` default 1, SORTABLE, SKIPINITIALSCAN, vector queries need DIALECT 2 or later; vector schema `VECTOR HNSW 6 TYPE FLOAT32 DIM n DISTANCE_METRIC COSINE` (the count is the number of name and value tokens) and the KNN query form with PARAMS, AS and SORTBY; FT.DROPINDEX (documents kept unless DD); FT.ALTER SCHEMA ADD; FT.ALIASUPDATE; FT.INFO fields num_docs, percent_indexed, hash_indexing_failures, inverted_sz_mb, vector_index_sz_mb; FT.PROFILE syntax; Redis 8 builds in previously modular functionality. Removed unconfirmed: background initial indexing, FLAT/HNSW exact versus approximate wording, per-shard cluster claim.
Method: documentation only; no commands were run.
