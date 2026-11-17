---
id: computing-software.database-administration.mongodb.full-time-diagnostic-data-capture
name: full-time-diagnostic-data-capture
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, ftdc, diagnostic-data, mongodb-operations, mongodb-monitoring]
level: practitioner
status: docs-checked
description: "Use MongoDB FTDC diagnostic.data files: what they capture, retention settings, and how to decode and chart them when investigating a past incident."
sources:
  - https://www.mongodb.com/docs/manual/administration/full-time-diagnostic-data-capture/
  - https://www.mongodb.com/docs/manual/reference/parameters/#mongodb-parameter-param.diagnosticDataCollectionEnabled
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Full-time diagnostic data capture (FTDC)

**Goal:** answer "what happened at 03:12 last night?" even without a monitoring system: mongod and mongos run FTDC by default, sampling server statistics once per second into compressed files.

## What it collects
- Periodically: `serverStatus`, `replSetGetStatus` and `collStats` for `local.oplog.rs` (mongod only), `connPoolStats`, `getParameter`, `getClusterParameter`; at file rotation or startup also `getCmdLineOpts`, `buildInfo`, `hostInfo`.
- Depending on the OS: CPU, memory, performance-related disk utilisation (not capacity) and network statistics (metadata only). In containers the figures are relative to the container's limits.
- FTDC thread failures are fatal and stop the mongod or mongos process.

## Files
- mongod: `<dbPath>/diagnostic.data`. mongos: the log path with its extension removed plus `diagnostic.data` (for `/var/log/mongodb/mongos.log`, `/var/log/mongodb/mongos.diagnostic.data`).
- Files are compressed and not human-readable and inherit the data files' permissions. FTDC never contains query samples, predicates or results, data from user collections or indexes, or credentials and certificates. It does contain host information such as hostnames, OS information and startup options, so tell MongoDB engineers first if those are confidential.

## Settings
```javascript
db.adminCommand({ getParameter: 1, diagnosticDataCollectionDirectorySizeMB: 1, diagnosticDataCollectionPeriodMillis: 1 })
db.adminCommand({ setParameter: 1, diagnosticDataCollectionDirectorySizeMB: 1000 })
```
Defaults: capture every 1000 ms (`diagnosticDataCollectionPeriodMillis`), `diagnosticDataCollectionDirectorySizeMB` 500 (before 8.3: 250 MB, 500 MB on sharded clusters), `diagnosticDataCollectionFileSizeMB` 10, `diagnosticDataCollectionEnabled` true. The manual advises changing them only when MongoDB engineers ask; disabling FTDC (`diagnosticDataCollectionEnabled: false` in `setParameter`) is not recommended in production.

## Using the data
- Send `diagnostic.data` to MongoDB support; the source is in the `src/mongo/db/ftdc` directory of the mongodb/mongo repository.
- Copy the directory immediately after an incident: MongoDB deletes the oldest files as the folder nears its size limit.
- FTDC data exists only on the local host. Data forwarded by OTel or log shippers cannot be used for diagnosis, and ephemeral or rebuilt hosts lose it, so keep `diagnostic.data` on persistent storage or copy it off periodically.

## Typical incident questions FTDC answers
Anything exposed by the commands listed above over time: serverStatus counters and cache or queue metrics, replica set status, oplog collection statistics, connection pool statistics and host utilisation. Interpreting the files needs MongoDB's tooling or support.

## Verify
`ls -lh <dbPath>/diagnostic.data` shows recent files; their total stays below `diagnosticDataCollectionDirectorySizeMB` and the oldest covers your desired lookback.

## Checked

2026-10-25, against the MongoDB manual source (mongodb/docs repository, content/manual/manual, latest commit 2026-10-23). Confirmed: FTDC enabled by default, commands collected periodically and at rotation, diagnostic.data location for mongod and mongos, privacy statements (no query samples or user data or credentials; host info is included), thread failures are fatal, defaults (1 s period, 500 MB directory size from 8.3, previously 250 MB or 500 MB sharded, 10 MB file size), parameter names, disabling not recommended, older files deleted at the size limit, FTDC data not usable via OTel forwarding. Corrected the 200 MB default and removed unconfirmed file names and third-party decoder tools.

Method: documentation only; no commands were run.
