---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.tiered-storage-disk-types
name: tiered-storage-disk-types
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [disk-type, ssd-hdd, dir-idx, tiered-storage]
level: advanced
status: docs-checked
description: "Place hot and cold data on different disks: volume -disk tags, path rules with fs.configure -disk, and a fast index directory."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/Tiered-Storage
  - https://github.com/seaweedfs/seaweedfs/wiki/Cloud-Tier
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# tiered storage disk types

Tiers run from NVMe to SSD to HDD to cloud. Volume reads and writes stay O(1) disk seeks.

Tag disks on the volume server (one tag per `-dir`):
```bash
weed volume -max=10000 -disk=hdd,ssd -port=8080 -dir=/large_data,/fast_data -compactionMBps=40 -minFreeSpacePercent=7
```
Route data by path in `weed shell`:
```
fs.configure -locationPrefix=/buckets/ssd_ -disk=ssd -apply
```
So buckets or collections starting with `ssd_` allocate on SSD, the rest on HDD. Custom lower-case tags work too (`ssd1`, `hdd2`, `nvme`, `raid6`).

Speed up the index: `weed volume -dir.idx=/fast/disk/dir`.

Cloud Tier is different from Cloud Drive: tiering moves whole volume files to the cloud, they are unusable outside SeaweedFS, and filer data encryption applies transparently. Cloud Drive mounts a bucket as files and cannot encrypt.

Verify: upload under `/buckets/ssd_x/` and check which disk type holds the new volume.

## Checked
Checked 2026-11-09: the tier ladder, `-disk` and `-dir` pairing, `fs.configure -locationPrefix -disk -apply`, custom lower-case tags, `-dir.idx`, and the Cloud Tier versus Cloud Drive comparison match the pages. Removed the claim that the master assign API takes `disk=` (not on either page).
Method: docs-checked 2026-11-09 against the SeaweedFS wiki pages Tiered-Storage and Cloud-Tier, both read in full from a local clone of the wiki.
