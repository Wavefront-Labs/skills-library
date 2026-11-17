---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.weed-mount-write-buffer-quota
name: weed-mount-write-buffer-quota
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [writebuffersizemb, collectionquotamb, fuse-maxbackground, write-buffer, collection-quota, df-logical]
level: advanced
status: docs-checked
description: "Tune weed mount: bound the write buffer, move the swap off /tmp, raise FUSE concurrency, and cap a collection with -collectionQuotaMB (ENOSPC)."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/FUSE-Mount
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# weed mount write buffer quota

Bound write memory/swap (buffers are in RAM for sequential writes or a swap file under `-cacheDir`, usually /tmp). If volume servers stall, uploads queue and the buffer grows, so cap it:
```bash
weed mount -filer=localhost:8888 -dir=/mnt/seaweedfs -filer.path=/   -cacheDirWrite=/var/cache/seaweedfs -writeBufferSizeMB=2048 -chunkSizeLimitMB=32 -concurrentWriters=128
```
Kernel FUSE concurrency: `-fuse.maxBackground=2048`, optionally `-fuse.congestionThreshold=1900`.

Collection quota:
```bash
weed mount -filer=localhost:8888 -dir=/mnt/seaweedfs -filer.path=/buckets/data -collection=data -collectionQuotaMB=5120
```
At the limit, writes, creates, links and xattr updates fail with `ENOSPC`; reads and deletes still work, so you can free space.

Facts and gotchas:
- Quota is per collection, shared by all mounts writing it, and measured including replicas and EC shards (add `-df.logical` to count logical bytes).
- Enforcement is mount-side, not authoritative; a client without a quota is not restricted, and two mounts can briefly overshoot.
- Changing it at runtime goes over the mount gRPC socket; polling only starts if a quota was set at mount time.
- The CSI driver uses this for PVC size; it differs from S3 bucket quota.

Verify: fill past the limit and expect ENOSPC.

## Checked
Checked 2026-11-09: the write-buffer, FUSE concurrency and collection-quota sections of the FUSE-Mount page match every flag, example and gotcha here. Nothing removed.
Method: docs-checked 2026-11-09 against the SeaweedFS wiki page FUSE-Mount, read in full from a local clone of the wiki.
