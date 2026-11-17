---
id: computing-software.ai-ml-engineering.mlops.versioned-data-lakefs-and-delta-time-travel
name: versioned-data-lakefs-and-delta-time-travel
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, data-versioning, lakefs, delta-time-travel, iceberg-snapshots, training-data-reproducibility, data-lineage]
level: practitioner
status: docs-checked
description: "Pin exact training data versions with Delta and Iceberg time travel (or lakeFS), and keep VACUUM and snapshot expiry from breaking reproducibility."
sources:
  - https://raw.githubusercontent.com/delta-io/delta-docs/main/src/pages/latest/delta-batch.mdx
  - https://raw.githubusercontent.com/delta-io/delta-docs/main/src/pages/latest/delta-utility.mdx
  - https://raw.githubusercontent.com/apache/iceberg/main/docs/docs/spark-queries.md
  - https://raw.githubusercontent.com/apache/iceberg/main/docs/docs/spark-procedures.md
  - https://raw.githubusercontent.com/treeverse/lakeFS/master/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Versioned data lakes: lakeFS and Delta time travel

**Goal:** every model can say which data it was trained on, and you can re-read it later.

## Delta Lake time travel
```python
df = spark.read.format("delta").option("versionAsOf", 128).load("/delta/features")
df = spark.read.format("delta").option("timestampAsOf", "2026-10-01T00:00:00Z").load("/delta/features")
```
SQL: `SELECT * FROM table_name VERSION AS OF 128` and `... TIMESTAMP AS OF '<timestamp>'`. The version is a long that comes from the output of `DESCRIBE HISTORY`, e.g. `spark.sql("DESCRIBE HISTORY delta.`/delta/features`")`.

## Iceberg time travel
Spark SQL supports `TIMESTAMP AS OF` and `VERSION AS OF`; the `VERSION AS OF` clause takes a long snapshot ID or a branch or tag name, for example `VERSION AS OF 'historical-snapshot'`. If a branch or tag name equals a snapshot ID, the snapshot ID wins, so use a prefixed name such as `snapshot-1`. `FOR SYSTEM_TIME AS OF` and `FOR SYSTEM_VERSION AS OF` also work, and `prod.db.table.tag_<name>` / `branch_<name>` address refs. DataFrame read options: `snapshot-id`, `as-of-timestamp` (milliseconds), `branch`, `tag` (tag and `as-of-timestamp` cannot be combined).

## lakeFS
The lakeFS README describes a Git-like interface to data on S3, Azure Blob Storage or Google Cloud Storage, S3-API compatible with Spark, Hive, Athena, DuckDB and Presto, which makes reproducing the state of data at any point in time straightforward. It describes hooks so that only data that passed tests becomes part of production. The lakeFS docs site was not readable in this batch, so command syntax, zero-copy branching and commit-ID addressing are not asserted here; use the lakeFS docs for those.

## The retention trap
- Delta: `VACUUM` removes files no longer referenced by the table and older than the retention threshold (default 7 days, from `delta.deletedFileRetentionDuration`). After running vacuum, time travel to a version older than the retention period is lost. Log files are deleted automatically after checkpoints; their default retention is 30 days (`delta.logRetentionDuration`). A safety check prevents dangerously short retention settings.
- Iceberg: snapshots are kept for snapshot isolation and time travel; the `expire_snapshots` procedure removes older ones (`older_than` default 5 days ago, `retain_last` default 1) and never removes files still required by a non-expired snapshot. Keep a tag or branch on snapshots you must retain (design guidance; check how your Iceberg version treats refs during expiry).
- Align retention with how long you need to reproduce a model's training data, not just storage cost.

## Verify
- [ ] Each production model records its data version (Delta version, Iceberg snapshot ID or tag).
- [ ] Re-reading the training data for the current production model works.
- [ ] Retention settings cannot expire referenced training snapshots.

## Checked
Date: 2026-11-09.
- Confirmed in the Delta batch and utility pages, the Iceberg Spark queries and procedures pages, and the lakeFS README: all concrete items above.
- Removed as unconfirmed: all lakectl commands and URIs, zero-copy branches and commit-ID reads, pre-merge hook specifics, the MLflow logging snippet, Delta SHALLOW/DEEP CLONE advice, Iceberg tag-with-retention mechanics, and the docs.lakefs.io, docs.delta.io and iceberg.apache.org source URLs (replaced by raw repo files; docs.lakefs.io not readable).
Method: documentation only; no commands were run.
