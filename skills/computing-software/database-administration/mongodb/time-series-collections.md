---
id: computing-software.database-administration.mongodb.time-series-collections
name: time-series-collections
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, aggregation-pipeline, time-series-collection, timefield, metafield, granularity, iot]
level: practitioner
status: verified
description: "Create and run MongoDB time series collections: timeField/metaField design, granularity or bucket settings, expiry, secondary indexes, and query/update limits."
sources:
  - https://www.mongodb.com/docs/manual/core/timeseries-collections/
  - https://www.mongodb.com/docs/manual/core/timeseries/timeseries-best-practices/
  - https://www.mongodb.com/docs/manual/core/timeseries/timeseries-limitations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Time series collections

Time series collections store measurements in compressed internal **buckets** grouped
by `metaField` value and time range: far less storage and index size than one document per
reading in a normal collection.

## Create
```js
db.createCollection("sensor_readings", {
  timeseries: {
    timeField: "ts",            // required, BSON date
    metaField: "meta",          // identifies the series: { deviceId, site, type }
    granularity: "minutes"      // seconds | minutes | hours ("days" is rejected); match the ingest interval per series
    // or instead of granularity: bucketMaxSpanSeconds: 3600, bucketRoundingSeconds: 3600 (not together with granularity)
  },
  expireAfterSeconds: 60 * 60 * 24 * 90      // TTL: drop buckets older than 90 days
})
db.sensor_readings.insertMany([
  { ts: new Date(), meta: { deviceId: "d-17", site: "ams" }, temp: 21.4, rh: 48 }
])
```

## Design rules
- `metaField` = what rarely changes and identifies a series. Put all tags in one subdocument.
  Do **not** put unique-per-reading values there (each value creates its own buckets; no compression).
- `granularity` close to the interval between readings **of the same series**; too fine
  creates many small buckets, too coarse wastes work on queries.
- Insert in roughly time order per series; heavily out-of-order data opens many buckets.
- Unordered `insertMany` batches maximize throughput.

## Indexes
A compound index on `{ metaField, timeField }` is created automatically (docs: MongoDB 6.3 and later; `getIndexes()` showed `{meta: 1, ts: 1}`). Add secondary
indexes for common filters:
```js
db.sensor_readings.createIndex({ "meta.site": 1, ts: -1 })
db.sensor_readings.createIndex({ temp: 1 })            // measurement fields can be indexed
```

## Querying
Normal find/aggregate work; time-bounded queries on `ts` with `meta` filters prune buckets.
Useful stages: `$dateTrunc` for bucketing, `$setWindowFields` for moving averages,
`$densify`/`$fill` for gaps. Create downsampled rollups with `$merge` into another collection.

## Limitations to plan around
- Updates: the filter may only match the `metaField`, and the update must be multi (`updateMany`): on 9.0.4 an update filtering on `temp` failed with "Cannot perform an update or delete on a time-series collection when querying on a field that is not the metaField" and `updateOne` with "Cannot perform a non-multi update". A `deleteMany` filtering on a measurement field worked. Treat data as append-only.
- A normal collection cannot be converted in place (`collMod` with `timeseries` on a normal collection errors); copy with `$out` using its `timeseries` option (the output collection was created as type `timeseries`).
- Sharding: the docs deprecate shard keys that contain the `timeField` starting in 8.0 (use the `metaField`).
- Change streams are not supported (`watch()` errored; the limitations page says so). `$lookup` with a time series as the `from` collection ran. Check the limitations page for other restrictions on your version.

## Verify
`db.sensor_readings.stats()` (or `$collStats` with `storageStats`) shows `timeseries.bucketCount` and `avgNumMeasurementsPerCommit`; storage size is much smaller than an equivalent normal collection.

## Checked
- MongoDB 9.0.4 Community and mongosh 2.13.0 on Windows, run in a scratch folder. `createCollection` with `timeseries` + `expireAfterSeconds`, with `bucketMaxSpanSeconds`/`bucketRoundingSeconds`, and each `granularity` value (seconds, minutes, hours ok; days rejected; granularity plus a non-default bucketMaxSpanSeconds rejected). A non-date `ts` was rejected.
- 200 measurements inserted unordered; auto index `{meta: 1, ts: 1}`; secondary indexes on `meta.site, ts` and on `temp` built; `$collStats` storageStats and `stats()` expose `timeseries.bucketCount` and `avgNumMeasurementsPerCommit`. `$dateTrunc`, `$setWindowFields` and `$merge` into another collection ran. `collMod` changed granularity upward.
- Updates/deletes/change stream/convert behaviour as quoted above. Docs fetched: time-series overview (compound index "MongoDB 6.3 and later"; shard key with timeField deprecated in 8.0; updates match only metaField) and limitations pages.
