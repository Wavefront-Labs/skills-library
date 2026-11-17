---
id: computing-software.database-administration.mongodb.validating-collections
name: validating-collections
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, validate-collection, mongodb-operations, data-integrity, wiredtiger]
level: practitioner
status: gated
description: "Check MongoDB collections and indexes for structural corruption with validate, interpret results, and repair via resync or index rebuild rather than --repair."
sources:
  - https://www.mongodb.com/docs/manual/reference/command/validate/
  - https://www.mongodb.com/docs/manual/reference/method/db.collection.validate/
  - https://www.mongodb.com/docs/manual/tutorial/recover-data-following-unexpected-shutdown/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Validating collections

**Goal:** confirm data and index structures are consistent after a crash, disk error, or before trusting a restored backup.

## Run
```javascript
db.orders.validate()                       // default: checks structures and index consistency
db.orders.validate({ full: true })         // also WiredTiger verify; slower, takes exclusive lock
db.orders.validate({ background: true })   // errors on a standalone ("not supported in standalone mode"); replica set members only
```
Per the validate docs, foreground validate takes an exclusive `W` lock on the collection and blocks reads and writes (on a secondary it can block all other operations there); run it on a secondary taken out of rotation or during maintenance.

## All collections
```javascript
db.getMongo().getDBNames().forEach(d => db.getSiblingDB(d).getCollectionNames().forEach(c => {
  const r = db.getSiblingDB(d)[c].validate(); if (!r.valid) print(d, c, JSON.stringify(r.errors))
}))
```

## Read the result
- `valid: true/false`, `errors`, `warnings`.
- `nrecords` vs per-index `keysPerIndex` mismatches indicate index inconsistency.
- `corruptRecords` lists record ids that cannot be read.
- `extraIndexEntries` / `missingIndexEntries` (present in the 9.0.4 output).

## Fix
The remediation rows below were not exercised here (no corrupt data was created) (gated: unconfirmed, source is paywalled or blocked).

| Finding | Action |
|---|---|
| Index inconsistency only | Drop and rebuild the index (rolling per member) |
| Corrupt records on a replica set member | Resync the member (initial sync from healthy peers) |
| Standalone, no backup | `mongod --repair` as last resort: it discards unreadable data |
| Restored backup fails | Pick an older backup |

`validate` itself does not fix anything by default. The `fixMultikey` and `repair` options were accepted by 9.0.4 (`metadata: true` cannot be combined with other options); test them on a copy first.

## Verify
After remediation, run `validate()` again on the member and compare document counts against the primary (`countDocuments` with the same filter).

## Checked
- MongoDB 9.0.4 Community and mongosh 2.13.0 on Windows, run in a scratch folder. `validate()` on a 100-document collection with 5 indexes returned `valid: true`, `nrecords: 100`, `keysPerIndex`, `corruptRecords`, `extraIndexEntries`, `missingIndexEntries`, `errors`, `warnings`; `full: true` returned `valid: true` (with a transient-use warning); `background: true` errored on a standalone. The all-collections loop covered 61 namespaces with 0 invalid (views throw "is a view, not a collection" and need a try/catch).
- Option names `checkBSONConformance`, `fixMultikey`, `repair` ran. Docs fetched: validate command page (exclusive W lock). Corruption handling rows in the Fix table are procedures not exercised here (no corrupt data file was created).
