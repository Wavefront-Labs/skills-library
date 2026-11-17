---
id: computing-software.database-administration.cassandra.compression-settings
name: compression-settings
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, chunk-length-kb, compression-ratio, zstd, sstable-compression, lz4-compressor, zstd-compression, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Chunk length and algorithms"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/managing/operating/compression.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SSTable compression

Goal: trade CPU for disk and I/O.
- `compression = {'class': 'LZ4Compressor', 'chunk_length_in_kb': 64}`; the defaults are class `LZ4Compressor` and `chunk_length_in_kb` 16KiB.
- On reads Cassandra decompresses the whole chunk, so chunk size matters; `ZstdCompressor` is available from 4.0, `ZstdDictionaryCompressor` from 6.0, while Snappy and Deflate are kept for backwards compatibility.
- A new setting applies to new SSTables; rebuild old ones with `nodetool scrub` or `nodetool upgradesstables -a`.
- The ratio is the `SSTable Compression Ratio` field of `nodetool tablestats`.
Verify: read latency and disk size compared before and after.

## Checked

2026-11-02. Checked against the Compression page (table of algorithms and versions, option defaults, example statements, ratio field of tablestats, rebuild after changing). Removed: the claim that smaller chunks help random reads and larger chunks compress better (not stated).

Method: documentation only; no commands were run.
