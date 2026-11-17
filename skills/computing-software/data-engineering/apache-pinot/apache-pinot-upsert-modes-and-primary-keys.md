---
id: computing-software.data-engineering.apache-pinot.apache-pinot-upsert-modes-and-primary-keys
name: apache-pinot-upsert-modes-and-primary-keys
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, upsert, primarykeycolumns, full-upsert, partial-upsert, upsertconfig, strictreplicagroup, stream-partitioning]
level: advanced
status: docs-checked
description: "Enabling Pinot upsert: FULL, PARTIAL and NONE modes, primaryKeyColumns, stream partitioning by key and strictReplicaGroup routing."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/build-with-pinot/ingestion/upsert-and-dedup/upsert.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upsert modes and primary keys

Upsert keeps the latest row per primary key.

Schema (a list, because the key can be composite): `"primaryKeyColumns": ["orderId"]`.

Table config:
```
"upsertConfig": { "mode": "FULL" },
"routing": { "instanceSelectorType": "strictReplicaGroup" }
```

Modes:
- `FULL` (default): a new record replaces the older record with the same key completely. Supported on REALTIME, OFFLINE and HYBRID tables.
- `PARTIAL`: update only chosen columns, using `partialUpsertStrategies` (OVERWRITE, INCREMENT, APPEND, UNION, IGNORE, MAX, MIN, FORCE_OVERWRITE). **REALTIME tables only**, and null handling must be enabled (`tableIndexConfig.nullHandlingEnabled: true`). Columns without a strategy use `OVERWRITE`, changeable with `defaultPartialUpsertStrategy`.
- `NONE`: upsert is disabled.

When two records share a key, the one with the greater comparison value wins. The default comparison value is the table time column.

Hard requirements:
1. The input stream must be **partitioned by the primary key**. For Kafka the producer must set the message key. If the source is not partitioned, shuffle it first with a stream processor such as Flink.
2. Use `strictReplicaGroup` routing: all segments of one partition must be served from the same server.
3. If you also use `segmentPartitionConfig` for broker pruning, the partition function must match the producer's (Kafka Java client default is murmur2, other-language clients default to CRC32).
4. Do not enable adaptive server selection on upsert tables; it ignores `strictReplicaGroup` boundaries.
5. Use explicit partitioned replica-group instance assignment with `numInstancesPerPartition` set to `1`, so the partition-to-server mapping is persisted.

Gotchas:
- If the producer does not key by primary key, keys split across partitions and upsert yields duplicates.
- You cannot change the number of source partitions after the table is created, so start with enough (the page suggests at least 2-3 times the number of servers).
- `primaryKeyColumns`, `mode`, `hashFunction` and `comparisonColumns` are immutable after creation; to change them create a new table and reingest.
- Star-tree indexes cannot be used on upsert tables.

## Checked

2026-11-09. Read the whole Pinot docs page `upsert.md` (pinot-contrib/pinot-docs, branch latest). Confirmed: FULL default and the table-type support matrix, PARTIAL realtime-only with null handling required, the strategy list and default OVERWRITE, the stream-partitioning requirement and murmur2/CRC32 note, `strictReplicaGroup`, adaptive-selector warning, `numInstancesPerPartition` of 1, immutable fields, star-tree limitation, partition-count limitation. Changed: the draft's "segment assignment" requirement is now the documented explicit instance-assignment advice, and PARTIAL details were added.
Method: documentation only; no commands were run.
