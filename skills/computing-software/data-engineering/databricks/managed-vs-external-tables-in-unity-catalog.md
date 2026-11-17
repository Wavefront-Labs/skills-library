---
id: computing-software.data-engineering.databricks.managed-vs-external-tables-in-unity-catalog
name: managed-vs-external-tables-in-unity-catalog
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, uc-managed-tables, external-tables, unity-catalog, external-locations]
level: advanced
status: docs-checked
description: "Choose between Unity Catalog managed and external tables: storage locations, drop semantics, predictive optimization, external locations, and converting external to managed."
sources:
  - https://docs.databricks.com/aws/en/tables/managed
  - https://docs.databricks.com/aws/en/tables/external
  - https://docs.databricks.com/aws/en/connect/unity-catalog/cloud-storage/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Managed vs external tables in Unity Catalog

**Goal:** pick the table type on purpose, knowing what DROP does and which features you gain or lose.

## Managed tables (default, recommended)
```sql
CREATE TABLE main.sales.orders (order_id BIGINT, amount DECIMAL(18,2));
```
- Data under the schema/catalog/metastore **managed location**; Databricks controls file layout.
- `DROP TABLE` removes the table; data files are deleted after the recovery period expires (default 7 days).
- Support predictive optimization, which Databricks recommends enabling for all managed tables; other managed-table features are listed on the managed tables page.

## External tables
```sql
CREATE TABLE main.sales.orders_ext (order_id BIGINT) LOCATION 's3://acme-lake/sales/orders';
```
- Path must be inside an **external location** (storage credential + URL) you have CREATE EXTERNAL TABLE on.
- `DROP TABLE` removes metadata only; files stay.
- Use when other systems must read/write the same files by path, or for data you must keep under a specific bucket layout.

## Setting managed locations
```sql
CREATE CATALOG finance MANAGED LOCATION 's3://acme-uc-finance/';
CREATE SCHEMA finance.gl MANAGED LOCATION 's3://acme-uc-finance/gl/';
```
Per-catalog buckets give data isolation per domain/compliance boundary while staying managed.

## Converting external to managed
CTAS or DEEP CLONE into a managed table and swap names; check the managed tables page for any in-place conversion command. Readers by path must be migrated first.

## Gotchas
- Never point two external tables (or a table and a volume) at overlapping paths.
- Writing files directly into a managed table's storage path is unsupported and can corrupt it.
- External engines reading managed tables should use UC (Delta Sharing, UC REST/Iceberg endpoints, credential vending), not raw paths.

## Verify
`DESCRIBE EXTENDED` shows whether the table is managed or external and the storage location as intended.

## Checked

- 2026-10-28: confirmed on the managed tables page (predictive optimization recommended, default 7-day recovery period, external table files must be deleted manually) and the external tables and cloud storage pages.
- Removed: `UNDROP`, automatic liquid clustering and metadata claims (the page lists liquid clustering as off by default), and the `SET MANAGED` statement.

Method: documentation only; no commands were run.
