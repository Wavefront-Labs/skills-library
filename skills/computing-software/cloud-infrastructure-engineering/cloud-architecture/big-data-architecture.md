---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.big-data-architecture
name: big-data-architecture
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, architecture-styles, big-data-architecture, lakehouse, lambda-architecture, kappa-architecture, spark, data-lake]
level: practitioner
status: docs-checked
description: "Design big data architectures: components, batch, streaming, lambda and kappa styles, lakehouse formats and governance, using Azure, Delta Lake and AWS Lake Formation docs."
sources: ["https://learn.microsoft.com/azure/architecture/databases/guide/big-data-architectures", "https://docs.aws.amazon.com/whitepapers/latest/building-data-lakes/building-data-lake-aws.html", "https://docs.delta.io/latest/index.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Big data architecture

## Steps
1. **Decide whether you need one.** Azure guidance: consider it to store and process volumes too
   large for a traditional database, transform unstructured data for analysis, or capture and
   analyse unbounded streams with low latency. Workloads: batch at rest, real-time in motion,
   interactive exploration, predictive analytics and ML.
2. **Identify the components** (not every solution has all): data sources, data storage (data lake),
   batch processing, real-time message ingestion (stream buffering, e.g. Event Hubs, IoT Hub,
   Kafka), stream processing, analytical data store, analytics and reporting, orchestration (e.g.
   Azure Data Factory, Fabric).
3. **Choose the processing style**:
   - **Lambda**: all data takes two paths. Batch layer (cold path) stores immutable raw data and
     builds batch views; speed layer (hot path) gives low latency at the expense of accuracy; a
     serving layer indexes the batch view and takes incremental updates from the speed layer. The
     cost is that logic exists in two places on different frameworks.
   - **Kappa**: one path through a stream processor. Events are immutable, appended to a
     distributed unified log, mirrored to long-term storage; recompute by replaying the stream,
     typically in parallel.
   - **Lakehouse**: combines data lake and warehouse, typically low-cost cloud storage in open
     formats such as Parquet or ORC for raw and processed data.
4. **Table format**: Delta Lake provides ACID transactions with serializable isolation, time travel
   (versioning, rollback, audit), one table used as batch table and streaming source and sink,
   schema enforcement, and merge/update/delete. Engines named on its page: Spark, Flink, Hive,
   Trino, Athena. Evaluate other table formats from their own documentation.
5. **Governance**: AWS Lake Formation manages access to S3 data and Glue Data Catalog metadata at
   database, table, column, row and cell level, with tag-based access control (LF-Tags) and audit
   logs via CloudTrail.
6. **Orchestrate** repeated processing as workflows that transform, move and load data.

## Gotchas
- Lambda duplicates computation logic and doubles the management burden; Azure presents Kappa as the
  alternative with a single path.
- Hot-path results can be less accurate; the client must choose timely or accurate.
- The size threshold for "big data" varies by organisation; do not adopt the architecture on size alone.

## Verify
- [ ] Recomputing history is possible from immutable raw data or a replayable log.
- [ ] Access policy is applied centrally at column/row level where PII exists.

## Checked
Confirmed against the Azure big data architectures page, the Delta Lake documentation home page and
the AWS Lake Formation guide served at the cited AWS URL. Removed because the cited pages did not
state them: medallion zones, 128 MB-1 GB file sizes, compaction and partitioning advice, Iceberg and
Hudi capabilities (Iceberg page body unreadable; Google big-data page is a stub, both dropped from
sources), named catalogs other than Glue, cost controls.
Method: docs-only read of cited pages, 2026-11-08
