---
id: computing-software.data-engineering.etl-pipeline-design.columnar-format-selection
name: columnar-format-selection
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, file-formats, columnar-formats, parquet, orc, avro, row-groups, schema-evolution, file-sizing]
level: practitioner
status: gated
description: "Choose Parquet, ORC, Avro, JSON or CSV per pipeline stage, and tune Parquet row groups, encodings, statistics and file sizes for pruning and fast scans."
sources:
  - https://parquet.apache.org/docs/file-format/
  - https://parquet.apache.org/docs/file-format/configurations/
  - https://orc.apache.org/docs/
  - https://avro.apache.org/docs/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Columnar format selection: Parquet, ORC, Avro

**Goal:** pick the file format that suits each stage (transport, landing, analytics) and lay out files so engines read as little as possible.

## 1. Pick by access pattern
| Format | Layout | Strength | Use for |
|---|---|---|---|
| Parquet | columnar | column pruning, predicate pushdown via stats, universal engine support | analytics storage, lake tables (Delta/Iceberg/Hudi data files) |
| ORC | columnar | similar to Parquet; strong in Hive/Trino ecosystems, built-in indexes, ACID Hive tables | Hive-centric stacks |
| Avro | row | compact, schema embedded/registry, schema evolution rules, fast whole-record writes | Kafka messages, CDC, landing raw records |
| JSON (lines) | row, text | human-readable, flexible | small feeds, debugging, raw API payloads |
| CSV | row, text | universal exchange | partner exchange only; loses types and nulls |
Default: Avro (or Protobuf) on the wire, Parquet at rest. ORC, Avro and Hive-ecosystem strengths in the table are from memory (gated: unconfirmed, source is paywalled or blocked).

## 2. Parquet internals that matter
- File → **row groups** (horizontal chunks) → **column chunks** → pages. Min/max statistics per row group (and page indexes) let engines skip data for `WHERE` filters.
- Row group size: 128 MB-1 GB uncompressed (parquet-java default `parquet.block.size` is 128 MB, the Parquet docs recommend 512 MB-1 GB row groups). Too small → overhead; too large → less skipping and more memory per reader.
- Sort or cluster data by common filter columns **before** writing so min/max ranges don't overlap — otherwise statistics skip nothing.
- Dictionary encoding for low/medium-cardinality columns happens automatically; very high-cardinality strings fall back to plain encoding.
- Bloom filters (`parquet.bloom.filter.enabled`, default false in parquet-java; the per-column `#col` suffix and the Parquet version that introduced them are unconfirmed (gated: unconfirmed, source is paywalled or blocked)) help point lookups on high-cardinality columns.
- Nested data: repetition/definition levels store structs/arrays efficiently — fine to keep nesting.

## 3. Writing well (Spark / PyArrow)
The PyArrow call was run (pyarrow 26: it wrote ZSTD, and DECIMAL(18,2) plus UTC timestamp[us] round-tripped as logical types). The Spark snippet was not run (no Spark here) (gated: unconfirmed, source is paywalled or blocked).
```python
(df.repartition("event_date").sortWithinPartitions("customer_id")
   .write.option("compression", "zstd").partitionBy("event_date").parquet("s3://lake/events/"))
```
```python
import pyarrow.parquet as pq
pq.write_table(table, "events.parquet", row_group_size=1_000_000, compression="zstd",
               use_dictionary=True, write_statistics=True)
```
Target data files of ~128 MB-1 GB; tiny files kill listing and planning time (see object storage layout).

## 4. Types and evolution
- Use logical types: DECIMAL for money (not DOUBLE), TIMESTAMP with explicit UTC adjustment, DATE. INT96 timestamps are legacy (Spark's `outputTimestampType` defaults to INT96 and documents it as non-standard) — set `TIMESTAMP_MICROS`.
- Parquet files can't be altered; evolution happens at the table layer (Delta/Iceberg) or by reader schema merge (`mergeSchema`). Avro supports writer/reader schema resolution with defaults — that's why it suits streams.
- Column renames: Iceberg/Delta column mapping by ID/name; plain Parquet datasets match by name, so renames break history.

## 5. Inspect files
```bash
parquet-tools meta file.parquet          # or: python -c "import pyarrow.parquet as pq; print(pq.ParquetFile('file.parquet').metadata)"
duckdb -c "SELECT * FROM parquet_metadata('file.parquet')"     # row groups, stats, encodings, compression
```

## Verify
- [ ] Filter queries show row groups/files skipped (engine metrics or `EXPLAIN ANALYZE`).
- [ ] Data files are 128 MB-1 GB with row groups in range.
- [ ] Money columns are DECIMAL; timestamps are not INT96.
