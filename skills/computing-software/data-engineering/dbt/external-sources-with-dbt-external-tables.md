---
id: computing-software.data-engineering.dbt.external-sources-with-dbt-external-tables
name: external-sources-with-dbt-external-tables
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-sources, dbt-external-tables, external-tables, stage-external-sources, snowflake, bigquery, spark, data-lake]
level: practitioner
status: docs-checked
description: "Declare data-lake files as dbt sources with the dbt-external-tables package: YAML external config per warehouse, stage_external_sources, partitions and refresh."
sources:
  - https://github.com/dbt-labs/dbt-external-tables
  - https://hub.getdbt.com/dbt-labs/dbt_external_tables/latest/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# External sources with dbt-external-tables

**Goal:** files in S3/GCS/ADLS become queryable sources defined in dbt YAML, created and refreshed by dbt, with lineage like any other source.

## Install
```yaml
# packages.yml
packages:
  - package: dbt-labs/dbt_external_tables
    version: [">=0.12.0", "<0.13.0"]   # latest release is 0.12.4
```

## Snowflake example
```yaml
sources:
  - name: lake
    database: raw
    schema: ext
    loader: S3
    tables:
      - name: events
        external:
          location: "@raw.ext.lake_stage/events/"     # existing external stage
          file_format: "(type = parquet)"
          auto_refresh: true                           # requires an event notification from Amazon S3 or Azure
          partitions:
            - name: event_date
              data_type: date
              expression: to_date(substr(metadata$filename, 8, 10), 'YYYY-MM-DD')   # illustrative: derive the value from the file path
        columns:
          - {name: event_id, data_type: varchar}
          - {name: user_id, data_type: varchar}
          - {name: ts, data_type: timestamp_ntz}
```
Snowpipe alternative: an `external.snowpipe` block (with `auto_ingest`, `aws_sns_topic` or `integration`, `copy_options`) makes the package create an empty table, backfill it and pipe new data instead of an external table.

## BigQuery example
```yaml
      - name: events
        external:
          location: "gs://lake/events/*"
          options:
            format: parquet
            hive_partition_uri_prefix: "gs://lake/events"
          partitions:
            - {name: event_date, data_type: date}
```

## Spark/Databricks
```yaml
        external:
          location: "s3://lake/events/"
          using: csv              # file type: csv, json, parquet, delta, ...
          partitions: [{name: event_date, data_type: date}]
```

## Create/refresh
```bash
dbt run-operation stage_external_sources                          # create if missing, refresh metadata
dbt run-operation stage_external_sources --vars "ext_full_refresh: true"   # create or replace (+ refresh if necessary)
dbt run-operation stage_external_sources --args "select: lake.events"
```
Run it before models that read the external sources.

## Gotchas
- Specify all column names and data types: column order must match for CSVs and names must match for other formats; some databases support schema inference.
- All Snowflake external tables include a `metadata$filename` pseudocolumn and a `value` column, so they need not be declared.
- BigQuery: for a partitioned external table the file paths must be Hive-style and `hive_partition_uri_prefix` must be set; BigQuery can also infer columns and partitions.
- The package needs permissions to create tables, and the database/project and schema/dataset must already exist.

## Verify
- [ ] `select count(*)` on the external source returns rows after `stage_external_sources`.
- [ ] `dbt run-operation stage_external_sources --args "select: lake.events"` refreshes a single table.

## Checked

2026-10-25: dbt-external-tables repository on main. Confirmed: dbt-external-tables README and sample_sources (repository last commit 2026-10-01, latest release 0.12.4): `stage_external_sources` modes and `select:` syntax, `ext_full_refresh`, `external` properties per warehouse (Snowflake `location`, `file_format`, `auto_refresh`, `partitions` with `expression`, `snowpipe`; BigQuery `location`, `options`, `hive_partition_uri_prefix`; Spark `using`, `options`), column and prerequisite requirements. Removed unconfirmed claims about performance, freshness on metadata columns and the earlier version range; the Snowflake partition expression is illustrative.

Method: documentation only; no commands were run.
