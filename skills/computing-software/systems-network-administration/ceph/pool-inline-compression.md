---
id: computing-software.systems-network-administration.ceph.pool-inline-compression
name: pool-inline-compression
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, pool, compression, bluestore, zstd, lz4]
level: practitioner
status: docs-checked
description: "Enable BlueStore inline compression on one Ceph pool with compression_algorithm, compression_mode and blob size keys."
sources:
  - https://docs.ceph.com/en/latest/rados/operations/pools/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pool-level keys override the global BlueStore settings (`bluestore_compression_algorithm`, `bluestore_compression_mode` and the blob size options), so you can compress one pool without touching the rest:

```
ceph osd pool set {pool-name} compression_algorithm zstd
ceph osd pool set {pool-name} compression_mode aggressive
```

Valid values:

- `compression_algorithm`: `lz4`, `snappy`, `zlib`, `zstd`
- `compression_mode`: `none`, `passive`, `aggressive`, `force`
- `compression_min_blob_size`: chunks smaller than this are not compressed
- `compression_max_blob_size`: larger chunks are split into blobs of at most this size before compression

Reading results:

- Compressed pool statistics appear in `ceph df detail`.
- Most API and CLI calls still show the original uncompressed object sizes. For example, an RGW bucket placed directly in a compressed RADOS pool, with no RGW-level compression, reports uncompressed sizes through `radosgw-admin`.

To read a value back use `ceph osd pool get {pool-name} compression_mode`. To turn compression off for the pool set `compression_mode none`.

## Checked

2026-11-03. Confirmed against: the Ceph Pools page (docs.ceph.com/en/latest/rados/operations/pools/): compression_algorithm, compression_mode, blob size keys and the ceph df detail note.

Removed: the claim that settings affect only data written after the change.

Method: documentation only; no commands were run.
