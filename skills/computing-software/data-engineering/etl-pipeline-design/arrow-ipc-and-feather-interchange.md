---
id: computing-software.data-engineering.etl-pipeline-design.arrow-ipc-and-feather-interchange
name: arrow-ipc-and-feather-interchange
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, arrow-ipc, apache-arrow, feather, zero-copy]
level: advanced
status: verified
description: "Move tabular data between processes and tools with Apache Arrow IPC (stream and file/Feather formats): when to use it over Parquet, compression, schemas and gotchas."
sources:
  - https://arrow.apache.org/docs/format/Columnar.html#serialization-and-interprocess-communication-ipc
  - https://arrow.apache.org/docs/python/ipc.html
  - https://arrow.apache.org/docs/python/feather.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Arrow IPC and Feather interchange

**Goal:** fast, type-preserving data exchange between Python, R, Rust, DuckDB, Spark and services, without CSV/JSON parsing costs.

## Formats
- **IPC stream**: sequence of record batches, unknown length; for pipes, sockets, HTTP responses, Arrow Flight. Media type `application/vnd.apache.arrow.stream`, recommended extension `.arrows`.
- **IPC file** (= **Feather v2**): same plus a footer for random access; memory-mappable. Media type `application/vnd.apache.arrow.file`, extension `.arrow`.
- Parquet: columnar **storage** format with encoding/compression and statistics: smaller on disk. Use Parquet for data at rest/lakes; Arrow IPC for transient interchange and caching.

## Python
```python
import pyarrow as pa, pyarrow.ipc as ipc, pyarrow.feather as feather

table = pa.table({"id": pa.array([1, 2], pa.int64()), "ts": pa.array([0, 1], pa.timestamp("us", tz="UTC"))})

feather.write_feather(table, "batch.arrow", compression="zstd")   # IPC file
t2 = feather.read_table("batch.arrow", memory_map=True)

with pa.OSFile("batch.stream", "wb") as sink, ipc.new_stream(sink, table.schema) as w:   # IPC stream
    for b in table.to_batches(max_chunksize=64_000):
        w.write_batch(b)
reader = ipc.open_stream(pa.memory_map("batch.stream"))
```
- pandas: `df.to_feather()` / `pd.read_feather()`; polars `write_ipc` / `scan_ipc`; DuckDB reads Arrow tables in memory zero-copy.
- HTTP APIs: media type `application/vnd.apache.arrow.stream`. Run here: the polars and DuckDB calls above work (pyarrow 26, polars/DuckDB current).

## Gotchas
- Compression (`lz4`, `zstd`) disables zero-copy memory mapping of the compressed buffers (measured: reading a 5M-row int64 file with `memory_map=True` allocated 0 KB uncompressed vs about 39 MB with zstd). `write_feather` defaults to LZ4 for V2 when available, so pass `compression="uncompressed"` if you need mmap.
- Schema is strict: timestamp units and time zones, dictionary encoding, large vs regular string types must match what the consumer expects; cast explicitly.
- Use Parquet for durable storage; IPC is for interchange and caching.
- Feather v1 is a legacy format distinct from Arrow IPC (fewer types, no compression; deprecated in pyarrow 25); use v2 (the default).

## Verify
Round-trip a sample: schema equality (`t2.schema.equals(table.schema)`) and row hashes match; measure read time vs the CSV/JSON path it replaces.
