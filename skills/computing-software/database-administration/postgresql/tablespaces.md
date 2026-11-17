---
id: computing-software.database-administration.postgresql.tablespaces
name: tablespaces
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, managing-databases, postgres-tablespaces, tablespace, create-tablespace, alter-table-set-tablespace, temp-tablespaces, storage-layout]
level: practitioner
status: verified
description: "Decide when PostgreSQL tablespaces are worth it, create and move objects between them, and avoid the backup, replica and lock traps they bring."
sources:
  - https://www.postgresql.org/docs/current/manage-ag-tablespaces.html
  - https://www.postgresql.org/docs/current/sql-createtablespace.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tablespaces

**Goal:** use tablespaces only for a real storage reason (separate fast volume
for temp files, a huge cold table on cheap disk) and move data without surprises.

## When they help, when they do not
- Good: `temp_tablespaces` on local NVMe for big sorts/hashes; a separate volume
  when one filesystem cannot grow further.
- Not good: "performance" on a single RAID/SAN or cloud volume; tablespaces add
  operational complexity for no gain. They are not a quota or isolation mechanism.

## Create and use
First create the directory: it must exist (CREATE TABLESPACE will not create it), should be empty, be owned by the
PostgreSQL service user and be given as an absolute path.
```sql
CREATE TABLESPACE fast LOCATION '/mnt/fast/pg_tbs';
GRANT CREATE ON TABLESPACE fast TO app_owner;
CREATE TABLE events (...) TABLESPACE fast;
CREATE INDEX ... TABLESPACE fast;
ALTER DATABASE app SET temp_tablespaces = 'fast';
```
The directory is symlinked from `<datadir>/pg_tblspc/<oid>`.

## Moving objects
`ALTER TABLE big SET TABLESPACE cold;` rewrites the table under
`ACCESS EXCLUSIVE` lock: blocks reads and writes for the whole copy. For live
tables use `pg_repack --tablespace=cold --moveidx` or logical copy. Moving a
whole database: `ALTER DATABASE app SET TABLESPACE cold;` needs no connections.

## Gotchas
- Never put a tablespace on ephemeral storage such as a RAM disk: the docs warn the cluster "might become unreadable or unable to start".
  Tablespaces are part of the cluster and cannot be attached to a different one.
- A new tablespace is created on a standby at the same path as on the primary (via WAL), so the path must be creatable there; a standby on the same host
  as the primary collided with it and replay stopped (`could not rename file ... pg_filenode.map.tmp`). Use `pg_basebackup
  --tablespace-mapping=OLD=NEW` for the initial copy.
- Backups must include every tablespace; `pg_basebackup` handles them, homegrown
  rsync scripts often miss `pg_tblspc` targets.
- `DROP TABLESPACE` requires it empty in every database.

## Verify
```sql
SELECT spcname, pg_tablespace_location(oid), pg_size_pretty(pg_tablespace_size(oid)) FROM pg_tablespace;
SELECT c.relname, t.spcname FROM pg_class c JOIN pg_tablespace t ON t.oid = c.reltablespace WHERE c.reltablespace NOT IN (0, 1664);   -- 1664 = pg_global, shared catalogs
```

## Checked
- PostgreSQL 18.6 (Windows): `CREATE TABLESPACE` on an existing empty directory worked and `<datadir>/pg_tblspc/<oid>` was a link to it; `GRANT CREATE ON TABLESPACE`, `CREATE TABLE ... TABLESPACE`, `CREATE INDEX ... TABLESPACE`, `ALTER ROLE ... SET temp_tablespaces`, `ALTER DATABASE ... SET temp_tablespaces`, `ALTER TABLE ev SET TABLESPACE cold2` all ran; `DROP TABLESPACE cold2` failed `tablespace "cold2" is not empty` until the table moved back, then succeeded; `CREATE DATABASE ... TABLESPACE` followed by `ALTER DATABASE ... SET TABLESPACE pg_default` (no other connections) worked. The verify query `reltablespace <> 0` also listed dozens of shared system catalogs (tablespace 1664, pg_global), so it was changed. `pg_tablespace_location` and `pg_tablespace_size` ran. `pg_basebackup` copied both tablespaces (`2/2 tablespaces`) with `-T`. A standby on the same host replayed `CREATE TABLESPACE` at the same path and later failed on `ALTER DATABASE ... SET TABLESPACE` (`could not rename file "pg_tblspc/.../pg_filenode.map.tmp"`), which is the shared-path hazard described.
- Docs: sql-createtablespace (directory must exist, should be empty, owned by the PostgreSQL user, absolute), manage-ag-tablespaces (RAM disk warning, `pg_tblspc` symbolic links, tablespaces cannot be attached elsewhere), sql-altertable (ACCESS EXCLUSIVE unless noted), sql-droptablespace (must be empty), runtime-config-client (`temp_tablespaces`), pg_repack page (`-s/--tablespace`, `-S/--moveidx`; documented only, pg_repack was not run).
- The `mkdir`/`chown` commands were replaced by prose (Linux only, not run).
