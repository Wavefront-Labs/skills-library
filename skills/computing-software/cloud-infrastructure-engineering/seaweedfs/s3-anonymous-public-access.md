---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.s3-anonymous-public-access
name: s3-anonymous-public-access
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [public-bucket, weed-shell, anonymous, public-read, s3-bucket-access]
level: practitioner
status: docs-checked
description: "Grant or revoke unauthenticated S3 read/list access on a bucket with s3.anonymous.set or s3.bucket.access, and verify it with curl and --no-sign-request."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/Simplest-S3-Bucket-and-User-Setup
  - https://github.com/seaweedfs/seaweedfs/wiki/S3-Bucket-Policies
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# s3 anonymous public access

Goal: serve public assets from one bucket without opening the rest.

In `weed shell`:
```
> s3.anonymous.set -bucket my-bucket -access Read,List
> s3.anonymous.set -bucket my-bucket -access none      # make private again
> s3.anonymous.list
> s3.anonymous.get -bucket my-bucket
```
Actions: `Read`, `Write`, `List`, `Tagging`, `Admin`, comma-combined; `none` revokes.

Equivalent per-user form (user auto-created if missing):
```
> s3.bucket.access -name my-bucket -user anonymous -access Read,List
> s3.bucket.access -name my-bucket -user anonymous
```
Actions are stored on the identity scoped as `Action:bucket`.

Verify:
```bash
aws --endpoint-url http://localhost:8333 s3 ls s3://my-bucket/ --no-sign-request
curl http://localhost:8333/my-bucket/file.txt
```
After `none`, unauthenticated requests to the bucket are rejected.

## Checked

2026-11-04. Confirmed against the SeaweedFS wiki pages Simplest S3 Bucket and User Setup (s3.anonymous.set/list/get, actions, verify commands) and S3 Bucket Policies (s3.bucket.access, user auto-created, Action:bucket scoping). Removed the generic closing tip about Write.
Method: documentation only; no commands were run.
