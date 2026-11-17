---
id: computing-software.data-engineering.data-warehouse-architecture.lakehouse-vs-warehouse-vs-lake
name: lakehouse-vs-warehouse-vs-lake
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, lakehouse-architecture, data-lake, cloud-data-warehouse, open-table-formats, storage-compute-separation, architecture-decision]
level: practitioner
status: draft
description: "Choose between a cloud warehouse, a data lake and a lakehouse: what each gives (ACID, governance, openness, cost, workloads) and hybrid patterns that are common in practice."
sources:
  - https://www.cidrdb.org/cidr2021/papers/cidr2021_paper17.pdf
  - https://iceberg.apache.org/docs/latest/
  - https://www.oreilly.com/library/view/fundamentals-of-data/9781098108298/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Lakehouse vs warehouse vs lake

**Goal:** an architecture decision grounded in workloads, skills and constraints, written down as an ADR, instead of vendor marketing.

## Definitions that matter for the decision
| | Cloud data warehouse | Data lake | Lakehouse |
|---|---|---|---|
| Storage | proprietary managed storage | files in object storage (Parquet/JSON/CSV) | files in object storage + open table format (Iceberg/Delta/Hudi) |
| Transactions / updates | full ACID, MERGE | none (file overwrite) | ACID, MERGE, time travel via table format |
| Governance | built in (RBAC, masking, lineage) | bucket/IAM level, coarse | catalog-based (Unity Catalog, Polaris, Glue + Lake Formation) |
| Engines | one vendor engine | any engine | many engines on the same tables |
| Workloads | SQL/BI best-in-class | ML/raw storage, cheap archive | SQL + ML + streaming on one copy |
| Ops effort | lowest | low storage effort, high correctness effort | medium (compaction, catalogs, maintenance) |

The lines have blurred: warehouses read/write Iceberg (Snowflake, BigQuery, Redshift), and lakehouse platforms ship warehouse-like SQL engines (Databricks SQL, Trino/Starburst, Dremio).

## Decision drivers
- **Engine diversity:** need Spark/Flink/Python ML and SQL on the same data without copies -> lakehouse / open table formats.
- **Team skills:** SQL-centric analytics team, few platform engineers -> warehouse first.
- **Openness / lock-in:** regulatory or strategic need to own data in open formats -> lakehouse or warehouse with external Iceberg tables.
- **Concurrency and BI latency:** high-concurrency dashboards -> warehouse or lakehouse SQL engine with caching; test with your query mix.
- **Streaming:** continuous ingestion and upserts at scale -> lakehouse formats or warehouse streaming features (Snowpipe Streaming, BigQuery Storage Write API).
- **Cost model:** storage on object storage is cheap everywhere; compute pricing and idle cost differ. Model your workload.
- **Unstructured data and ML:** images/docs/features near the tables -> lake/lakehouse (volumes, object storage).

## Common hybrid patterns
- Raw/bronze in object storage (Iceberg/Delta), curated marts in the warehouse.
- Single Iceberg copy with a REST catalog, queried by warehouse and Spark/Trino (requires catalog interoperability discipline).
- Warehouse primary, lake as archive and ML feature source via exports.

## ADR template
Context (workloads, volumes, latency, team) -> Options considered -> Decision -> Consequences (what we must operate: compaction, catalog, governance) -> Revisit triggers (cost thresholds, new engines).

## Gotchas
- "Lake without table format" for anything mutable recreates 2010s problems: partial writes, no deletes for GDPR, small files.
- Two catalogs (warehouse + lake) with overlapping tables cause governance drift; choose a system of record per table.

## Verify
- [ ] ADR approved with benchmarked representative queries and cost estimate.
- [ ] Every table has one designated system of record and catalog.
