---
id: computing-software.data-engineering.druid.druid-update-overwrite-and-reindex
name: druid-update-overwrite-and-reindex
category: computing-software
field: data-engineering
product: druid
tags: [update, overwrite, reindex, replace, append-to-existing, druid-input-source]
level: practitioner
status: docs-checked
description: "Update Druid data by overwriting a time range or reindexing; there are no single-record updates."
sources:
  - https://github.com/apache/druid/blob/master/docs/data-management/update.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Druid partitions data by time chunk and updates it by overwriting time ranges using the same mechanisms as batch ingestion. Data outside the replacement range is untouched.

Examples: native batch with `appendToExisting: false` and `intervals` set to a range overwrites that range; SQL `REPLACE <table> OVERWRITE [ALL | WHERE ...]` overwrites the table or a time range. Druid's atomic update mechanism flips queries from old to new data one time chunk at a time.

Ingestion and overwrite cannot run concurrently on the same time range of the same datasource. While an overwrite runs, new ingestion for that range is queued; other ranges proceed, and read-only queries use the existing version.

Druid does not support single-record updates by primary key.

Reindexing is an overwrite whose source is the existing data. Use it for schema changes, repartitioning, filtering out unwanted data or enriching data. It follows the same atomic update and locking behaviour. With native batch it uses the `druid` input source, and `transformSpec` can filter or modify data during the job. With SQL use `REPLACE <table> OVERWRITE` with `SELECT ... FROM <table>`; Druid has no `UPDATE` or `ALTER TABLE` statements.

Rolled-up datasources can be updated by appending: rows with an identical set of dimensions are combined at query time by aggregation operators, and compaction or automatic compaction can physically combine them later.

For a dimension whose values change often, such as mapping an ID to a human-readable name, try lookups first.

## Checked

2026-11-08. Read data-management/update.md in full. Added SQL reindex, rolled-up datasource appends and the lookups advice.

Method: documentation only; no commands were run.
