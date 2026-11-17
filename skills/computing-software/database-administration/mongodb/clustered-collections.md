---
id: computing-software.database-administration.mongodb.clustered-collections
name: clustered-collections
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, clustered-collection, clustered-index, mongodb-indexes, ttl]
level: practitioner
status: verified
description: "Create MongoDB clustered collections (5.3+) ordered by _id to speed range scans and TTL deletes, and know their restrictions versus a normal _id index."
sources:
  - https://www.mongodb.com/docs/manual/core/clustered-collections/
  - https://www.mongodb.com/docs/manual/reference/method/db.createCollection/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Clustered collections

**Goal:** store documents physically in `_id` order (like an index-organized table), saving the separate `_id` index and making `_id` range scans and TTL expiry cheaper.

## Create (only at creation time)
```javascript
db.createCollection("events", {
  clusteredIndex: { key: { _id: 1 }, unique: true, name: "events_clustered" },
  expireAfterSeconds: 60 * 60 * 24 * 30          // optional TTL; per the docs `_id` must be a supported date type for TTL
})
```
An existing collection cannot be converted; create a new clustered one and copy (`$out` / `$merge` or `mongodump`/`mongorestore`).

## Good fit
- Append-heavy data where `_id` is time-ordered (ObjectId or a date), queried by `_id` ranges. For TTL the docs require `_id` to be a supported date type, so an ObjectId alone will not expire; check the TTL page.
- TTL: per the docs a clustered index can eliminate the need for a secondary TTL index.
- Fewer indexes: the clustered key replaces the `_id` index (`getIndexes()` shows only `events_clustered`).

## Poor fit / limits
- Choose `_id` deliberately: it is the clustered key and cannot be changed later; read the Limitations section of the clustered-collections docs before using random or very large `_id` values.
- Key must be `{_id: 1}` and `unique: true` (other keys and `unique: false` are rejected).
- Not allowed on capped collections (the `size` option is rejected); the clustered index cannot be dropped or hidden, and `collMod` cannot add one to an existing collection.

## Query check
```javascript
db.events.find({ _id: { $gte: ObjectId.createFromTime(Date.now()/1000 - 3600) } }).explain()
```
Plan shows `CLUSTERED_IXSCAN` with `minRecord`/`maxRecord` bounds instead of `IXSCAN` + `FETCH`.

## Verify
`db.getCollectionInfos({name:"events"})[0].options.clusteredIndex` exists; `db.events.getIndexes()` lists the clustered index.

## Checked
- MongoDB 9.0.4 Community and mongosh 2.13.0 on Windows, run in a scratch folder. `createCollection` with `clusteredIndex` and `expireAfterSeconds` worked; `getIndexes()` lists `events_clustered` with `clustered: true` and no separate `_id_`; `getCollectionInfos(...).options.clusteredIndex` exists; an `_id` range query showed `CLUSTERED_IXSCAN` with `minRecord`.
- Rejected: capped with size, `unique: false`, key other than `_id`, `dropIndex`, `hideIndex`, `collMod clusteredIndex`; `expireAfterSeconds` without `clusteredIndex` is rejected too.
- Docs fetched: clustered collections page (TTL needs a date-type `_id`; may not be capped).
