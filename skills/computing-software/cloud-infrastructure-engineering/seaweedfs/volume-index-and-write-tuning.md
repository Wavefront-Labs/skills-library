---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.volume-index-and-write-tuning
name: volume-index-and-write-tuning
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [volumepreallocate, leveldb-index, vol-grow, preallocate]
level: advanced
status: docs-checked
description: "Tune SeaweedFS volumes: leveldb index flavors, preallocation, growing writable volumes via /vol/grow, and master volumeSizeLimitMB."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/Optimization
  - https://github.com/seaweedfs/seaweedfs/wiki/Tiered-Storage
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# volume index and write tuning

Index type: the default is in-memory (fast, slow startup with many files). `weed volume -index=leveldb` starts much faster at slightly slower access. Flavors: `leveldb` (4MB total), `leveldbMedium` (8MB), `leveldbLarge` (12MB).

Index location: `weed volume -dir.idx=/fast/disk/dir` (or `weed server -volume.dir.idx=...`) puts the index on a fast SSD. For existing data, stop the server, move the `.idx` files, restart.

Preallocate disk (Linux XFS, ext4, Btrfs) for contiguous blocks, on the master:
```bash
weed master -volumePreallocate -volumeSizeLimitMB=30000
```
Concurrent writes: with no replication there are 7 writable volumes by default. Pre-create more:
```bash
curl "http://localhost:9333/vol/grow?count=12&replication=001"
curl "http://localhost:9333/vol/grow?count=12&collection=benchmark"
```
`count=12` with `001` consumes 24 physical volumes.

Verify: the master UI shows the new writable volumes after `vol/grow`.

## Checked
Checked 2026-11-09: leveldb flavors and memory sizes, `-dir.idx`, `-volumePreallocate` with `-volumeSizeLimitMB`, the 7 default writable volumes, the `/vol/grow` examples and the 001 doubling to 24 physical volumes match the Optimization and Tiered-Storage pages. Removed the unexplained `-compactionMBps` advice.
Method: docs-checked 2026-11-09 against the SeaweedFS wiki pages Optimization and Tiered-Storage, both read in full from a local clone of the wiki.
