---
id: computing-software.data-engineering.apache-pinot.apache-pinot-forward-index-raw-compression-codecs
name: apache-pinot-forward-index-raw-compression-codecs
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, forward-index, raw-index, compressioncodec, chunkcompressiontype, rawindexwriterversion, targetdocsperchunk, targetmaxchunksize, codecspec, pinot-forward-index-default-compression-codec, nodictionarycolumns]
level: advanced
status: docs-checked
description: "Tuning RAW (no dictionary) forward indexes: compressionCodec values, chunk sizing keys, rawIndexWriterVersion, codecSpec pipelines and the cluster default codec setting."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/build-with-pinot/indexing/forward-index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RAW forward index compression codecs

A RAW forward index stores values directly instead of through a dictionary. Configure it in `fieldConfigList`:
```
{ "name": "payload", "encodingType": "RAW",
  "indexes": { "forward": { "compressionCodec": "ZSTANDARD" } } }
```

Parameters in `indexes.forward` (defaults in brackets):
- `compressionCodec` [null]: `PASS_THROUGH` (none), `SNAPPY`, `ZSTANDARD` (high ratio, slower than Snappy), `LZ4` (fast, balanced), `GZIP` (since 1.2.0). `chunkCompressionType` is the older name, replaced since 1.2.0. With the JSON null default, metrics use PASS_THROUGH and other columns use the configured default codec (LZ4 unless overridden).
- `rawIndexWriterVersion` [4]: the latest version selectable is 6. V6 (since 1.3.0) delta-encodes chunk headers.
- `targetDocsPerChunk` [1000] and `targetMaxChunkSize` [1MB]. For writer version 4 the chunk size is min(longest document x targetDocsPerChunk, targetMaxChunkSize); a negative targetDocsPerChunk disables dynamic sizing. Documents larger than targetMaxChunkSize get their own chunk.
- `deriveNumDocsPerChunk` [false]: for variable-length types (string, big decimal, bytes), true uses a heuristic doc count.
- `codecSpec` [null]: codec pipeline for a single-value, fixed-width RAW column, for example `"DELTA,ZSTD(3)"`. Any non-null value selects the V7 format and cannot be combined with `compressionCodec`. With V7, `targetDocsPerChunk` applies but `rawIndexWriterVersion`, `deriveNumDocsPerChunk` and `targetMaxChunkSize` do not. Upgrade every component that builds or reads segments before enabling it; to roll back, remove `codecSpec` and regenerate or re-push segments.
- `dictIdCompressionType` [null]: for dictionary-encoded forward indexes; `MV_ENTRY_DICT` adds a second dictionary level for repeated multi-value entries.

Cluster default: set `pinot.forward.index.default.compression.codec` (PASS_THROUGH, SNAPPY, ZSTANDARD or LZ4; case-insensitive) as the fallback for non-metric RAW columns with no explicit codec. It is read at service startup (restart after changing); explicit per-column codecs win; metric columns stay PASS_THROUGH; existing indexes are not rewritten just by a reload. Standalone, Spark/Hadoop batch ingestion and `pinot-admin CreateSegment` do not inherit it. Similar operator-managed defaults exist for `pinot.forward.index.default.raw.index.writer.version`, `.target.max.chunk.size` and `.target.docs.per.chunk`, used when the table config does not set the property.

## Checked

Confirmed against the Pinot docs page "Forward index": codec values and meanings, parameter defaults, V6 and V7 behaviour, cluster default codec rules and the related default properties. Removed the unsourced rule of thumb about codecs per data type and chunk size trade-offs.

Method: docs-only read of cited pages, 2026-11-08
