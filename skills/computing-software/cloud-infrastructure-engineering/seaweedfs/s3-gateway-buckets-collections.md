---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.s3-gateway-buckets-collections
name: s3-gateway-buckets-collections
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [weed-s3, s3-gateway, buckets]
level: practitioner
status: docs-checked
description: "Run the stateless SeaweedFS S3 gateway (weed s3, weed server -s3, weed filer -s3), how buckets map to collections, and how to keep many buckets affordable."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/Amazon-S3-API
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# s3 gateway buckets collections

`weed s3` is a stateless bridge from the S3 API to the filer. Shortcuts: `weed server -s3` (master, volume, filer and S3) and `weed filer -s3` (filer plus S3). Run several S3 instances against one filer to scale out; the easiest way is `weed filer -s3` on each filer.

Buckets: each bucket is one collection, stored at `/buckets/<name>`. From version 3.51 the collection is `filerGroup_bucketname`, or just `bucketname` without a filer group. Deleting a bucket deletes its collection, which is fast.

Many buckets: one collection usually uses about 7 volumes of 30GB each, so disk fills quickly. Keep volumes small and limit growth:
```bash
weed master -volumeSizeLimitMB=1024
# in weed shell
fs.configure -locationPrefix=/buckets/ -volumeGrowthCount=1 -apply
fs.configure -locationPrefix=/buckets/ -replication=001 -volumeGrowthCount=2 -apply
```
With replication, make the growth count a multiple of the number of replicas.

The page lists every S3 operation with its support status; check it before relying on an uncommon API.

## Checked

2026-11-04. Confirmed against the SeaweedFS wiki page Amazon S3 API: stateless gateway, the three start commands, bucket-per-collection at /buckets, naming from 3.51, 7 volumes of 30GB, `-volumeSizeLimitMB`, the two fs.configure examples, multiple S3 nodes. Removed the Verify line (`collection.list` is not on the page).
Method: documentation only; no commands were run.
