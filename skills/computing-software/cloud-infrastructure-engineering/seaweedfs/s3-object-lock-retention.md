---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.s3-object-lock-retention
name: s3-object-lock-retention
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [worm, legal-hold, governance-mode, compliance-mode, object-lock, retention]
level: advanced
status: docs-checked
description: "Use S3 Object Lock on SeaweedFS: enable at bucket creation with versioning, governance vs compliance retention, legal holds and bypass permission."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/S3-Object-Lock-and-Retention
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# s3 object lock retention

Prerequisites: Object Lock needs versioning, and it can only be enabled when the bucket is created, not later.

```bash
aws --endpoint-url $S3_ENDPOINT s3api create-bucket --bucket locked --object-lock-enabled-for-bucket
```
Modes:
- Governance: protects against most users; `s3:BypassGovernanceRetention` (and admin users) can override.
- Compliance: nobody can delete or modify, including root, and the retention period cannot be shortened.
- Legal hold: independent of retention; blocks deletion and modification until removed, can be combined with a retention.

API:
- `GET/PUT /?object-lock` for bucket configuration
- `GET/PUT /{object}?retention`
- `GET/PUT /{object}?legal-hold`
```bash
aws --endpoint-url $S3_ENDPOINT s3api put-object-retention --bucket locked --key f --retention Mode=GOVERNANCE,RetainUntilDate=2030-01-01T00:00:00Z
aws --endpoint-url $S3_ENDPOINT s3api put-object-legal-hold --bucket locked --key f --legal-hold Status=ON
```
Compliance retention cannot be shortened, and no user, including root, can delete or modify the object. Deleting an object under compliance retention returns an error such as `Object is under COMPLIANCE mode retention and cannot be deleted`.

## Checked

2026-11-04. Confirmed against the SeaweedFS wiki page S3 Object Lock and Retention: versioning prerequisite, creation-time only, governance, compliance and legal hold behaviour, bypass permission, API paths, CLI examples. Replaced the generic Gotcha and Verify with page-stated behaviour.
Method: documentation only; no commands were run.
