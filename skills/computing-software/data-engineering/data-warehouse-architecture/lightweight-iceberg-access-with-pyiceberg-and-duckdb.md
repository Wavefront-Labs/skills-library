---
id: computing-software.data-engineering.data-warehouse-architecture.lightweight-iceberg-access-with-pyiceberg-and-duckdb
name: lightweight-iceberg-access-with-pyiceberg-and-duckdb
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, pyiceberg, duckdb, apache-iceberg, python]
level: practitioner
status: verified
description: "Read and write Iceberg tables without Spark using PyIceberg and DuckDB: catalog config, scans with filters, appends and upserts, schema evolution, and limits."
sources:
  - https://py.iceberg.apache.org/configuration/
  - https://duckdb.org/docs/current/core_extensions/iceberg/overview
  - https://duckdb.org/docs/current/core_extensions/iceberg/catalogs.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lightweight Iceberg access (PyIceberg / DuckDB)

**Goal:** query and maintain small-to-medium Iceberg workloads from Python services, notebooks or CI without a Spark cluster.

## Configure a catalog
```yaml
# ~/.pyiceberg.yaml  (or env vars PYICEBERG_CATALOG__PROD__URI=...)
catalog:
  prod:
    type: rest
    uri: https://catalog.example.com/api/catalog
    warehouse: analytics
    credential: <client_id>:<client_secret>
```
The `type` values are `rest`, `sql` (sqlite/postgres), `hive`, `glue`, `dynamodb` and `in-memory` (BigQuery is also in the 0.12 enum). The file is found via `PYICEBERG_HOME`, then the home directory, then the working directory. `credential` is `client_id:client_secret` (OAuth2 client credentials). The catalog name in the YAML must match the name the table was created under (a SQL catalog stores it per row). Env vars use `__` for nesting (`PYICEBERG_CATALOG__PROD__TYPE=sql`); tested with a sqlite catalog.

## Read
```python
from pyiceberg.catalog import load_catalog
cat = load_catalog("prod")
tbl = cat.load_table("sales.orders")
arrow = tbl.scan(row_filter="order_date >= '2026-10-01' AND status = 'paid'",
                 selected_fields=("order_id", "amount")).to_arrow()
df = tbl.scan(limit=1000).to_pandas()
```
Filters prune partitions and files using manifest statistics.

## Write
```python
tbl.append(arrow_table)                         # schema must match (or evolve first)
tbl.overwrite(arrow_table, overwrite_filter="order_date = '2026-10-17'")
tbl.upsert(arrow_table, join_cols=["order_id"]) # returns UpsertResult(rows_updated, rows_inserted); ran on 0.12
with tbl.update_schema() as u:
    u.add_column("channel", StringType())
```
Writes go through the catalog (atomic commit).

## DuckDB
```sql
INSTALL iceberg; LOAD iceberg;
-- a metadata file always works; a bare table directory needs version-hint.text (or SET unsafe_enable_version_guessing = true, or version => '?')
SELECT count(*) FROM iceberg_scan('s3://acme-lake/warehouse/sales/orders/metadata/00004-<uuid>.metadata.json');
LOAD httpfs;
CREATE SECRET iceberg_secret (TYPE ICEBERG, TOKEN 'bearer_token');   -- or OAuth2 credentials; optional for some OAuth2 catalogs
ATTACH 'analytics' AS lake (TYPE iceberg, SECRET iceberg_secret, ENDPOINT 'https://catalog.example.com/api/catalog');  -- REST catalog
SELECT * FROM lake.sales.orders WHERE order_date = '2026-10-18';
```
`iceberg_scan` on a path is read-only; writes (INSERT, UPDATE, DELETE, MERGE INTO) are documented only for an attached REST catalog, and are newer than read support, so check your version. Run here (DuckDB 1.5.6, local sqlite catalog): `iceberg_scan` on a PyIceberg metadata file returned the right count; on the bare directory it failed with "No version was provided and no version-hint could be found". The REST ATTACH could not be run (no catalog available), syntax is from the DuckDB docs.

## Limits
- Single-process: large scans are bounded by one machine's memory/network; push heavy work to Spark/Trino.
- Feature coverage (MOR deletes, v3 features, maintenance procedures) lags Spark: check the docs.

## Verify
Counts from PyIceberg/DuckDB equal those from Spark/Trino for the same snapshot (`tbl.current_snapshot().snapshot_id`).
