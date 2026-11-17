---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.s3-lifecycle-rules
name: s3-lifecycle-rules
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [expiration, noncurrent, put-bucket-lifecycle, lifecycle]
level: practitioner
status: docs-checked
description: "Configure S3 lifecycle expiration on SeaweedFS buckets: supported rule fields, filters, rejected Transition rules, API errors and the worker's lag."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/S3-Lifecycle
  - https://github.com/seaweedfs/seaweedfs/wiki/S3-Lifecycle-Operator-Guide
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# s3 lifecycle rules

Rules are set with the normal S3 API and enforced by a scheduled worker:
```bash
aws s3api put-bucket-lifecycle-configuration --endpoint-url http://localhost:8333 --bucket my-bucket   --lifecycle-configuration '{"Rules":[{"ID":"expire-old","Status":"Enabled","Filter":{"Prefix":""},"Expiration":{"Days":90}}]}'
aws s3api get-bucket-lifecycle-configuration --endpoint-url http://localhost:8333 --bucket my-bucket
aws s3api delete-bucket-lifecycle --endpoint-url http://localhost:8333 --bucket my-bucket
```
Supported: `Expiration.Days` / `Date` / `ExpiredObjectDeleteMarker`, `NoncurrentVersionExpiration.NoncurrentDays` and `NewerNoncurrentVersions`, `AbortIncompleteMultipartUpload.DaysAfterInitiation`, and filters `Prefix`, `Tag`, `ObjectSizeGreaterThan` / `LessThan`, `And`.

Not supported: `Transition` and `NoncurrentVersionTransition`. A PUT whose enabled rules contain either is rejected with `NotImplemented` (a Disabled rule carrying one is ignored).

PUT errors: body over 1 MiB gives `EntityTooLarge`, bad XML gives `MalformedXML`; GET with none configured gives `NoSuchLifecycleConfiguration`.

Gotcha: expiry is not event-time exact. The delay is bounded by the worker cadence (default 24h), and walker-only rules (`Date`, `ExpiredObjectDeleteMarker`, `NewerNoncurrentVersions`) can wait longer.

## Checked

2026-11-04. Confirmed against the SeaweedFS wiki pages S3 Lifecycle (supported fields, filters, Transition rejected with NotImplemented, 1 MiB limit, error codes, worker lag of default 24h plus walker window) and S3 Lifecycle Operator Guide. Removed the Verify line (head-object is not on the page).
Method: documentation only; no commands were run.
