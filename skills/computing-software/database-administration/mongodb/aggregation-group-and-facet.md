---
id: computing-software.database-administration.mongodb.aggregation-group-and-facet
name: aggregation-group-and-facet
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, aggregation-pipeline, group-stage, facet-stage, accumulators, bucket-auto, sortbycount, faceted-search, mongosh]
level: practitioner
status: verified
description: "Summarise MongoDB data with $group accumulators and run several aggregations in one pass with $facet for faceted search, with memory limits in mind."
sources:
  - https://www.mongodb.com/docs/manual/reference/operator/aggregation/group/
  - https://www.mongodb.com/docs/manual/reference/operator/aggregation/facet/
  - https://www.mongodb.com/docs/manual/reference/operator/aggregation/bucketAuto/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# $group and $facet

**Goal:** produce totals, counts and faceted-search sidebars from a collection in one pipeline.

## $group
```javascript
db.orders.aggregate([
  { $match: { status: "paid", createdAt: { $gte: ISODate("2026-10-01") } } },   // filter first, uses an index
  { $group: {
      _id: { region: "$region", day: { $dateTrunc: { date: "$createdAt", unit: "day" } } },
      revenue: { $sum: "$total" },
      orders:  { $sum: 1 },
      avgBasket: { $avg: "$total" },
      customers: { $addToSet: "$customerId" },        // unbounded; watch memory
      lastOrder: { $max: "$createdAt" },
      top3: { $topN: { n: 3, sortBy: { total: -1 }, output: "$_id" } }
  } },
  { $sort: { "_id.day": 1 } }
])
```
- `_id: null` groups everything.
- `$first`/`$last` depend on input order: put a `$sort` before `$group`; with `$sort` on the group key + index, `$group` can use the DISTINCT_SCAN optimisation for `$first`.
- `$sortByCount: "$field"` = group + count + sort.

## $facet: several sub-pipelines over the same input
```javascript
db.products.aggregate([
  { $match: { $text: { $search: "laptop" } } },
  { $facet: {
      byBrand: [ { $sortByCount: "$brand" }, { $limit: 10 } ],
      byPrice: [ { $bucket: { groupBy: "$price", boundaries: [0, 500, 1000, 2000], default: "2000+" } } ],
      results: [ { $sort: { score: { $meta: "textScore" } } }, { $skip: 0 }, { $limit: 20 } ],
      total:   [ { $count: "n" } ]
  } }
])
```
`$bucketAuto: { groupBy: "$price", buckets: 5 }` picks boundaries itself.

## Limits
- `$group`, `$bucket` and `$bucketAuto` have a 100 MB RAM limit per stage and write temporary files when they exceed it (current docs; pass `allowDiskUse` explicitly to control it).
- `$facet` cannot spill: each stage inside it is limited to 100 MB and exceeding it raises `ExceededMemoryLimit`. Its output is ONE document and must stay under 16 MiB.
- `$facet` sub-pipelines cannot use indexes: explain shows each one fed by an `$internalFacetTeeConsumer` stage after the single cursor over the input. Do the `$match` (and `$text`) before `$facet`.
- `$addToSet`/`$push` arrays count toward memory and the 16 MB result doc.

## Verify
`db.orders.explain("executionStats").aggregate([...])` shows IXSCAN for the leading `$match` and `$group` results match a spot-check with `countDocuments`.

## Checked
- MongoDB 9.0.4 Community and mongosh 2.13.0 on Windows, run in a scratch folder. The `$group` pipeline (with `$dateTrunc`, `$addToSet`, `$max`, `$topN`), `$sortByCount` and the `$text` + `$facet` pipeline (with `$bucket` and `textScore` sort) all ran and returned the documented shapes.
- `$sort` on the group key plus a matching compound index gave `DISTINCT_SCAN` for `$first`; without the index the plan was `COLLSCAN` + `SORT` + `GROUP`.
- Docs fetched: `$facet` (100 MB per stage, cannot spill to disk, 16 MiB output) and `$group`/`$bucketAuto` (100 MB RAM then temp files). The unconfirmed "5.2+" and "default true from 6.0" claims were removed.
