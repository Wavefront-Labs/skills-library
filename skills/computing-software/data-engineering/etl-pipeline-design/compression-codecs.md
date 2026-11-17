---
id: computing-software.data-engineering.etl-pipeline-design.compression-codecs
name: compression-codecs
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, file-formats, compression-codecs, zstd, snappy, gzip, lz4, splittable-compression, storage-cost]
level: practitioner
status: gated
description: "Choose compression codecs for data files and streams: zstd vs snappy vs gzip vs lz4 trade-offs, splittability of text files, compression levels, and measuring ratio vs CPU."
sources:
  - https://parquet.apache.org/docs/file-format/data-pages/compression/
  - https://facebook.github.io/zstd/
  - https://spark.apache.org/docs/latest/sql-data-sources-parquet.html#configuration
  - https://kafka.apache.org/documentation/#producerconfigs_compression.type
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compression codecs

**Goal:** smaller files and network transfers without making reads or writes CPU-bound, and without creating unsplittable files that serialise processing.

## 1. Codec characteristics
Spark, Delta, Hive/Impala, ClickHouse and codec-support claims below were not run here (gated: unconfirmed, source is paywalled or blocked); the Parquet codec list, Kafka and Iceberg settings and the pyarrow numbers were checked.
| Codec | Ratio | Compress speed | Decompress speed | Notes |
|---|---|---|---|---|
| Snappy | low-medium | very fast | very fast | Spark's Parquet default (`spark.sql.parquet.compression.codec=snappy`) |
| LZ4 | low-medium | very fast | fastest | ClickHouse default; in Parquet use `LZ4_RAW` (the older `LZ4` codec is deprecated in the spec) |
| Zstd | high | fast (level 1-3) to slow (19+) | fast | best general choice today; tunable levels |
| Gzip/Deflate | high | slow | medium | universal compatibility |
| Bzip2 | very high | very slow | slow | splittable, legacy |
| Brotli | high | slow | fast | rarely used in data pipelines |
Measured with pyarrow 26 on 2M rows (int, low-cardinality string, float, random hex): none 58 MB, snappy 44, lz4 46, zstd 23, gzip 27 (write 16 s vs 0.45 s for zstd), brotli 26 (write 4.5 s). Reads were 0.04-0.13 s for all. Your data will differ.
Rule of thumb: **zstd** (level 1-3) for Parquet/ORC at rest and Kafka; snappy/lz4 when CPU is the bottleneck; gzip only for exchange with systems that need it.

## 2. Splittability (text formats)
A single `.csv.gz` or `.json.gz` file **cannot be split** — one task reads the whole file. A 20 GB gzip CSV = one core for the whole read.
- Columnar formats (Parquet/ORC/Avro) compress per page/block internally, so files stay splittable with any codec.
- For text exchange, produce many moderately sized compressed files (e.g. 100-500 MB each) instead of one huge one; bzip2 is splittable but slow.
- Uncompressed ingest of a huge gzip file: decompress once in parallel-friendly form (rewrite to Parquet) before heavy processing.

## 3. Setting codecs
```python
spark.conf.set("spark.sql.parquet.compression.codec", "zstd")            # Spark default is snappy
df.write.option("compression", "zstd").parquet(path)
```
```sql
-- Iceberg table property (Iceberg's own default is already zstd; Delta uses a different property)
ALTER TABLE t SET TBLPROPERTIES ('write.parquet.compression-codec' = 'zstd');
```
```properties
# Kafka producer (default compression.type is none; valid: none, gzip, snappy, lz4, zstd)
# The broker/topic-level setting `compression.type=producer` keeps whatever the producer used.
compression.type=zstd
linger.ms=20          # producer default is 5 ms
batch.size=131072     # producer default is 16384 bytes
```
Larger batches compress better — compression and batching tuning go together.

## 4. Measure, don't guess
Take a representative sample (1-10 GB), write it with each candidate codec/level, and record: output size, write time, read time of a typical query. Storage is cheap relative to compute for hot tables; for cold archives use higher zstd levels.
```bash
for c in snappy zstd gzip; do python write_sample.py --codec $c; done   # compare size + timings
```

## 5. Gotchas
- Re-compressing already-compressed data (images, encrypted blobs) wastes CPU — store as-is.
- Parquet column chunks of high-entropy columns (UUIDs, hashes) barely compress; dictionary encoding helps low-cardinality columns more than codec choice.
- Old readers may not support newer codecs (zstd in very old Hive/Impala, LZ4_RAW) — check every consumer.

## Verify
- [ ] Codec is set explicitly for each sink (not relying on version defaults).
- [ ] No pipeline reads giant single gzip text files.
- [ ] Benchmarks of size/time are recorded for the chosen codec.
