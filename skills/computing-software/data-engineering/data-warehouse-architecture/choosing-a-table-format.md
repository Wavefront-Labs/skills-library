---
id: computing-software.data-engineering.data-warehouse-architecture.choosing-a-table-format
name: choosing-a-table-format
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, table-format-selection, apache-iceberg, delta-lake, apache-hudi]
level: advanced
status: docs-checked
description: "Choose between Iceberg, Delta Lake and Hudi: engine support, catalogs, write patterns, interoperability (UniForm, XTable) and ecosystem fit."
sources:
  - https://iceberg.apache.org/docs/latest/
  - https://iceberg.apache.org/rest-catalog-spec/
  - https://docs.delta.io/latest/index.html
  - https://docs.delta.io/latest/delta-uniform.html
  - https://hudi.apache.org/docs/overview
  - https://xtable.apache.org/docs/how-to
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing a table format

**Goal:** pick the open table format that fits your engines, write patterns and catalog strategy, and keep interoperability options open.

## What each project's docs say it is for
| Factor | Iceberg | Delta Lake | Hudi |
|---|---|---|---|
| Positioning | open table format for huge analytic datasets, with a specification for compatibility across languages and implementations | open source lakehouse layer: ACID transactions, scalable metadata, streaming and batch unification | open table format built for high-performance writes on incremental pipelines; also a lakehouse platform with ingestion services |
| Engines named in the docs | Spark, Trino, PrestoDB, Flink, Hive, Impala | Spark, Flink, Hive, Trino, AWS Athena (connectors) | Spark, Flink, Presto, Trino, Hive; Rust/Python via Hudi-rs |
| Catalog | REST catalog protocol: a common API for any Iceberg catalog, with credential vending or remote signing | read the Delta docs for your catalog and engine | own timeline of transactions and table services |
| Row-level changes | see the Iceberg docs for your engine | merge, update and delete (CDC, SCD, streaming upserts) | efficient upserts and deletes, indexes, clustering and compaction; table types COPY_ON_WRITE and MERGE_ON_READ |
| Layout evolution | hidden partitioning, partition layout evolution, schema evolution (add, drop, update, rename) | schema enforcement | check the Hudi docs |
| Time travel | yes | yes | yes (snapshot, incremental and read-optimized query types) |
Engine lists in the docs are examples, not support guarantees: verify each engine and version you need against that engine's own documentation.

## Heuristics (judgement, not vendor claims)
- Mostly one vendor's platform: use the format that platform treats as native, and keep a read path for others.
- Several engines or vendors on the same data: favour a format with an open specification and a vendor-neutral catalog protocol, such as Iceberg with a REST catalog.
- Heavy CDC upserts with incremental pulls: evaluate Hudi (designed for incremental pipelines) against the others with your own workload.
- Choose the **catalog** with the format: governance, credential vending and engine access come from it.

## Interoperability
- Delta **UniForm** generates Iceberg metadata (and Hudi metadata, preview) asynchronously for the same Parquet data files, so Iceberg or Hudi clients read a Delta table. Requirements include column mapping and, for Iceberg, minReaderVersion >= 2, minWriterVersion >= 7, Delta Lake 3.1 or above, and table properties `delta.enableIcebergCompatV2` and `delta.universalFormat.enabledFormats`. It is read-only for the Iceberg and Hudi side: an external writer can destroy the Delta table. UniForm does not work on tables with deletion vectors enabled.
- **Apache XTable** (incubating) syncs a table's metadata to other target formats without copying the data files, run as a bundled jar.
- Read-compatibility of advanced features differs by engine; check each one.

## Evaluate with a proof
Load a representative table, run your write pattern (batch append, MERGE CDC, streaming), query from every engine you need, measure compaction and maintenance effort, and test catalog permissions end to end.

## Gotchas
- Format choice is less important than having one catalog and consistent maintenance.
- Migrating formats later is possible (metadata conversion or rewrite) but disruptive; decide early for core tables.

## Verify
Decision record lists required engines, write patterns tested and results; a sample table works in all required engines.

## Checked
2026-11-08: Read in full: the Iceberg, Delta Lake and Hudi documentation landing pages, the Iceberg REST catalog spec page, the Delta UniForm page and the first 40 lines of the XTable how-to (its intro and prerequisites; the rest is a tutorial). Removed unconfirmed claims from the draft: the wide engine list (Snowflake, BigQuery, Dremio, DuckDB, Databricks via Unity Catalog), named catalogs (Polaris, Nessie, Glue), Iceberg v3 deletion vectors, Delta liquid clustering, "limited" Hudi partition evolution, "best fit historically" streaming claims. Added UniForm requirements and limits from the Delta page. The heuristics are judgement.
Method: documentation only; no commands were run.
