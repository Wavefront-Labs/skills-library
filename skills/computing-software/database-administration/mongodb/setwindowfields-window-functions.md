---
id: computing-software.database-administration.mongodb.setwindowfields-window-functions
name: setwindowfields-window-functions
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, aggregation-pipeline, setwindowfields, window-functions, running-total, moving-average, rank, shift, time-series-analytics]
level: practitioner
status: verified
description: "Compute running totals, moving averages, ranks and previous-row deltas in MongoDB with $setWindowFields, including window bounds and memory limits."
sources:
  - https://www.mongodb.com/docs/manual/reference/operator/aggregation/setWindowFields/
  - https://www.mongodb.com/docs/manual/reference/operator/aggregation/shift/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# $setWindowFields

**Goal:** SQL-style window functions over MongoDB documents without client-side loops.

## Shape
```javascript
db.sensor.aggregate([
  { $match: { deviceId: "d-17", ts: { $gte: ISODate("2026-10-01") } } },
  { $setWindowFields: {
      partitionBy: "$deviceId",
      sortBy: { ts: 1 },
      output: {
        runningKwh: { $sum: "$kwh", window: { documents: ["unbounded", "current"] } },
        avg1h:      { $avg: "$temp", window: { range: [-1, 0], unit: "hour" } },     // time-based
        prevTemp:   { $shift: { output: "$temp", by: -1, default: null } },
        rankByTemp: { $denseRank: {} },                                            // rank by sortBy
        rowNo:      { $documentNumber: {} }
      }
  } },
  { $set: { delta: { $subtract: ["$temp", "$prevTemp"] } } }
])
```

## Windows
- `documents: [lower, upper]`: row offsets; `"unbounded"`, `"current"`, integers.
- `range: [lower, upper]` with `unit` (`second`..`year`) for dates, or numeric ranges on a numeric `sortBy` field. Range windows require a single sortBy field.
- No window = whole partition (e.g. `$sum` for partition total).

## Operators
Accumulators (`$sum`, `$avg`, `$min`, `$max`, `$count`, `$push`, `$stdDevPop`, `$first`, `$last`, `$topN`), plus window-only `$rank`, `$denseRank`, `$documentNumber`, `$shift`, `$derivative`, `$integral`, `$expMovingAvg`, `$covariancePop`, `$locf` (fill gaps) and `$linearFill`. `$derivative` needs explicit window bounds ("requires explicit window bounds").

## Top-N per group
```javascript
{ $setWindowFields: { partitionBy: "$category", sortBy: { sales: -1 }, output: { r: { $rank: {} } } } },
{ $match: { r: { $lte: 3 } } }
```

## Performance
- Index on `{ partitionBy, sortBy }` fields lets the preceding sort use it.
- 100 MB memory limit per stage; windows over `unbounded` partitions hold more; the pipeline ran with `allowDiskUse: true`.

## Gotchas
- `sortBy` is required for rank, shift, and document/range windows (errors: "Document-based bounds require a sortBy", "Range-based bounds require sortBy a single field").
- `$rank` needs a `sortBy` with exactly one field. Ties: `$rank` repeats the rank and then skips (a three-way tie at rank 3 appeared three times in a test), `$denseRank` does not skip, `$documentNumber` is unique but arbitrary among ties.

## Verify
Compare `runningKwh` for the last document of a partition to a `$group` `$sum` over the same filter.

## Checked
- MongoDB 9.0.4 Community and mongosh 2.13.0 on Windows, run in a scratch folder. The full example (running `$sum`, 1 hour `range` `$avg`, `$shift`, `$denseRank`, `$documentNumber`, then `$subtract`) ran on 12 sensor rows; the last `runningKwh` (78) equals a `$group` `$sum` (78).
- All listed accumulators (`$sum`, `$avg`, `$min`, `$max`, `$count`, `$push`, `$stdDevPop`, `$first`, `$last`, `$topN`) and window-only operators (`$rank`, `$denseRank`, `$documentNumber`, `$integral`, `$expMovingAvg`, `$covariancePop`, `$locf`, `$linearFill`) were accepted inside `$setWindowFields`; `$derivative` without a window errored.
- Error cases: `$rank` with no `sortBy`, range window with two sort fields, document window with no `sortBy`. Numeric `range: [-1, 0]` on a numeric `sortBy` worked. Top-3 per category via `$rank` + `$match` returned ties.
- Docs fetched: `$setWindowFields` page (New in version 5.0). The 5.2 and 5.3 gates for `$locf`/`$linearFill` were not confirmed and were removed.
