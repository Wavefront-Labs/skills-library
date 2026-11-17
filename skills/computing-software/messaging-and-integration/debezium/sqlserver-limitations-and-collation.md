---
id: computing-software.messaging-and-integration.debezium.sqlserver-limitations-and-collation
name: sqlserver-limitations-and-collation
category: computing-software
field: messaging-and-integration
product: debezium
tags: [sql-server, collation, incremental-snapshot, limitations]
level: advanced
status: docs-checked
description: "Avoid lost rows in SQL Server ad hoc snapshots with collation and sendStringParametersAsUnicode, and know connector limits."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/sqlserver.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Known limits of the SQL Server connector:

- Indexed (materialised) views are unsupported, because CDC needs a table as the base of a capture instance.
- Schema changes are unsupported while an incremental snapshot is running.
- CDC must be enabled per table, and the SQL Server Agent must run.

Collation caveat for ad hoc and incremental snapshots: some collation sets, such as `SQL_*`, have sorting rules that are not compatible with the Unicode sorting algorithm. The incompatible rules can lead to lost data when the connector runs an ad hoc snapshot. For example, when `sendStringParametersAsUnicode` is `true`, the connector can skip records during the snapshot.

Protect against it by turning the option off through the driver pass-through property:

```json
"driver.sendStringParametersAsUnicode": "false"
```

Other snapshot-adjacent properties:

- `streaming.delay.ms` (default `0`): delay before streaming starts after a snapshot completes. Setting a value higher than the offset flush interval prevents restarting the snapshot if a failure hits right after it ends.
- `data.query.mode` (default `direct`): `direct` queries change tables directly; `function` calls `cdc.[fn_cdc_get_all_changes_#]`.
- `source.struct.version` (default `v2`): `v1` restores the old source block but is slated for removal.

Check: run an ad hoc snapshot on a test table with string keys and compare row counts with the source.

## Checked

2026-11-08. Confirmed against the Debezium page connectors/sqlserver (read in part: Limitations, the collation note, streaming.delay.ms, data.query.mode and source.struct.version rows, and the incremental snapshot schema change note). Corrected the function name to the page's form.

Method: documentation only; no commands were run.
