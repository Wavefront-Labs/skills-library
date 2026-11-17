---
id: computing-software.data-engineering.apache-pinot.apache-pinot-dedup-config
name: apache-pinot-dedup-config
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, dedup, dedupconfig, dedupenabled, hashfunction, deduptimecolumn, metadatattl, preload, ignorenondefaulttiers, strictreplicagroup]
level: advanced
status: docs-checked
description: "Pinot realtime dedup: dedupConfig fields, metadata TTL, preload, and the partitioning and strictReplicaGroup routing prerequisites."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/build-with-pinot/ingestion/upsert-and-dedup/dedup.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dedup configuration

Dedup drops records whose primary key was already ingested, during real-time ingestion.
```
"dedupConfig": {
  "dedupEnabled": true,
  "hashFunction": "MD5",
  "dedupTimeColumn": "ts",
  "metadataTTL": 86400,
  "preload": "ENABLE",
  "ignoreNonDefaultTiers": "ENABLE"
}
```

- `hashFunction`: `NONE` (default), `MD5` or `MURMUR3`. The hash stores a 128-bit code instead of the key, useful for long keys; collisions are possible but very unlikely.
- `dedupTimeColumn` and `metadataTTL` expire old key metadata to bound JVM heap use. The TTL uses the time column's unit, which must be numeric.
- `preload` rebuilds key state from existing segments on restart, using `pinot.server.instance.max.segment.preload.threads` threads (default 0, which disables preload).

Prerequisites match upsert: stream partitioned by the primary key (schema `primaryKeyColumns`), `strictReplicaGroup` routing, and `numInstancesPerPartition=1` in the replica-group config.

Set the TTL long enough that new records are deduplicated before their keys are removed. Changing the primary key columns or `dedupTimeColumn` is not recommended.

## Checked

2026-11-09: confirmed against the Pinot Stream ingestion with Dedup page (pinot-docs build-with-pinot/ingestion/upsert-and-dedup/dedup.md): `primaryKeyColumns`, partitioning the stream by primary key, `strictReplicaGroup`, `numInstancesPerPartition` of 1, `hashFunction` values and default, `dedupTimeColumn` and `metadataTTL`, `preload` with the preload threads setting, and `ignoreNonDefaultTiers` accepting the string values. Removed the first-write-wins contrast with upsert, which the page does not state.

Method: documentation only; no commands were run.
