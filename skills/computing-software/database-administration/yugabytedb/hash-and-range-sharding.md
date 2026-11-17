---
id: computing-software.database-administration.yugabytedb.hash-and-range-sharding
name: hash-and-range-sharding
category: computing-software
field: database-administration
product: yugabytedb
tags: [sharding, hash-sharding, range-sharding, tablets, presplit, docdb]
level: intro
status: docs-checked
description: "Choosing hash or range sharding in YugabyteDB, how hash codes map to tablets, and the cap on hash tablets per table that affects capacity planning."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/architecture/docdb-sharding/sharding.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/architecture/docdb-sharding/tablet-splitting.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hash and range sharding

A table is divided into tablets, and the sharding scheme decides how rows map to them.

**Hash sharding** hashes the leading key columns to a 16-bit value in the range 0x0000 to 0xFFFF. Each tablet owns a contiguous slice of that space, so there can be at most 64K hash tablets per table. It spreads data evenly and suits massively scalable workloads and point lookups, but range queries can be inefficient.

**Range sharding** keeps rows ordered by primary key and splits the key space at chosen boundaries. It suits range queries on primary key values, but starting with one tablet means one node takes all queries until splits happen, and globally ordered keys often create hot spots.

Operational consequences:
- Hash tables begin with a tablet count set by `--ysql_num_shards_per_tserver` for YSQL or `--yb_num_shards_per_tserver` for YCQL (default -1, so the system chooses from the CPU core count and whether automatic splitting is on) or an explicit `SPLIT INTO n TABLETS`.
- Range tables start as one tablet unless presplit with `SPLIT AT VALUES`, and are split dynamically as data grows. YCQL tables are hash sharded only.
- Each tablet replica costs CPU and memory on its tserver (about 0.4 vCPUs and 800 MiB per 1000 replicas, per the deployment checklist); see the tablet-replica-limits skill.

## Checked

2026-11-04. Confirmed against the Sharding page (hash space 0x0000 to 0xFFFF, at most 64K tablets, hash and range advantages and disadvantages, range tables start with one tablet, YCQL hash only), the Tablet splitting page (`SPLIT INTO n TABLETS`, `SPLIT AT VALUES` for range tables), the yb-tserver reference (`ysql_num_shards_per_tserver` and `yb_num_shards_per_tserver`, default -1) and the deployment checklist (per-replica overhead). Corrected the YSQL flag name (the skill named only the YCQL flag) and removed the unsupported 'changing the scheme means a new table' and 'last tablet hot-spots' claims.

Method: documentation only; no commands were run.
