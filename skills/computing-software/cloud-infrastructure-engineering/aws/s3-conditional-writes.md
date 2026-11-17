---
id: computing-software.cloud-infrastructure-engineering.aws.s3-conditional-writes
name: s3-conditional-writes
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, conditional-writes, if-none-match, if-match, optimistic-concurrency, distributed-locking]
level: advanced
status: docs-checked
description: "Use S3 conditional writes (If-None-Match create-only, If-Match ETag compare-and-swap) to stop clobbering, build leases and manifests, and enforce them with bucket policy."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/conditional-writes.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/conditional-writes-enforce.html", "https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutObject.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# S3 conditional writes

S3 supports preconditions on writes: `If-None-Match: *` (create only if the
key does not exist) and `If-Match: <etag>` (overwrite only if the current object still has
that ETag). Both work on `PutObject`, `CompleteMultipartUpload` and `CopyObject`
(destination). Requests must be signed with Signature Version 4. `If-None-Match` needs `s3:PutObject`; `If-Match` needs
`s3:PutObject` and `s3:GetObject`.

## 1. Create-only (no overwrite)
```bash
aws s3api put-object --bucket b --key locks/job-2026-10-18 --body lease.json --if-none-match '*'
```
- Success: you created it.
- `412 Precondition Failed`: it already exists, someone else won.
- `409 ConditionalRequestConflict`: a conflicting operation happened during the write (for example a concurrent delete); retry the upload
  (for `CompleteMultipartUpload`, re-initiate the multipart upload with `CreateMultipartUpload`). With `If-Match`, a missing object, a delete marker as the current version, or a concurrent delete returns `404 Not Found`.
Use cases: idempotent job markers, "first writer wins" uploads, write-once log segments,
preventing accidental overwrite of user files.

## 2. Compare-and-swap with If-Match
```bash
ETAG=$(aws s3api head-object --bucket b --key state/manifest.json --query ETag --output text)
# modify locally, then:
aws s3api put-object --bucket b --key state/manifest.json --body manifest.json --if-match "$ETAG"
```
If another writer updated the manifest since you read it, you get 412: re-read, re-apply
your change, retry. The first conditional write to finish wins. This gives optimistic concurrency for small shared state (table
format manifests, catalogue pointers, config) without DynamoDB.

boto3:
```python
try:
    s3.put_object(Bucket=b, Key=k, Body=data, IfMatch=etag)
except s3.exceptions.ClientError as e:
    if e.response["Error"]["Code"] in ("PreconditionFailed", "ConditionalRequestConflict"):
        ...  # reload and retry with backoff
    else:
        raise
```

## 3. Multipart uploads
Pass the condition on `CompleteMultipartUpload`. The check happens at completion and conditional writes do not consider in-progress
multipart uploads, so a long upload can lose the race at the end (412) if another client wrote the key meanwhile.

## 4. Leases and locks (pattern)
1. Acquire: `PutObject locks/<name>` with `If-None-Match: *`, body = owner + expiry.
2. Renew: read ETag, `PutObject` with `If-Match` (still owner).
3. Release: `DeleteObject` (the S3 API model also accepts `If-Match` on `DeleteObject`; check your SDK version), or let
   expiry be honoured by readers.
4. Expired lock takeover: read, check expiry, overwrite with `If-Match` on the expired
   lock's ETag.
Expiry of the lock is enforced by clients: lifecycle expiration is asynchronous and gives no deadline guarantee.

## 5. Enforce in bucket policy
Require conditional headers on writes for a prefix. Multipart uploads need the `s3:ObjectCreationOperation` key, because `CreateMultipartUpload`, `UploadPart` and
`UploadPartCopy` do not accept conditional headers:
```json
{"Effect": "Deny", "Principal": "*", "Action": "s3:PutObject",
 "Resource": "arn:aws:s3:::b/uploads/*",
 "Condition": {"Null": {"s3:if-none-match": "true"}, "Bool": {"s3:ObjectCreationOperation": "true"}}}
```
(condition keys `s3:if-none-match` and `s3:if-match`). Clients that do not send the header are
denied, which prevents silent overwrites by misconfigured tools. Note: once such a policy is in place, `CopyObject` requests to the protected prefix
fail with 403 without a conditional header and with 501 Not Implemented when one is sent.

## Gotchas
- ETags of multipart objects are not MD5s; treat them as opaque version tokens.
- Versioned buckets: `If-None-Match` evaluates against the current version only; a delete marker as the current version counts as
  "does not exist" and the write succeeds (for `If-Match` it returns 404).
- Older SDKs/CLI versions lack the parameters; upgrade.

## Verify
- [ ] Two concurrent create-only writes: exactly one succeeds, the other gets 412.
- [ ] Stale-ETag update returns 412 and the retry loop converges.
- [ ] Bucket policy denies a PutObject without the header on the protected prefix.

## Checked

2026-10-24 against the AWS documentation (docs.aws.amazon.com, current Amazon S3 User Guide) and the botocore API models. Confirmed: `If-None-Match: *` and `If-Match` on PutObject, CompleteMultipartUpload and CopyObject, SigV4 requirement, permissions, 412 and 409 semantics (botocore parameter docs), 404 for `If-Match` on missing object or delete marker, multipart-race behaviour, delete-marker semantics, `s3:if-none-match` / `s3:if-match` / `s3:ObjectCreationOperation` policy keys and CopyObject side effects, `DeleteObject` `IfMatch` parameter in the API model. Removed unconfirmed launch dates and directory-bucket claims; corrected the sources link to the API reference.

Method: documentation only; no commands were run.
