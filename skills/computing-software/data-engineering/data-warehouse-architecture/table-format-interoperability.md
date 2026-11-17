---
id: computing-software.data-engineering.data-warehouse-architecture.table-format-interoperability
name: table-format-interoperability
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, open-table-formats, uniform, xtable, delta-lake, apache-iceberg, apache-hudi, metadata-translation, multi-engine]
level: practitioner
status: verified
description: "Make one copy of lakehouse data readable as Delta, Iceberg and Hudi: Delta UniForm, Apache XTable metadata sync, catalog exposure, and their limits for writers."
sources:
  - https://docs.delta.io/latest/delta-uniform.html
  - https://docs.databricks.com/aws/en/delta/uniform
  - https://docs.databricks.com/aws/en/external-access/iceberg
  - https://xtable.apache.org/docs/how-to
  - https://github.com/apache/incubator-xtable
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Table format interoperability (UniForm / XTable)

**Goal:** let engines that speak different table formats read the same Parquet files without copying data.

## 1. The idea
Delta, Iceberg and Hudi all store data as Parquet; they differ in metadata. Interop tools write a second (or third) metadata layer pointing at the same files. One format is the **writer of record**; the others are read-only views.

## 2. Delta UniForm (Iceberg reads of Delta tables)
```sql
CREATE TABLE main.sales.orders (order_id BIGINT, amount DECIMAL(18,2), ts TIMESTAMP)
TBLPROPERTIES ('delta.enableIcebergCompatV2' = 'true',
               'delta.universalFormat.enabledFormats' = 'iceberg');
-- existing table
ALTER TABLE main.sales.orders SET TBLPROPERTIES (
  'delta.enableIcebergCompatV2'='true', 'delta.universalFormat.enabledFormats'='iceberg');
```
- Iceberg metadata is generated asynchronously after Delta commits; readers may lag a commit or two.
- Requirements/limits (Databricks docs): column mapping must be enabled (the docs create the table with `'delta.columnMapping.mode' = 'id'`, which they recommend; the OSS Delta UniForm page also says to enable column mapping); deletion vectors cannot be enabled on a table with Iceberg reads (use `REORG` to purge them first); VOID types are unsupported; data files are written with Zstandard instead of Snappy. Not run here (needs Databricks).
- On Databricks, Iceberg clients read via the Unity Catalog Iceberg REST endpoint (`/api/2.1/unity-catalog/iceberg-rest`), so Snowflake, Trino, Spark etc. connect as an Iceberg catalog.
- Iceberg clients get read-only access to UniForm tables; keep Delta as the writer. If external engines must write, use a native Iceberg table instead.

## 3. Apache XTable (incubating) — any to any
Runs as a sync job that reads one format's metadata and writes the others.
```yaml
# xtable-config.yaml
sourceFormat: HUDI
targetFormats: [DELTA, ICEBERG]
datasets:
  - tableBasePath: s3://lake/orders
    tableName: orders
    partitionSpec: order_date:VALUE
```
```bash
java -jar xtable-utilities-<version>-bundled.jar --datasetConfig xtable-config.yaml
# optionally --icebergCatalogConfig catalog.yaml (a yaml with `catalogImpl`, per the README) to use an Iceberg catalog
```
Run it after each source commit or on a schedule. The YAML keys (`sourceFormat`, `targetFormats`, `datasets`, `tableBasePath`, `tableName`, `partitionSpec`) and the `--datasetConfig` flag match the XTable README and tutorial; not run here (Java is not available).

## 4. Choosing
| Situation | Use |
|---|---|
| Databricks writer, Snowflake/Trino/BigQuery readers | UniForm + UC Iceberg REST |
| Hudi or Iceberg writer, Delta readers (e.g. Databricks / Fabric) | XTable |
| Several writers in different formats on one table | don't — pick one format |
| Engines all support Iceberg natively | write Iceberg directly; no translation |

## 5. Gotchas
- Readers see only features the target format can express — e.g. Delta generated columns or check constraints are not enforced through Iceberg.
- Maintenance (VACUUM / expire snapshots) runs on the writer format; the translated metadata must not reference vacuumed files — let the tool regenerate after maintenance.
- Time travel exists per format, but version numbers don't map 1:1.

## Verify
- [ ] An Iceberg client reads the latest Delta commit's rows (after metadata sync).
- [ ] Only one engine/format writes the table.
- [ ] Maintenance jobs don't break the secondary readers.
