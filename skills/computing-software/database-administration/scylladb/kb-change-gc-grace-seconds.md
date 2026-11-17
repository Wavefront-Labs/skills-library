---
id: computing-software.database-administration.scylladb.kb-change-gc-grace-seconds
name: kb-change-gc-grace-seconds
category: computing-software
field: database-administration
product: scylladb
tags: [gc-grace-seconds, tombstones, data-resurrection, repair, alter-table]
level: advanced
status: docs-checked
description: "Safely change gc_grace_seconds on a ScyllaDB table: full repair, ALTER TABLE, check schema agreement with describecluster, repair each new window; consistency ALL alternative."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/kb/gc-grace-seconds.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Changing gc_grace_seconds safely

After changing `gc_grace_seconds` for a table, readjust the repair frequency so there is at least one successful full repair of the table in every new `gc_grace_seconds` window; otherwise deleted data can be resurrected.

Procedure:
1. Run a full repair of the table (for example with ScyllaDB Manager).
2. Change the value:
```
ALTER TABLE ks.tbl WITH gc_grace_seconds = 432000;
```
3. Check the schema is in sync: run `nodetool describecluster` from all nodes and confirm only a single schema version is reported (otherwise follow the schema mismatch troubleshooting guide).
4. Run at least one full repair during each new window. Example: with 10 days, repair every 8 to 9 days so repair always lands before the threshold.

Alternative that removes the repair requirement: make sure tombstones are created with consistency level `ALL`. Operations that generate tombstones are DELETEs, TTL expirations, and INSERT/UPDATE statements that overwrite a whole composite value such as a map, list or UDT.

Related: to purge many old tombstones from a large partition quickly, see the flush-old-tombstones workaround, which temporarily sets a small gc_grace_seconds right after a repair.

## Checked

2026-11-04. Confirmed against kb/gc-grace-seconds.rst: repair frequency requirement, procedure steps, describecluster check, the 10-day example and the consistency ALL alternative with its tombstone-generating operations. Removed the mechanism explanation the page does not give.

Method: documentation only; no commands were run.
