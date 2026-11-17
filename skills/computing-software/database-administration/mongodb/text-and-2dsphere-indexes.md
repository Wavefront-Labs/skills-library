---
id: computing-software.database-administration.mongodb.text-and-2dsphere-indexes
name: text-and-2dsphere-indexes
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, mongodb-indexes, text-index, 2dsphere, geospatial-query, near, geowithin, geojson, text-search, atlas-search]
level: practitioner
status: verified
description: "Use MongoDB text indexes for keyword search and 2dsphere indexes for GeoJSON proximity and polygon queries, and know when Atlas Search is the better tool."
sources:
  - https://www.mongodb.com/docs/manual/core/indexes/index-types/index-text/
  - https://www.mongodb.com/docs/manual/core/indexes/index-types/geospatial/2dsphere/
  - https://www.mongodb.com/docs/manual/reference/operator/query/near/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Text and 2dsphere indexes

**Goal:** basic full-text keyword search and location queries served from indexes.

## Text index
```javascript
db.articles.createIndex({ title: "text", body: "text" }, { weights: { title: 10, body: 1 }, default_language: "english", name: "article_text" })
db.articles.find({ $text: { $search: "replica \"write concern\" -arbiter" } },   // phrase, negation
                 { score: { $meta: "textScore" } }).sort({ score: { $meta: "textScore" } }).limit(20)
```
- One text index per collection (use a compound or wildcard `"$**": "text"` to cover many fields).
- Stemming and stop words per language; `language_override` field per document.
- A text index gives keyword search ranked with `weights`; for fuzzy matching or autocomplete see the Atlas Search documentation or a dedicated search engine.
- A `$text` query must use the text index; `hint` errors ("text and hint not allowed in same query") and combining with `$near`/`$geoNear` errors ("text and geoNear not allowed in same query").

## 2dsphere
Store GeoJSON with longitude first:
```javascript
db.places.insertOne({ name: "Depot", loc: { type: "Point", coordinates: [151.2093, -33.8688] } })
db.places.createIndex({ loc: "2dsphere", category: 1 })
// nearest within 2 km, sorted by distance
db.places.find({ loc: { $near: { $geometry: { type: "Point", coordinates: [151.21, -33.87] }, $maxDistance: 2000 } }, category: "cafe" })
// inside a polygon (no sort)
db.places.find({ loc: { $geoWithin: { $geometry: { type: "Polygon", coordinates: [[[151.1,-33.9],[151.3,-33.9],[151.3,-33.8],[151.1,-33.8],[151.1,-33.9]]] } } } })
// distance as a field in aggregation (must be first stage; `query` filters)
db.places.aggregate([ { $geoNear: { near: { type: "Point", coordinates: [151.21, -33.87] }, distanceField: "dist", maxDistance: 2000, query: { category: "cafe" } } } ])
```
Distances are metres on the sphere. `$centerSphere` takes radians (km / 6378.1).

## Gotchas
- Coordinates as `[lat, lng]` silently put points in the wrong place or fail validation (lat outside -90..90). Always `[lng, lat]`.
- Polygons must be closed (first = last point) and not self-intersecting; inserting an invalid geometry fails with `Could not extract geo keys at path ...` ("Loop is not closed", "Edges 0 and 2 cross").
- `$near` must be a top-level expression: inside `$or` it errors ("geo $near must be top-level expr"). A `.sort()` on another field is accepted and replaces the distance ordering.
- `$geoNear` must really be the first stage: a `$match` before it errors ("$geoNear was not the first stage in the pipeline after optimization"); use its `query` option instead.

## Verify
`explain()` shows `GEO_NEAR_2DSPHERE` / `TEXT_MATCH` stages; a known point returns with the expected distance.

## Checked
- MongoDB 9.0.4 Community and mongosh 2.13.0 on Windows, run in a scratch folder. Text index with weights built and `$text` with a phrase and `-arbiter` returned only "Replica set write concern" (score 18.75); a second text index on other fields is rejected; a `"$**": "text"` index built; explain shows `TEXT_MATCH`; `$text` without an index errors.
- 2dsphere: `$near` + `category` returned the nearby cafe with `GEO_NEAR_2DSPHERE`; `$geoWithin` polygon matched 2; `$geoNear` returned `dist` 148.4 m; `$centerSphere` with 2 / 6378.1 radians matched the two points within 2 km; `[lat, lng]` order errored (lng -33.87 lat 151.21 out of bounds); an open polygon and a self-intersecting polygon were rejected.
