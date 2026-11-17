---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.s3-bucket-quota-enforce
name: s3-bucket-quota-enforce
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [bucket-quota, s3-bucket-quota, readonly-bucket, quota-enforce, read-only-bucket]
level: practitioner
status: docs-checked
description: "Set bucket size quotas with s3.bucket.quota and enforce them via s3.bucket.quota.enforce, which flips over-quota buckets to read-only."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/S3-Bucket-Quota
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# s3 bucket quota enforce

Usage is cheap to read because each bucket is one collection. In `weed shell`:
```
> s3.bucket.list
  b1	size:527971104	file:151
> s3.bucket.quota -name b1 -sizeMB 15
> s3.bucket.quota.enforce -apply
  b1 ... usage:3356.75%
    changing bucket b1 to read only!
```
Sizes are actual disk use including replicas.

Configuration and enforcement are separate: set quotas with `s3.bucket.quota` (set, remove, enable, disable), then run `s3.bucket.quota.enforce -apply` periodically, for example as a script in `master.toml`. Over-quota buckets get `readOnly` set; the filer then denies create and update requests for that bucket. The flag is stored in filer config for `locationPrefix=/buckets/b1/` and visible with `fs.configure`.

Over-quota writes (PutObject, UploadPart, CopyObject, UploadPartCopy) fail with 403 AccessDenied, not 500; deletes and reads still work.

This is server-side. The FUSE mount `-collectionQuotaMB` is a different mechanism, enforced mount-side.

## Checked

2026-11-04. Confirmed against the SeaweedFS wiki page S3 Bucket Quota: commands, sample output, readOnly flag at locationPrefix, 403 AccessDenied, distinction from `-collectionQuotaMB`. Removed the unconfirmed claim that a bucket can exceed quota between runs (the page only says to run enforcement regularly) and the Verify line.
Method: documentation only; no commands were run.
