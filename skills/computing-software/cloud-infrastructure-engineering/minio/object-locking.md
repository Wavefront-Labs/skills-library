---
id: computing-software.cloud-infrastructure-engineering.minio.object-locking
name: object-locking
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, object-locking, worm, governance-mode, compliance-mode, mc-mb-with-lock, mc-retention-set, bypass-governance-retention, default-retention]
level: advanced
status: docs-checked
description: "Protect MinIO object versions with WORM locking: mc mb --with-lock, default retention with mc retention set, and GOVERNANCE or COMPLIANCE mode."
sources: ["https://github.com/minio/docs/blob/main/source/administration/object-management/object-retention.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MinIO object locking and retention

Object locking enforces WORM immutability on versioned objects and is S3-compatible. The docs state it meets SEC17a-4(f), FINRA 4511(C) and CFTC 1.31(c)-(d) as assessed by Cohasset Associates.

## Enabling
- Locking can be enabled only **at bucket creation**: `mc mb --with-lock ALIAS/BUCKET`. It implicitly enables versioning.
- Retention rules can be configured any time. Bucket default:
```
mc retention set --recursive --default MODE DURATION ALIAS/BUCKET
```
`MODE` is `COMPLIANCE` or `GOVERNANCE`. Per-object retention is set through the SDK's PUT operation.

## Modes
- **GOVERNANCE** - blocks changes by non-privileged users. Users with `s3:BypassGovernanceRetention` may modify the object, change the duration or lift the lock, and must send the `x-amz-bypass-governance-retention:true` header.
- **COMPLIANCE** - blocks changes by everyone including the root user; the lock cannot be changed or removed before the duration expires.
In both modes MinIO lifts the lock automatically when the duration passes.

## Versioning and lifecycle interaction
- Locks are per version. Unversioned deletes create a delete marker; deleting a locked specific version fails ("WORM protected").
- Lifecycle expiration respects locks: current-version rules create a delete marker, while non-current-version expiry waits until retention has passed or been lifted (legal holds). In the docs' 45 day GOVERNANCE example only the oldest unlocked version is eligible.

See `computing-software.cloud-infrastructure-engineering.minio.legal-hold`.

## Checked

2026-11-03. Confirmed against the MinIO docs source: object-retention page: lock modes, bypass header, root cannot modify COMPLIANCE, versioning and lifecycle interaction. Removed or fixed: nothing.

Method: documentation only; no commands were run.
