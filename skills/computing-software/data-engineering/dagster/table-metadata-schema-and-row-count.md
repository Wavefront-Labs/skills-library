---
id: computing-software.data-engineering.dagster.table-metadata-schema-and-row-count
name: table-metadata-schema-and-row-count
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, table-schema, row-count, column-schema, build-column-schema-change-checks, tablecolumn]
level: advanced
status: docs-checked
description: "Attach dagster/column_schema and dagster/row_count to table assets and detect schema drift with build_column_schema_change_checks."
sources:
  - https://docs.dagster.io/guides/build/assets/metadata-and-tags/table-metadata
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Table metadata

Goal: expose schema and row counts for tabular assets and catch schema changes.

## Column schema
Construct a `TableSchema` with `TableColumn` entries and attach it under the `dagster/column_schema` metadata key, either on the asset definition (schema known up front) or on the `MaterializeResult` returned by the asset (schema known only at materialization). It is then visible in the UI. The dbt integration can attach column schema automatically for assets loaded from dbt models.

## Row count
Attach a numeric value under `dagster/row_count` in the metadata of the `MaterializeResult` returned by the asset. The UI highlights it and lets you track changes over time, which you can use to monitor data quality.

## Column-level lineage
Covered on a separate docs page (see the column-level-lineage skill).

## Schema change checks
When schemas are defined at runtime, `build_column_schema_change_checks` creates asset checks that compare the current materialization's schema to the previous one. They detect added columns, removed columns and changed column types.

## Checked
2026-11-08. Confirmed against the Dagster docs page Table metadata (raw markdown from the docs repo): metadata keys, definition versus runtime attachment, dbt note, schema change checks. Added the lineage pointer from the page; nothing removed. Snippets are referenced by file and were not read.
Method: documentation only; no commands were run.
