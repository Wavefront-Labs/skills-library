---
id: computing-software.database-administration.mongodb.array-expressions-map-filter-reduce
name: array-expressions-map-filter-reduce
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, mongodb-aggregation, filter-expression, map-expression, reduce-expression, array-operators]
level: practitioner
status: verified
description: "Transform arrays inside MongoDB documents without $unwind using $filter, $map, $reduce and related operators, with patterns and performance notes."
sources:
  - https://www.mongodb.com/docs/manual/reference/operator/aggregation/filter/
  - https://www.mongodb.com/docs/manual/reference/operator/aggregation/map/
  - https://www.mongodb.com/docs/manual/reference/operator/aggregation/reduce/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Array expressions: $filter, $map, $reduce

**Goal:** compute over embedded arrays per document. `$unwind` + `$group` multiplies documents and is far slower when the answer stays per-document.

## $filter: keep matching elements
```javascript
{ $project: { openItems: { $filter: {
    input: "$items", as: "it",
    cond: { $eq: ["$$it.status", "open"] },
    limit: 5                      // stop after N matches (1 or more)
} } } }
```

## $map: transform each element
```javascript
{ $set: { items: { $map: { input: "$items", as: "it",
    in: { $mergeObjects: ["$$it", { lineTotal: { $multiply: ["$$it.qty", "$$it.price"] } }] } } } } }
```

## $reduce: fold to one value
```javascript
{ $set: { orderTotal: { $reduce: { input: "$items", initialValue: 0,
    in: { $add: ["$$value", { $multiply: ["$$this.qty", "$$this.price"] }] } } } } }
```
`$$value` is the accumulator, `$$this` the current element. For simple sums prefer `{ $sum: "$items.price" }` (arrays of a path resolve to an array, and `$sum` adds it) — shorter and faster.

## Companions
| Need | Operator |
|---|---|
| Size | `$size` (errors on missing field: wrap `{ $ifNull: ["$items", []] }`) |
| Element at index | `$arrayElemAt`, `$first`, `$last` |
| Sort array in place | `$sortArray` (New in 5.2) |
| Top N inside array | `$firstN`, `$maxN` |
| Membership | `$in` (expression form) |
| Zip / index | `$zip`, `$range` + `$map` |
| Array to object | `$arrayToObject`, `$objectToArray` |

## Gotchas
- `$size` on a missing or non-array field throws; guard with `$ifNull` or `$isArray`.
- Variable names in `as` must start with a lowercase letter (an uppercase name is rejected: "starts with an invalid character for a user variable name"); reference with `$$`.
- These run after documents are fetched; to *select* documents by array content use `$elemMatch` in `$match` so a multikey index helps.
- Writes: the same expressions work in update pipelines (`updateMany({}, [ { $set: ... } ])`).

## Verify
Run on one document with `$match: {_id: ...}` and compare to a hand calculation before running over the collection.

## Checked
- MongoDB 9.0.4 Community and mongosh 2.13.0 on Windows, run in a scratch folder. `$filter` (with `limit`), `$map` with `$mergeObjects`, `$reduce` (23 for the sample items) and `{ $sum: "$items.price" }` (16) all ran and matched hand calculation; `$sortArray`, `$firstN`, `$maxN` ran; an update pipeline with `$size` ran.
- `$size` on a missing field errors ("must be an array, but was of type: missing"); `$ifNull` guard returns 0. An `as` of `It` was rejected.
- Docs fetched: `$sortArray` page (New in version 5.2) and `$filter` (limit must be at least 1). The 5.2 gates on `limit`, `$firstN` and `$maxN` could not be confirmed and were removed.
