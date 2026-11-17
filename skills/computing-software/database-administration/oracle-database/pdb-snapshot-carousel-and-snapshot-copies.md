---
id: computing-software.database-administration.oracle-database.pdb-snapshot-carousel-and-snapshot-copies
name: pdb-snapshot-carousel-and-snapshot-copies
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, multitenant, pluggable-database, pdb-snapshot, snapshot-carousel, snapshot-copy, test-environments]
level: advanced
status: docs-checked
description: "Use PDB snapshot carousel and snapshot copy clones in Oracle multitenant for fast test refreshes and point-in-time PDB copies, with licensing and storage caveats."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/multi/administering-pdb-snapshots.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/multi/cloning-a-pdb.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PDB snapshot carousel and snapshot copies

## Snapshot carousel
A library of point-in-time copies of a PDB, taken manually or every N minutes, kept up to
`MAX_PDB_SNAPSHOTS` (default 8, max 8). Uses: create a new PDB as of a snapshot time, or
recover data into a separate PDB. Check the Licensing Information guide for your platform before using it.

```sql
-- inside the PDB or with PDB name from root
ALTER PLUGGABLE DATABASE sales SNAPSHOT MODE EVERY 24 HOURS;     -- or MANUAL / NONE
ALTER PLUGGABLE DATABASE sales SET MAX_PDB_SNAPSHOTS = 6;        -- run in the PDB
ALTER PLUGGABLE DATABASE sales SNAPSHOT before_release_42;       -- manual named snapshot
SELECT con_name, snapshot_name, snapshot_scn, full_snapshot_path FROM dba_pdb_snapshots;
```
Create a PDB from a snapshot:
```sql
CREATE PLUGGABLE DATABASE sales_r41 FROM sales USING SNAPSHOT before_release_42;
-- or: USING SNAPSHOT AT SCN 123456789 / AT TIMESTAMP ...
```
Carousel snapshots are full clone PDBs; snapshot copy PDBs created from them are sparse.

## Snapshot copy clones
Thin clone sharing unchanged blocks with the source, ideal for many short-lived test PDBs:
```sql
ALTER SYSTEM SET clonedb = TRUE SCOPE=SPFILE;        -- see the Multitenant guide for when this is required
CREATE PLUGGABLE DATABASE dev01 FROM sales_master SNAPSHOT COPY;
```
- The source should be a read-only "master" PDB (refreshable clone or closed copy); while a
  snapshot copy exists, the source cannot be dropped or (depending on storage) opened read write.
- Storage: use a file system that supports sparse files, such as Oracle ACFS; with a network
  file system enable Direct NFS for the CDB.

## Typical test refresh workflow
1. Production -> refreshable clone `sales_master` (`REFRESH MODE EVERY 60 MINUTES`).
2. Close the refreshable clone at a consistent point.
3. `CREATE PLUGGABLE DATABASE devNN FROM sales_master SNAPSHOT COPY;` for each developer.
4. Mask PII in the master copy before cloning (Data Masking / scripts).

## Gotchas
- Snapshots are not backups: they live on the same storage; keep RMAN backups.
- Carousel snapshot creation needs local undo mode.

## Verify
`dba_pdb_snapshots` lists snapshots at the expected times; a PDB created from a snapshot
opens and contains data as of that SCN; `v$pdbs` shows snapshot-copy PDBs using little space.

## Checked

2026-10-28. Confirmed against the cited Oracle documentation: MAX_PDB_SNAPSHOTS (default 8, maximum 8), SNAPSHOT MODE EVERY, DBA_PDB_SNAPSHOTS, CREATE PLUGGABLE DATABASE ... USING SNAPSHOT, SNAPSHOT COPY, CLONEDB, ACFS and Direct NFS, local undo (Multitenant guide, administering PDB snapshots and cloning a PDB).

Removed or corrected: release and edition/licence statements, sparse-storage list, ASM claim, MAX_PDB_SNAPSHOTS = 0 behaviour and the archivelog requirement (not found in the cited pages).

Method: documentation only; no commands were run.
