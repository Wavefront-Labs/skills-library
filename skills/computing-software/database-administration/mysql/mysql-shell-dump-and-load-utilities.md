---
id: computing-software.database-administration.mysql.mysql-shell-dump-and-load-utilities
name: mysql-shell-dump-and-load-utilities
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mysqlsh-dump, mysql-shell, util-dump-instance, util-load-dump, util-dump-schemas, parallel-logical-backup, heatwave-migration, ocimds]
level: practitioner
status: docs-checked
description: "Fast parallel logical backups and migrations with MySQL Shell util.dumpInstance/dumpSchemas/dumpTables and util.loadDump, including resume and compatibility options."
sources:
  - https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-shell-utilities-dump-instance-schema.html
  - https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-shell-utilities-load-dump.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MySQL Shell dump and load utilities

**Goal:** dump and reload hundreds of GB logically in parallel, with chunking, compression and restartable loads.

## Dump
```js
// mysqlsh root@db1:3306 --js
util.dumpInstance("/backup/2026-10-16", {
  threads: 8, compression: "zstd", bytesPerChunk: "128M",
  consistent: true,                       // FTWRL briefly, or LOCK INSTANCE FOR BACKUP, then per-thread snapshots
  excludeSchemas: ["scratch"], users: true
})
util.dumpSchemas(["app"], "/backup/app", { threads: 8 })
util.dumpTables("app", ["orders", "order_items"], "/backup/orders", { where: { orders: "created_at >= '2026-01-01'" } })
```
Writes data chunks, DDL and `@.json` metadata (including `gtidExecuted`); chunking is on by default, and with no primary key or unique index chunks are sized from row count, average row length and `bytesPerChunk`. `dryRun: true` checks first. Can write straight to object storage: S3-compatible (`s3BucketName`), Azure (`azureContainerName`) or OCI.

## Load
```js
util.loadDump("/backup/2026-10-16", {
  threads: 8, deferTableIndexes: "all",  // build secondary indexes after data: much faster
  ignoreVersion: true,                    // loading into a different major version
  loadUsers: true, skipBinlog: true,
  updateGtidSet: "replace"                // to seed a GTID replica
})
```
Progress is tracked in `load-progress.<server_uuid>.json` (or the file named by `progressFile`): the utility supports resume and reset, so rerun the same command after an interruption.

## Compatibility (moving to HeatWave/RDS etc.)
```js
util.dumpInstance("/b", { ocimds: true, compatibility: ["strip_definers", "strip_restricted_grants", "create_invisible_pks", "force_innodb"] })
```

## Gotchas
- `consistent: true` needs `RELOAD` (FTWRL) or `BACKUP_ADMIN` (`LOCK INSTANCE FOR BACKUP`); without it the dump is not a single point in time.
- For `ocimds: true` dumps, tables without a primary key are reported as errors; add primary keys on the source or use the `create_invisible_pks` compatibility modification.

## Verify
`util.loadDump` completes with 0 errors and row counts per table match the source; a test of resume (interrupt midway, rerun) completes.

## Checked
2026-11-01. Confirmed against the MySQL Shell manual pages Instance, Schema and Table Dump Utility and Dump Loading Utility (option names, compatibility values, chunking, consistent privileges, object storage options, progress file, resume and reset). Removed: the redo-log disable tip, the claim that tables without a primary key cannot be chunked, the claim about format readability, `resetProgress` (not confirmed). The pages served were the current Shell manual; confirm option availability on your Shell version.
Method: documentation only; no commands were run.
