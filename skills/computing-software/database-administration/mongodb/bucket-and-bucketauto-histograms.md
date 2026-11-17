---
id: computing-software.database-administration.mongodb.bucket-and-bucketauto-histograms
name: bucket-and-bucketauto-histograms
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, mongodb-aggregation, bucket-stage, bucketauto, histogram, aggregation-pipeline]
level: practitioner
status: verified
description: "Build histograms and range reports in MongoDB with $bucket (fixed boundaries) and $bucketAuto (even-sized groups), including default buckets and granularity."
sources:
  - https://www.mongodb.com/docs/manual/reference/operator/aggregation/bucket/
  - https://www.mongodb.com/docs/manual/reference/operator/aggregation/bucketAuto/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# $bucket and $bucketAuto histograms

**Goal:** turn a numeric or date field into ranges (price bands, age groups, latency histograms) in one pipeline stage.

## $bucket: you choose the boundaries
```javascript
db.orders.aggregate([
  { $match: { status: "paid" } },
  { $bucket: {
      groupBy: "$total",
      boundaries: [0, 50, 100, 250, 1000],   // sorted, same BSON type; lower bound inclusive, upper exclusive
      default: "1000+",                        // REQUIRED if any value falls outside, else the stage errors
      output: { count: { $sum: 1 }, revenue: { $sum: "$total" }, avg: { $avg: "$total" } }
  } }
])
```
- `_id` of each bucket is its lower boundary (or the `default` literal).
- Empty buckets are **not** emitted; fill gaps client-side if a chart needs zeros, or use `$densify` on the output.
- Without `default`, a single out-of-range value fails the whole aggregation (`$switch could not find a matching branch`). A missing field falls into `default`, so keep `default` on real data.

## $bucketAuto: MongoDB chooses boundaries
```javascript
{ $bucketAuto: { groupBy: "$latencyMs", buckets: 10, granularity: "R20",
                 output: { n: { $sum: 1 } } } }
```
- Tries to put an equal number of documents in each bucket (quantile-like). Returns `_id: {min, max}`.
- `granularity` (`R5`, `R10`, `R20`, `R40`, `R80`, `1-2-5`, `E6`, `E12`, `E24`, `E48`, `E96`, `E192`, `POWERSOF2`) snaps edges to "nice" numbers; numeric values only (no NaN), and a negative value errors ("non-negative numbers only").
- Returns fewer buckets than asked when there are fewer distinct values (asking for 50 buckets over 20 distinct values returned 20) or the granularity is too coarse.

## Faceted histogram
Put several `$bucket` stages inside `$facet` to compute price and rating histograms in one pass over the `$match` result.

## Performance
Both stages are blocking group stages: they hold all groups in memory (100 MB RAM per stage; the docs say MongoDB writes temporary files when a stage exceeds it). Filter first with an indexed `$match`.

## Verify
- Sum of `count` across buckets equals `db.orders.countDocuments({status:"paid"})`.
- Spot-check boundary values (exactly 50 lands in the 50 bucket, not 0).

## Checked
- MongoDB 9.0.4 Community and mongosh 2.13.0 on Windows, run in a scratch folder. `$bucket` on 300 orders: boundary value 50 lands in bucket 50, bucket counts summed to `countDocuments` (225 = 225), empty buckets are not emitted, no `default` plus an out-of-range value errors, `default` absorbs a missing field.
- `$bucketAuto`: `R20` edges (0.9, 31.5, 63, 100, 140 ...), plain 5 buckets, negative values with `granularity` error, 20 distinct values with 50 buckets gives 20 buckets. `$densify` ran.
- Docs fetched: `$bucketAuto` page (granularity list R5, R10, R20, R40, R80, 1-2-5, E6 to E192, POWERSOF2; 100 MB limit then temp files; fewer buckets cases).
