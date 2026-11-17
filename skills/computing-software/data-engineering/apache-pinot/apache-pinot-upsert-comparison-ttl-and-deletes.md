---
id: computing-software.data-engineering.apache-pinot.apache-pinot-upsert-comparison-ttl-and-deletes
name: apache-pinot-upsert-comparison-ttl-and-deletes
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, upsert, comparisoncolumns, metadatattl, deleterecordcolumn, deletedkeysttl, consistencymode, snapshot, skipupsert, skipupsertview, dropoutoforderrecord, outoforderrecordcolumn]
level: advanced
status: docs-checked
description: "Pinot upsert controls: comparisonColumns, metadataTTL, soft deletes, deletedKeysTTL, consistencyMode, snapshots and out-of-order handling."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/build-with-pinot/ingestion/upsert-and-dedup/upsert.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upsert comparison columns, TTL and deletes

```
"upsertConfig": {
  "mode": "FULL",
  "comparisonColumns": ["updatedAt"],
  "deleteRecordColumn": "is_deleted",
  "deletedKeysTTL": 86400,
  "metadataTTL": 86400,
  "snapshot": "ENABLE"
}
```

- `comparisonColumns`: decides which version wins. By default Pinot uses the table time column. With several columns, **exactly one must be non-null per record** (more than one and the document is rejected), and a record is compared only against earlier records that used the same column. The older single `comparisonColumn` is deprecated.
- `deleteRecordColumn`: single-value BOOLEAN schema column marking a soft delete. A deleted key disappears from queries unless `skipUpsert=true`, and can be revived by a record with a higher comparison value. Treat it as immutable on an existing table.
- `deletedKeysTTL`: later reclaims metadata of deleted keys. Same unit as the comparison column.
- `metadataTTL`: expires primary-key metadata for old keys to bound heap memory. It is applied to the first comparison column and needs `snapshot` enabled.
- `metadataTTL` and `deletedKeysTTL` do not work with multiple comparison columns, and the comparison or time column must be NUMERIC.
- `snapshot: ENABLE` persists validDocIds snapshots so restarts recover faster; `preload: ENABLE` additionally needs the server config `pinot.server.instance.max.segment.preload.threads` set above 0.
- `consistencyMode`: `NONE` (default), `SYNC` (blocks upserts while queries run, adds write latency) or `SNAPSHOT` (queries use a snapshot; refresh interval `upsertViewRefreshIntervalMs`, default 3000 ms).

Out-of-order records:
- `dropOutOfOrderRecord: true` does not persist late records at all, so `skipUpsert` cannot show them. Default is `false`, where they are persisted but never referenced.
- `outOfOrderRecordColumn` names a boolean schema column that is set per record to flag late events.
- Both work only when `consistencyMode` is `NONE`.

Query options: `SET skipUpsert=true` reads every stored version. `skipUpsertView=true` bypasses the consistent view kept by SYNC or SNAPSHOT mode (a debugging aid, behaves as NONE).

## Checked

2026-11-09. Read the whole Pinot docs page `upsert.md`. Confirmed each bullet above against the sections on comparison column(s), metadata TTL, delete column, deleted-keys TTL, consistency modes, snapshots, preload and out-of-order handling. Corrected from the draft: the default ordering is the time column (not arrival order); skipUpsertView bypasses the consistent view; dropOutOfOrderRecord and outOfOrderRecordColumn require consistencyMode NONE, so the old combined example was invalid and was removed.
Method: documentation only; no commands were run.
