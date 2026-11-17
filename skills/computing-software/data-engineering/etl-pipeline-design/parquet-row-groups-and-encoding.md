---
id: computing-software.data-engineering.etl-pipeline-design.parquet-row-groups-and-encoding
name: parquet-row-groups-and-encoding
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, file-formats, parquet-row-groups, page-size, dictionary-encoding, column-statistics, bloom-filters, parquet-tools]
level: advanced
status: gated
description: "Tune Parquet files for query speed: row group and page sizes, dictionary encoding, sorting for min/max pruning, bloom filters, and inspecting files with parquet-tools or pyarrow."
sources:
  - https://parquet.apache.org/docs/file-format/configurations/
  - https://spark.apache.org/docs/latest/sql-data-sources-parquet.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Parquet row groups and encoding

**Goal:** Parquet files that let engines skip most data (row-group pruning) and read the rest efficiently.

## Structure that matters
File -> **row groups** (horizontal chunks, each with per-column min/max stats) -> column chunks -> **pages** (encoding/compression unit, optional page index).
Engines skip row groups whose min/max cannot match a filter. If data is unsorted, every row group spans the full value range and nothing is skipped.

## Sizing
- Row group: 128 MB-1 GB uncompressed (parquet-java default `parquet.block.size` = 128 MB; the Parquet docs recommend 512 MB-1 GB row groups; pyarrow `row_group_size` is in **rows**: default is the smaller of the table size and 1024*1024 rows, checked in pyarrow 26)). Larger = better compression and fewer stats; smaller = finer pruning and less memory per reader.
- Files: target 256 MB-1 GB; avoid many tiny files with tiny row groups (each file has footer overhead).
- Page size: parquet-java default `parquet.page.size` is 1 MB (the format docs recommend 8 KB data pages, smaller pages = finer reads, larger = less header overhead); page indexes (column index/offset index) allow page-level skipping in engines that support them.

## Sorting for pruning
```python
df.repartition("event_date").sortWithinPartitions("customer_id", "event_ts") \
  .write.partitionBy("event_date").parquet(path)
```
Sort by the most common selective filter column(s) within partitions. Table formats do this with `OPTIMIZE ... ZORDER BY`, liquid clustering, or Iceberg sort orders.

## Encodings
- **Dictionary encoding** (default on): excellent for low-cardinality strings; falls back to plain when dictionary exceeds `parquet.dictionary.page.size` (1 MB default, parquet-java). High-cardinality IDs fall back automatically.
- Delta encodings for sorted integers/timestamps (`DELTA_BINARY_PACKED`) in writers that support v2 pages.
- Compression on top: zstd (best ratio/speed trade-off in a pyarrow test), snappy (fast, default in Spark; pyarrow also defaults to snappy; parquet-java defaults to uncompressed), gzip (slow to write).

## Bloom filters
For equality lookups on high-cardinality columns (ids) where min/max is useless:
```python
df.write.option("parquet.bloom.filter.enabled#customer_id", "true") \
        .option("parquet.bloom.filter.expected.ndv#customer_id", "5000000").parquet(path)
```
The Parquet configuration page does not document the bloom options; the option names above are parquet-java settings (`parquet.bloom.filter.enabled` defaults to false; `expected.ndv` has no default). Reader support (Spark 3.2+, Trino, DuckDB) is unconfirmed here (gated: unconfirmed, source is paywalled or blocked). Supported readers skip row groups whose bloom filter excludes the value.

## Inspect files
```python
import pyarrow.parquet as pq
md = pq.ParquetFile("part-0001.parquet").metadata
print(md.num_row_groups, md.row_group(0).num_rows, md.row_group(0).total_byte_size)
print(md.row_group(0).column(3).statistics)       # min/max/null_count
print(md.row_group(0).column(3).encodings, md.row_group(0).column(3).compression)
```
CLI: `parquet-tools meta file.parquet` / `parquet-cli meta`, DuckDB `select * from parquet_metadata('file.parquet')`.

## Gotchas
- Timestamps: Spark's `spark.sql.parquet.outputTimestampType` defaults to INT96 (non-standard); set it to `TIMESTAMP_MICROS` for interoperability.
- Statistics for strings may be truncated or missing in old writers, disabling pruning.
- Decimals: pyarrow stored DECIMAL(18,2) as FIXED_LEN_BYTE_ARRAY(8) in a test; other writers (for example Spark) may pick INT32/INT64 for small precisions, so check what your writer emits (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] `parquet_metadata` shows narrow min/max ranges per row group for the sort column.
- [ ] Query on that column reads a small fraction of bytes (engine metrics: bytes scanned / row groups skipped).
