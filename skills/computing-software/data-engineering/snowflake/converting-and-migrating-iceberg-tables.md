---
id: computing-software.data-engineering.snowflake.converting-and-migrating-iceberg-tables
name: converting-and-migrating-iceberg-tables
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, iceberg-table-conversion, iceberg, convert-to-managed, migration]
level: sme
status: docs-checked
description: "Move tables between Snowflake native and Iceberg formats: CTAS to Snowflake-managed Iceberg, CONVERT TO MANAGED for external catalogs, and cutover checks."
sources:
  - https://docs.snowflake.com/en/user-guide/tables-iceberg-conversion
  - https://docs.snowflake.com/en/sql-reference/sql/alter-iceberg-table-convert-to-managed
  - https://docs.snowflake.com/en/sql-reference/sql/create-iceberg-table-snowflake
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Converting and migrating Iceberg tables

**Goal:** change who manages a table (Snowflake vs external catalog) or move a native table to open Iceberg format without losing data or grants.

## External catalog -> Snowflake-managed
`ALTER ICEBERG TABLE ... CONVERT TO MANAGED` converts a table that uses an external Iceberg catalog into a Snowflake-managed Iceberg table (Snowflake becomes the catalog) without rewriting its files. Run `ALTER ICEBERG TABLE ... REFRESH` first, as the conversion page requires:
```sql
ALTER ICEBERG TABLE lake.events CONVERT TO MANAGED
  BASE_LOCATION = 'events/';
```
Read the conversion page for the conditions that block conversion and for what happens to the external catalog afterwards.

## Native table -> Snowflake-managed Iceberg
No in-place conversion; copy:
```sql
CREATE ICEBERG TABLE core.orders_ice
  CATALOG = 'SNOWFLAKE' EXTERNAL_VOLUME = 'lake_vol' BASE_LOCATION = 'core/orders'
  CLUSTER BY (order_date)
AS SELECT * FROM core.orders;
```
Then reapply grants/policies (`COPY GRANTS` on CREATE OR REPLACE where usable), switch pipelines, swap names (`ALTER TABLE ... RENAME`), keep the native table until validated.

## Type mapping checks
- TIMESTAMP_TZ/LTZ, VARIANT, very wide NUMBER, collations: supported mappings differ for Iceberg; check the data type page; cast explicitly in the CTAS.

## Cutover checklist
1. Row counts and checksums (`HASH_AGG(*)`) match.
2. Masking/row access policies and tags reattached.
3. Streams on the old table recreated on the new one.
4. External engines can read (test with Spark/Trino via the catalog).

## Gotchas

## Verify
An external engine reading the new table sees the same row counts as the source.

## Checked

2026-10-28: reviewed against the Snowflake documentation fetched this batch.

Confirmed: ALTER ICEBERG TABLE ... CONVERT TO MANAGED syntax and BASE_LOCATION, refresh-before-convert, CREATE ICEBERG TABLE ... AS SELECT with CATALOG, EXTERNAL_VOLUME, BASE_LOCATION and CLUSTER BY (conversion and create-iceberg-table pages).

Removed or corrected: the 'read-only-ish' wording, claims about external writers, case preservation, bucket lifecycle and one-way conversion, and the SYSTEM$GET_ICEBERG_TABLE_INFORMATION verify step (not on the pages read).

Method: documentation only; no commands were run.
