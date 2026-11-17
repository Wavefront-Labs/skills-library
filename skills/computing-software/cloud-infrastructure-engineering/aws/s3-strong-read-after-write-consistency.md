---
id: computing-software.cloud-infrastructure-engineering.aws.s3-strong-read-after-write-consistency
name: s3-strong-read-after-write-consistency
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, read-after-write, strong-consistency, conditional-writes, concurrency]
level: practitioner
status: docs-checked
description: "Rely correctly on S3 strong read-after-write consistency for GET, PUT and LIST, and know what is still eventually consistent and how to handle concurrent writers."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/conditional-requests.html", "https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutObject.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# S3 strong read-after-write consistency

## 1. What is strongly consistent
After a successful PUT, overwrite or DELETE, any later GET, HEAD or LIST in any client sees the result:
- new object: GET returns it; LIST includes it;
- overwrite: GET returns the new bytes;
- delete: GET returns 404 and LIST omits it.
This applies in all Regions. Reads of object metadata (HEAD), ACLs and object tags are also strongly
consistent, and an update to a single key is atomic; there are no atomic updates across keys.

## 2. What is not
- Bucket configuration is eventually consistent: a deleted bucket can still appear in a bucket list, and
  after first enabling versioning AWS recommends waiting 15 minutes before writes to the bucket.
- S3 Inventory lists are eventually consistent. Replication, lifecycle actions and event notifications
  are separate asynchronous features; check each feature's page for its timing.
- CloudFront or other caches in front of S3 serve stale content until TTL or invalidation.

## 3. Concurrent writers
S3 does not support object locking for concurrent writers. Two simultaneous PUTs to the same key: the request with the latest timestamp wins. Use conditional writes:
```bash
aws s3api put-object --bucket b --key leases/job-42 --body lease.json --if-none-match '*'   # create only if absent
aws s3api put-object --bucket b --key state.json --body s.json --if-match '"<ETAG>"'          # compare-and-swap
```
`412 Precondition Failed` means the condition was not met (someone else won): re-read and retry. A
`409 ConditionalRequestConflict` means a conflicting operation was in flight: retry. Conditional writes also
work on CompleteMultipartUpload and CopyObject. Versioning keeps every write.

## 4. Patterns
- Write-then-read pipelines (producer writes, consumer lists) are safe.
- Leader election and manifests: conditional writes.

## Verify
- [ ] Integration test: PUT then immediate LIST from another client always includes the key.

## Checked

Checked 2026-10-27 against the S3 User Guide pages What is Amazon S3 (data consistency model) and Add preconditions to S3 operations with conditional requests, and the S3 API reference for PutObject and GetObject.
Confirmed: strong read-after-write consistency for PUT, DELETE, GET and LIST in all Regions; reads of metadata, ACLs and tags strongly consistent; no object locking for concurrent writers (latest timestamp wins); bucket configuration eventual consistency including the 15-minute versioning recommendation; If-None-Match and If-Match on PutObject (also CompleteMultipartUpload and CopyObject), 412 Precondition Failed and 409 ConditionalRequestConflict retry guidance. Removed the unconfirmed no-cost and S3Guard statements.

Method: documentation only; no commands were run.
