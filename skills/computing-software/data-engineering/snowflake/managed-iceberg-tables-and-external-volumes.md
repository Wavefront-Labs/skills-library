---
id: computing-software.data-engineering.snowflake.managed-iceberg-tables-and-external-volumes
name: managed-iceberg-tables-and-external-volumes
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, snowflake-iceberg-tables, external-volume, iceberg, catalog-integration, open-catalog, polaris, glue-catalog, interoperability, base-location]
level: advanced
status: docs-checked
description: "Store Snowflake tables as Apache Iceberg in your bucket: external volumes, Snowflake-managed vs Glue/Open Catalog tables, and reading them from Spark or Trino."
sources:
  - https://docs.snowflake.com/en/user-guide/tables-iceberg
  - https://docs.snowflake.com/en/user-guide/tables-iceberg-configure-external-volume
  - https://docs.snowflake.com/en/user-guide/tables-iceberg-configure-catalog-integration
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Iceberg tables and external volumes in Snowflake

**Goal:** keep table data in open Iceberg format in your own storage so Snowflake and other engines (Spark, Trino, Flink) can use the same tables.

## External volume (where data files live)
```sql
create or replace external volume lake_vol
  storage_locations = ((
    name = 'eu-west-1'
    storage_provider = 'S3'
    storage_base_url = 's3://<BUCKET>/iceberg/'
    storage_aws_role_arn = 'arn:aws:iam::<acct>:role/snowflake-iceberg'
  ));
desc external volume lake_vol;     -- trust policy values for the IAM role (like storage integrations)
```
The role needs read/write/delete on the prefix for Snowflake-managed tables.

## Snowflake-managed Iceberg table (Snowflake is the catalog)
```sql
create iceberg table analytics.orders_ice (order_id string, amount number(12,2), ordered_at timestamp_ntz)
  catalog = 'SNOWFLAKE'
  external_volume = 'lake_vol'
  base_location = 'analytics/orders_ice/';
```
Snowflake writes Parquet and Iceberg metadata. To sync to another catalog, see the CREATE ICEBERG TABLE reference.

## Externally managed (another catalog owns it)
```sql
create catalog integration glue_cat
  catalog_source = glue catalog_namespace = 'lake_db' table_format = iceberg
  glue_aws_role_arn = 'arn:aws:iam::<acct>:role/snowflake-glue' glue_catalog_id = '<acct>' enabled = true;
create iceberg table analytics.events_ice
  external_volume = 'lake_vol' catalog = 'glue_cat'
  ... ;   -- remaining parameters for a Glue-catalog table: see the CREATE ICEBERG TABLE reference
alter iceberg table analytics.events_ice refresh;     -- pick up new snapshots
```
Check the catalog integration page for supported catalog sources and parameters.

## Trade-offs
- Some features differ from native tables; check the Iceberg limits on the tables-iceberg page.

## Verify
- [ ] Spark (Iceberg REST or Glue catalog) reads the table and sees the same row count.
- [ ] Data and metadata files appear under the `base_location` prefix.

## Checked

2026-10-28: reviewed against the official documentation fetched this batch.

Confirmed on the tables-iceberg, CREATE EXTERNAL VOLUME and CREATE CATALOG INTEGRATION (Glue) pages: STORAGE_LOCATIONS with STORAGE_PROVIDER, STORAGE_BASE_URL and STORAGE_AWS_ROLE_ARN, DESCRIBE EXTERNAL VOLUME, CATALOG_SOURCE = GLUE, TABLE_FORMAT = ICEBERG, GLUE_AWS_ROLE_ARN, GLUE_CATALOG_ID, CATALOG_NAMESPACE, CATALOG = SNOWFLAKE with EXTERNAL_VOLUME and BASE_LOCATION, ALTER ICEBERG TABLE REFRESH.

Removed: CATALOG_SYNC wording, the catalog table-name parameter and auto-refresh option (not on the pages read), storage billing and performance claims.

Method: documentation only; no commands were run.
