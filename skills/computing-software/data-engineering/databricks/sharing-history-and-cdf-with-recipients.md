---
id: computing-software.data-engineering.databricks.sharing-history-and-cdf-with-recipients
name: sharing-history-and-cdf-with-recipients
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, delta-sharing, share-with-history, change-data-feed, streaming-from-shares, time-travel, incremental-consumption]
level: advanced
status: docs-checked
description: "Share Delta tables WITH HISTORY so recipients can time travel, read the change data feed and stream from a share, with runtime gotchas."
sources:
  - https://docs.databricks.com/aws/en/opensharing/create-share
  - https://docs.databricks.com/aws/en/opensharing/read-data-databricks
  - https://docs.databricks.com/aws/en/tables/features/change-data-feed
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sharing history and CDF with recipients

**Goal:** recipients consume only changes (not full snapshots) from a shared table, efficiently and reliably.

## Provider side
```sql
ALTER TABLE sales.core.orders SET TBLPROPERTIES (delta.enableChangeDataFeed = true);

ALTER SHARE partner_share ADD TABLE sales.core.orders
  WITH HISTORY                                  -- time travel, streaming reads and (with CDF on) table_changes
  PARTITION (region = 'EMEA')                   -- optional partition filter
  AS emea.orders;                               -- name as seen by recipient
```
Enable change data feed on the table before sharing it `WITH HISTORY` if recipients should call `table_changes()`. `WITH HISTORY` and `WITHOUT HISTORY` need Databricks Runtime 12.2 LTS or above; table sharing defaults to `WITH HISTORY` on Runtime 16.2 or above and `WITHOUT HISTORY` on earlier runtimes. Time travel, streaming reads and transactions on the recipient side need the table shared with history.

## Recipient side (Databricks)
```sql
CREATE CATALOG partner FROM SHARE provider_org.partner_share;
SELECT * FROM partner.emea.orders VERSION AS OF 120;
SELECT * FROM table_changes('partner.emea.orders', 120, 135);
```
Streaming incrementally:
```python
(spark.readStream.format("deltaSharing")
   .option("readChangeFeed", "true")
   .option("startingVersion", 120)
   .table("partner.emea.orders")
   .writeStream.option("checkpointLocation", "/Volumes/chk/partner_orders")
   .trigger(availableNow=True)
   .toTable("bronze.partner_orders"))
```
Streaming also supports `ignoreDeletes`, `ignoreChanges` and `startingVersion` (inclusive). Time travel and streaming need Databricks Runtime 12.2 LTS or above on the recipient.

## Retention coupling
Recipients can only read versions the provider still retains:
- Change data feed records are transient: table versions and their CDF versions are removed at regular intervals, and `VACUUM` deletes change data files under the table's retention policy. Once a version is removed, recipients can no longer read its changes.
Agree an SLA on how soon recipients must consume changes relative to the provider's retention settings.

## Gotchas
- Streaming from a share without history is not possible; re-add the table `WITH HISTORY`.
- If the shared table has deletion vectors or column mapping enabled, batch reads need Databricks Runtime 14.1 or above, and CDF or streaming reads need Runtime 14.2 or above with `responseFormat=delta` (optional on Runtime 16.4+ for CDF or plain streaming, and 17.3+ for CDF streaming).
- Tables shared with partition filters or without history need Scala Spark with `responseFormat` set to `delta` for row tracking columns.

## Verify
- [ ] Recipient `table_changes` returns rows for a version range after a provider MERGE.
- [ ] Recipient streaming job processes only new versions on subsequent runs.

## Checked

2026-11-09. Confirmed on the Databricks share creation, reading shared data and change data feed pages: ALTER SHARE ADD TABLE syntax with PARTITION, AS and WITH or WITHOUT HISTORY, defaults by runtime (16.2), CDF must be enabled before sharing for table_changes(), VERSION AS OF and table_changes on the recipient, streaming options on format deltaSharing (readChangeFeed, startingVersion, ignoreDeletes, ignoreChanges), deletion vector and column mapping runtime requirements, CDF retention and VACUUM. Removed: load_table_changes_as_pandas, the 30-day logRetentionDuration default, the partition-filter and schema-change gotchas and the 7/14-day SLA figures (not on the pages). Example object names are placeholders.

Method: documentation only; no commands were run.

