---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.data-lake-layout
name: data-lake-layout
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, storage-selection, data-lake-layout, medallion-architecture, partitioning, open-table-formats]
level: practitioner
status: draft
description: "Lay out data lake storage: zones (raw, cleaned, curated), path and partition conventions, file formats and sizes, open table formats, and access control."
sources: ["https://docs.aws.amazon.com/prescriptive-guidance/latest/defining-bucket-names-data-lakes/welcome.html", "https://learn.microsoft.com/azure/cloud-adoption-framework/scenarios/cloud-scale-analytics/best-practices/data-lake-zones", "https://iceberg.apache.org/docs/latest/", "https://docs.databricks.com/aws/en/lakehouse/medallion"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data lake storage layout

## Steps
1. **Zones** (medallion: bronze/silver/gold, or raw/enriched/curated): raw is immutable as
   received; cleaned is validated and conformed; curated is business-ready. Separate
   buckets/containers per zone so access and lifecycle policies differ.
2. **Path convention**: `<zone>/<domain>/<dataset>/<partition>=<value>/` e.g.
   `raw/sales/orders/ingest_date=2026-10-16/`. Lowercase, no spaces, stable names.
3. **Partitioning**: by the most common filter (usually date); avoid high-cardinality
   partitions (per customer ID) that create millions of tiny folders.
4. **File format and size**: columnar Parquet (or ORC) with compression (Snappy/ZSTD) for
   analytics; target 128 MB-1 GB files; compact small files from streaming ingestion.
5. **Table format**: Apache Iceberg, Delta Lake or Hudi for ACID, schema evolution, time travel
   and partition evolution; register in a catalogue (Glue Data Catalog, Unity Catalog, BigLake / Dataplex).
6. **Access control** at catalogue level (Lake Formation, Unity Catalog) rather than raw bucket
   policies; separate raw access (few) from curated (many).
7. **Lifecycle**: raw retention per policy, tiering of old partitions.

## Gotchas
- Small-files problem destroys query performance and increases request costs.
- Renaming paths later breaks every consumer; get conventions right first.

## Verify
- [ ] Average file size in curated tables above target.
- [ ] Every dataset registered in the catalogue with an owner.
