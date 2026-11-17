---
id: computing-software.database-administration.dragonfly.enable-ssd-tiering
name: enable-ssd-tiering
category: computing-software
field: database-administration
product: dragonfly
tags: [ssd-tiering, tiered-prefix, io-uring, nvme, dragonfly]
level: advanced
status: docs-checked
description: "Turn on Dragonfly SSD data tiering with tiered_prefix: what is offloaded, kernel and io_uring requirements, and current limits."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/tiering.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
SSD data tiering (first official release v1.35) uses an SSD/NVMe device as a second storage tier. Docs claim potentially a 2x-5x memory reduction with sub-millisecond average latency.

What is offloaded: large string values (over 64 characters by default). Shorter strings, other data types and the primary hashtable index stay in memory. Offloaded data is fetched from SSD on access. Write, delete and expire operations are handled in memory.

Enable:

```shell
./dragonfly --maxmemory=20G --tiered_prefix=/mnt/fast-ssd/dragonfly-tiered-file
```

`tiered_prefix` (path plus base name) also turns the feature on. Dragonfly checks free space on that partition to set maximum capacity and creates one storage file per proactor thread. New values are placed on disk immediately after creation.

Requirements:

- Linux kernel 5.19 or higher with `io_uring` enabled (critical).
- A fast SSD at the path; for cloud, instances with local SSD. The docs recommend `r6gd`/`m6gd` or higher families on AWS; any instance with local SSD on GCP.

Limits:

- Supported for strings; experimental for list nodes and mutable hash commands (`--tiered_experimental_hash_support`). Not supported for BitMap and HyperLogLog.
- With experimental hash offloading, database 0 hashes are not offloaded while a Search index on hashes exists.

## Checked

2026-11-04. Confirmed in the SSD Data Tiering page (v1.35, 64-character default, `tiered_prefix`, one file per proactor thread, kernel 5.19 and `io_uring`, instance families, string-only support, hash and Search note). Nothing removed.

Method: documentation only; no commands were run.
