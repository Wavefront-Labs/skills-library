---
id: computing-software.data-engineering.snowflake.refreshing-externally-managed-iceberg-tables
name: refreshing-externally-managed-iceberg-tables
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, iceberg-auto-refresh, iceberg, catalog-integration, metadata-refresh]
level: advanced
status: docs-checked
description: "Keep Snowflake's view of externally managed Iceberg tables current: manual REFRESH, AUTO_REFRESH with catalog integrations, refresh intervals and status checks."
sources:
  - https://docs.snowflake.com/en/user-guide/tables-iceberg-auto-refresh
  - https://docs.snowflake.com/en/sql-reference/sql/alter-iceberg-table-refresh
  - https://docs.snowflake.com/en/sql-reference/sql/create-catalog-integration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Refreshing externally managed Iceberg tables

**Goal:** Snowflake queries see new snapshots written by Spark/Flink/Glue soon after they commit.

## Manual refresh
```sql
ALTER ICEBERG TABLE lake.events REFRESH;                                   -- from the catalog
ALTER ICEBERG TABLE lake.events REFRESH 'metadata/00042-abc.metadata.json'; -- optional metadata file path
```
Run after the writer commits (e.g. as the last step of the Spark job, or from the orchestrator).

## Automatic refresh
```sql
CREATE CATALOG INTEGRATION glue_int
  CATALOG_SOURCE = GLUE CATALOG_NAMESPACE = 'lake' TABLE_FORMAT = ICEBERG
  GLUE_AWS_ROLE_ARN = 'arn:aws:iam::123456789012:role/snowflake-glue' GLUE_CATALOG_ID = '123456789012'
  REFRESH_INTERVAL_SECONDS = 60 ENABLED = TRUE;

CREATE ICEBERG TABLE lake.events
  EXTERNAL_VOLUME = 'lake_vol' CATALOG = 'glue_int' CATALOG_TABLE_NAME = 'events'
  AUTO_REFRESH = TRUE;

ALTER ICEBERG TABLE lake.events SET AUTO_REFRESH = TRUE;
SELECT SYSTEM$AUTO_REFRESH_STATUS('lake.events');
```
Snowflake polls the external catalog every `REFRESH_INTERVAL_SECONDS` (default 30 seconds); check the Iceberg automated refresh docs for supported catalog types.

## Verify
Write a row from Spark; within the interval, `SELECT count(*)` in Snowflake reflects it and auto-refresh status shows the latest snapshot.

## Checked
2026-10-28. Confirmed against ALTER ICEBERG TABLE ... REFRESH, the Iceberg automated refresh page (REFRESH_INTERVAL_SECONDS default 30 seconds with a Glue example at 60 seconds, ALTER ICEBERG TABLE ... SET AUTO_REFRESH, SYSTEM$AUTO_REFRESH_STATUS, CATALOG_SOURCE = GLUE). Removed: the supported-catalog list, the catalog-linked database section and the gotchas (serverless cost, schema evolution, snapshot expiry).
Method: documentation only; no commands were run.
