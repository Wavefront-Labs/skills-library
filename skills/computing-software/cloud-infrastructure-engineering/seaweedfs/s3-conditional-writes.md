---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.s3-conditional-writes
name: s3-conditional-writes
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [if-match, if-none-match, optimistic-locking, conditional-write]
level: advanced
status: docs-checked
description: "Use S3 conditional headers on SeaweedFS for compare-and-create and optimistic locking; checks are atomic cluster-wide, plus copy-source conditions."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/S3-Conditional-Operations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# s3 conditional writes

The precondition and the write are applied atomically under one lock on the filer that owns the key, so two clients racing an `If-Match` update never both succeed, whichever filer they hit.

Headers on the target object (GET, HEAD, PUT, POST/CompleteMultipartUpload, COPY; DELETE accepts only `If-Match`):
- `If-Match`: ETag, `*` matches any existing object, comma lists honored
- `If-None-Match`: `*` succeeds only if the object does not exist (compare-and-create)
- `If-Modified-Since`, `If-Unmodified-Since`: RFC 1123 dates

CopyObject and UploadPartCopy also take source conditions: `x-amz-copy-source-if-match`, `-if-none-match`, `-if-modified-since`, `-if-unmodified-since`. They are independent of the destination headers.

```bash
curl -X PUT -H "If-None-Match: *" --data "New file content" http://localhost:8333/mybucket/newfile.txt
```
Evaluation order follows RFC 7232 and AWS S3: If-Match, then If-Unmodified-Since (ignored if If-Match is present), If-None-Match, then If-Modified-Since (ignored if If-None-Match is present). `If-Range` is not supported.

Of any number of concurrent creates with `If-None-Match: *`, one succeeds and the rest get 412 Precondition Failed. Use it for distributed leader election, exclusive file creation and idempotent uploads. A 304 means GET/HEAD found the object unchanged; a malformed date gives 400.

## Checked

2026-11-04. Confirmed against the SeaweedFS wiki page S3 Conditional Operations: atomic cluster-wide check, header table, copy-source headers, evaluation order, status codes. Replaced the aws s3api example (its `--if-none-match` and `--body` usage is not on the page) with the page's curl example, and removed single-writer manifests and the Verify line.
Method: documentation only; no commands were run.
