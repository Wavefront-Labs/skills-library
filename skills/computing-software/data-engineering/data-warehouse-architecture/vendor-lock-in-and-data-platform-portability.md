---
id: computing-software.data-engineering.data-warehouse-architecture.vendor-lock-in-and-data-platform-portability
name: vendor-lock-in-and-data-platform-portability
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, vendor-lock-in, portability, open-table-formats, exit-strategy, iceberg, multi-engine]
level: practitioner
status: draft
description: "Assess and reduce data platform lock-in: where lock-in actually lives, open table formats and engines, portable SQL and dbt, egress costs, contract terms and an exit plan."
sources:
  - https://iceberg.apache.org/docs/latest/
  - https://delta.io/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Vendor lock-in and portability

Lock-in isn't binary; it's the cost and time to move. Decide consciously where you accept it in exchange for productivity.

## Where lock-in lives
| Layer | Lock-in drivers | Mitigation |
|---|---|---|
| Storage format | proprietary internal storage (classic warehouse tables) | open table formats (Iceberg, Delta, Hudi) on your object storage |
| Catalog | proprietary metastore | Iceberg REST catalog, Unity Catalog OSS, Polaris; or accept and plan export |
| SQL dialect | vendor functions (QUALIFY, FLATTEN, ARRAY functions, semi-structured syntax) | dbt cross-database macros, SQLGlot transpilation, style guide limiting exotic features |
| Procedural code | stored procedures, Snowpark/UDFs in vendor runtimes | keep logic in dbt/Python outside the warehouse where feasible |
| Orchestration/ingestion | vendor-specific pipelines (Snowpipe, DLT, Glue jobs) | Airflow/Dagster, open connectors (Airbyte, dlt), CDC via Debezium |
| Security model | roles, masking, row policies | policies as code, documented model mapping |
| Ecosystem | BI semantic layers, marketplace data, ML features | semantic layer outside BI tool (dbt Semantic Layer, Cube) |
| Commercial | committed spend, discounts tied to volume | term length vs flexibility, exit clauses |

## Open table formats: the biggest lever
- Data in Iceberg/Delta on your S3/ADLS/GCS can be read by Spark, Trino, Flink, DuckDB, Snowflake (Iceberg tables), BigQuery (BigLake), Databricks, Athena - switching engines doesn't require copying data.
- Trade-offs: some engines offer fewer optimisations on external/open tables; catalog interoperability is still maturing; you own more operations (compaction, snapshot expiry).

## Measure portability
- Inventory vendor-specific features in use (query history parsing, SQLGlot to detect dialect-only functions).
- Estimate egress cost for full data volume (cloud egress per GB) and migration effort (number of objects, procedures, pipelines).
- Test it: periodically run a subset of dbt models on a second engine (DuckDB/Trino) in CI to keep SQL portable.

## Contract and regulation
- Data export rights, format and assistance in the contract; termination assistance period.
- Regulated firms (EU DORA, EBA/ECB outsourcing guidelines) must have documented exit strategies for critical ICT providers.

## Balanced stance
Use managed proprietary features where they deliver large productivity gains, keep **data** in open formats where practical, keep **transformation logic** in version-controlled, mostly portable code, and keep an exit plan current.

## Verify
- [ ] Lock-in register lists each dependency, accepted reason and mitigation.
- [ ] Exit plan has cost/time estimates and was reviewed in the last year.
