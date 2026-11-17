---
id: computing-software.data-engineering.data-warehouse-architecture.open-source-query-engines-trino-duckdb
name: open-source-query-engines-trino-duckdb
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, platform-selection, trino, duckdb, federated-queries, iceberg, single-node-analytics, motherduck]
level: practitioner
status: verified
description: "Decide when Trino (distributed, federated SQL over the lake) or DuckDB (in-process single-node analytics) fits, with setup snippets, sizing limits and operational costs."
sources:
  - https://trino.io/docs/current/connector/iceberg.html
  - https://trino.io/docs/current/admin/fault-tolerant-execution.html
  - https://duckdb.org/docs/current/connect/concurrency
  - https://docs.aws.amazon.com/athena/latest/ug/engine-versions-reference-0003.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Open-source query engines: Trino and DuckDB

**Goal:** know where these engines beat or complement a commercial warehouse, and what running them costs.

## Trino (distributed MPP SQL)
**Use for:** interactive SQL over data lake tables (Iceberg/Delta/Hive) at TB-PB scale; federated queries joining lake + Postgres + MySQL + Kafka; avoiding warehouse lock-in.
```properties
# etc/catalog/lake.properties
connector.name=iceberg
iceberg.catalog.type=rest
iceberg.rest-catalog.uri=https://catalog.example.com/api/catalog
# etc/catalog/pg.properties
connector.name=postgresql
connection-url=jdbc:postgresql://pg:5432/app
connection-user=trino_ro
connection-password=${ENV:PG_PASSWORD}
```
```sql
select c.segment, sum(o.amount)
from lake.sales.orders o join pg.public.customers c on o.customer_id = c.id
where o.order_date >= date '2026-10-01' group by 1;
```
Property names above checked against the Trino docs (`iceberg.catalog.type` accepts `hive_metastore`, `glue`, `jdbc`, `rest`, `nessie`; `iceberg.rest-catalog.uri`; `${ENV:VARIABLE}` secrets; `retry-policy` is `NONE`/`QUERY`/`TASK`); the configs were not run (no Trino here). Operational reality: coordinator + workers (k8s Helm chart), memory tuning (`query.max-memory`, `query.max-memory-per-node`), spill config, fault-tolerant execution (`retry-policy=TASK` with an exchange manager on S3 or similar; `query.max-memory*` limits do not apply to task-level retries) for long ETL queries, resource groups for concurrency, access control (file-based, Ranger, OPA). Managed: Starburst Galaxy, Amazon Athena (engine version 3 tracks Trino and Presto open source per AWS docs), EMR.

Pushdown matters for federation: predicates/aggregations push to Postgres, but large cross-source joins pull data into Trino.

## DuckDB (in-process OLAP)
**Use for:** single-machine analytics up to hundreds of GB (larger with spilling), local development/testing of SQL pipelines, data apps, CI tests, reading Parquet/Iceberg/Delta directly from object storage, replacing pandas for heavy transforms.
```python
import duckdb
con = duckdb.connect()
con.sql("INSTALL httpfs; LOAD httpfs; INSTALL iceberg; LOAD iceberg;")
con.sql("CREATE SECRET (TYPE s3, PROVIDER credential_chain);")
con.sql("""
  select order_date, sum(amount) from read_parquet('s3://lake/orders/*/*.parquet', hive_partitioning=true)
  where order_date >= '2026-10-01' group by 1 order by 1
""").show()
```
Limits: single node, not a multi-user server (MotherDuck adds a hosted/shared layer). Concurrency per the DuckDB docs: within one process many threads work, but across processes only read-only access to one database file is supported; the Quack remote protocol for multi-process writes was beta in v1.5.2, and DuckLake with a PostgreSQL catalog is the documented stable alternative. Run locally on DuckDB 1.5.6: `read_parquet('.../*/*.parquet', hive_partitioning=true)` with `where order_date >= '2026-10-01'` returned only the matching partitions, and `INSTALL httpfs; LOAD httpfs; INSTALL iceberg; LOAD iceberg; CREATE SECRET (TYPE s3, PROVIDER credential_chain);` executed without error. Excellent for dbt local dev (`dbt-duckdb`) and lightweight pipelines.

## Choosing
| Need | Pick |
|---|---|
| Many concurrent BI users on PB lake | Trino/Starburst or a warehouse |
| Federated joins across operational DBs | Trino |
| Fast local/CI SQL, embedded analytics, < 1 TB | DuckDB |
| Fully managed, minimal ops | warehouse or managed Trino (Athena/Starburst) |

## Gotchas
- Self-hosted Trino's TCO includes on-call, upgrades and tuning; compare to managed pricing honestly.
- Iceberg writes from Trino and Spark simultaneously need the same catalog and compaction ownership.
- DuckDB reading S3 Parquet without partition pruning or column projection downloads a lot; filter on partition columns.

## Verify
- [ ] Benchmark representative queries on candidate engines with cost per query recorded.
- [ ] For Trino: resource groups and access control configured before opening to users.
