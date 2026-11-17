---
id: computing-software.database-administration.clickhouse.compression-codecs-per-column
name: compression-codecs-per-column
category: computing-software
field: database-administration
product: clickhouse
tags: [database-administration, clickhouse, compression, codec, delta, zstd]
level: practitioner
status: docs-checked
description: "Tune ClickHouse column compression with CODEC choices (LZ4, ZSTD, Delta, DoubleDelta, T64) and measure ratios from system.columns."
sources:
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/data-compression/compression-in-clickhouse.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# compression codecs per column
ClickHouse compresses each column separately; sorted, similar values sit next to each other so ratios are high. Measure per column:
```sql
SELECT name,
  formatReadableSize(sum(data_compressed_bytes))   AS compressed_size,
  formatReadableSize(sum(data_uncompressed_bytes)) AS uncompressed_size,
  round(sum(data_uncompressed_bytes) / sum(data_compressed_bytes), 2) AS ratio
FROM system.columns WHERE table = 'posts' GROUP BY name;
```
ZSTD usually compresses harder than LZ4 but costs more CPU. In ClickHouse Cloud the default is ZSTD(1).

Set codecs per column, chaining a specialised codec with a general one:
```sql
CREATE TABLE metrics
(
  ts   DateTime CODEC(Delta, ZSTD),
  val  UInt32   CODEC(T64, ZSTD(3)),
  host LowCardinality(String)
)
ENGINE = MergeTree ORDER BY (host, ts);
```
Recommendations (in the docs' order of importance):
- Delta (or DoubleDelta when deltas are not small) for monotonic sequences such as timestamps and counters; delta-encoded data compresses better under ZSTD, and with ZSTD other codecs rarely add more.
- Prefer LZ4 over ZSTD if the ratio is comparable, since decompression is faster and costs less CPU.
- T64 for sparse data or small value ranges per block; avoid it for random numbers.

Part type matters for small tables: compact parts (below `min_bytes_for_wide_part`, default 10485760 bytes) store columns together, so per-column sizes in `system.columns` differ from wide parts.

The docs add that ZSTD levels above 3 rarely repay the slower inserts, and that Gorilla and T64 are worth trying for data with an unknown pattern.

## Checked
2026-11-03. Confirmed against the ClickHouse docs page "Compression in ClickHouse": per-column sizing, the Delta, DoubleDelta, ZSTD, LZ4 and T64 recommendations, compact versus wide parts with `min_bytes_for_wide_part` default 10485760, and the Cloud ZSTD(1) default. Removed: the open-source default claim, the ALTER MODIFY COLUMN behaviour and the Verify step.
Method: documentation only; no commands were run.
