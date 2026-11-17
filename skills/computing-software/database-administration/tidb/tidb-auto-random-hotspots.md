---
id: computing-software.database-administration.tidb.tidb-auto-random-hotspots
name: tidb-auto-random-hotspots
category: computing-software
field: database-administration
product: tidb
tags: [tidb, auto-random, write-hotspot, auto-increment, shard-bits, pre-split-regions, last-insert-id]
level: advanced
status: docs-checked
description: "Avoid single-node write hotspots with AUTO_RANDOM in TiDB: syntax, shard bits and range parameters, constraints and interaction with PRE_SPLIT_REGIONS."
sources: ["https://docs.pingcap.com/tidb/stable/auto-random"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tidb auto random hotspots

`AUTO_RANDOM` (since v3.1.0) is a column attribute that assigns random, unique values to a `BIGINT` column. It replaces `AUTO_INCREMENT` on primary keys to avoid the hotspot caused by consecutive IDs landing in one Region. The column must be in the primary key and be its first column.

```sql
CREATE TABLE t (a BIGINT PRIMARY KEY AUTO_RANDOM, b VARCHAR(255));
CREATE TABLE t (a BIGINT AUTO_RANDOM(6), b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a BIGINT AUTO_RANDOM(5, 54), b VARCHAR(255), PRIMARY KEY (a));
```

An explicit value on insert is stored as is (this requires `@@allow_auto_random_explicit_insert` set to 1, default 0); otherwise TiDB generates one. A comment form `/*T![auto_rand] AUTO_RANDOM */` is available.

`AUTO_RANDOM(S, R)` layout in 64 bits:
- `S` shard bits (1 to 15, default 5), derived from a hash of the transaction start time.
- `R` total length of the allocation range (32 to 64, default 64).
- Auto-increment bits are allocated sequentially and guarantee global uniqueness; they must be at least 27 bits (signed: `R-1-S >= 27`; unsigned: `R-S >= 27`).
- Implicit values are always positive; reserved bits `64-R` are zero.

Choosing S: more shard bits means fewer increment bits. Best practice is `log2(x)` where x is the number of storage nodes, for example 4 for 16 TiKV nodes. Choosing R: lower it when clients cannot represent full 64-bit integers; JSON numbers only hold `[-(2^53)+1, (2^53)-1]`, so use a smaller R for them.

`PRE_SPLIT_REGIONS` splits the table into `2^(PRE_SPLIT_REGIONS)` Regions at creation. Read the last implicit value with `SELECT last_insert_id()`; the shard bits appear in `SHOW CREATE TABLE` and in `TIDB_ROW_ID_SHARDING_INFO` (`PK_AUTO_RANDOM_BITS=x`).

## Checked

2026-11-04. Confirmed against the AUTO_RANDOM page: v3.1.0, syntax forms, S and R ranges and defaults, bit layout, the 27-bit rule, shard-bit and range guidance, PRE_SPLIT_REGIONS, last_insert_id and TIDB_ROW_ID_SHARDING_INFO. Added the explicit-insert variable from the page.
Method: documentation only; no commands were run.
