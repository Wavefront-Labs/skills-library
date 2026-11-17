---
id: computing-software.database-administration.mongodb.unique-indexes-and-e11000
name: unique-indexes-and-e11000
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, unique-index-mongodb, e11000, duplicate-key, unique-index, mongodb-indexes]
level: practitioner
status: verified
description: "Create MongoDB unique indexes on existing data, find the duplicates blocking them, handle E11000 duplicate key errors, and use partial unique indexes for nullable fields."
sources:
  - https://www.mongodb.com/docs/manual/core/index-unique/
  - https://www.mongodb.com/docs/manual/core/index-partial/
  - https://www.mongodb.com/docs/manual/reference/error-codes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unique indexes and E11000

**Goal:** enforce uniqueness (email, external id) at the database, not in application checks that race.

## Create
```javascript
db.users.createIndex({ email: 1 }, { unique: true, collation: { locale: "en", strength: 2 } })
```
The collation makes uniqueness case-insensitive (`A@x.com` = `a@x.com`); queries must specify the same collation to use the index.

## The build fails on existing duplicates
Find them first:
```javascript
db.users.aggregate([
  { $group: { _id: { $toLower: "$email" }, ids: { $push: "$_id" }, n: { $sum: 1 } } },
  { $match: { n: { $gt: 1 } } }
], { allowDiskUse: true })
```
Merge or delete, then build. Under concurrent writes, new duplicates can appear during a long build. To convert an existing index without that race, use `collMod`:
```javascript
db.runCommand({ collMod: "users", index: { keyPattern: { email: 1 }, prepareUnique: true } })   // new duplicates now rejected
db.runCommand({ collMod: "users", index: { keyPattern: { email: 1 }, unique: true, dryRun: true } })   // optional check
db.runCommand({ collMod: "users", index: { keyPattern: { email: 1 }, unique: true } })
```
With existing duplicates the last step fails ("Please resolve conflicting documents"); without `prepareUnique` first it fails with "Cannot make index unique with 'prepareUnique=false'".

## Missing and null values
A unique index treats a missing field as `null`; only one document may lack the field. For optional fields use a partial index:
```javascript
db.users.createIndex({ taxId: 1 }, { unique: true, partialFilterExpression: { taxId: { $type: "string" } } })
```
(`sparse: true` also works for single fields but is the older, less flexible mechanism.)

## E11000 at runtime
```
E11000 duplicate key error collection: app.users index: email_1 dup key: { email: "a@x.com" }
```
Error code `11000` (`e.code` in mongosh). Handle it as a business error (409 Conflict), not a retry. For "create if absent" use `updateOne(filter, {$setOnInsert: ...}, {upsert: true})`; concurrent upserts can still raise E11000 on the loser; retry once in the app.

## Sharded collections
Unique indexes on sharded collections have restrictions; read the unique-index page (replica set and sharded builds) before relying on cross-shard uniqueness.

## Verify
`db.users.getIndexes()` shows `unique: true`; inserting a known duplicate returns E11000.

## Checked
- MongoDB 9.0.4 Community and mongosh 2.13.0 on Windows, run in a scratch folder. A unique index with `{locale:"en", strength:2}` failed to build over `A@x.com` + `a@x.com` with E11000; the `$group`/`$toLower` finder returned that pair; after deleting one the build succeeded and `B@X.com` was rejected as a duplicate of `b@x.com` (message names the collation); `e.code` was 11000.
- Missing field: second document without `taxId` raised `dup key: { taxId: null }`; a `$type: "string"` partial index and `sparse: true` both allowed 2 documents without it. `updateOne` with `$setOnInsert` + upsert: first call upserted 1, repeat 0.
- `collMod` flow: without `prepareUnique` the convert errors; after `prepareUnique: true` inserts and updates creating new duplicates fail with E11000; the convert fails while duplicates exist (also with `dryRun`) and succeeds after cleanup. `createIndex` with `prepareUnique` did not set the flag (not a createIndex option here).
- Docs fetched: unique-index page. The 4.2 build-failure, auto-retry and shard-key-prefix claims were not confirmed and were removed.
