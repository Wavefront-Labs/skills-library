---
id: computing-software.cloud-infrastructure-engineering.minio.lifecycle-expiration-rules
name: lifecycle-expiration-rules
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, lifecycle-expiration-rules, expire-days, noncurrent-expire-days, expire-delete-marker, expire-all-object-versions, admin-set-tier, put-lifecycle-configuration]
level: practitioner
status: docs-checked
description: "Create MinIO expiry rules with mc ilm rule add: --expire-days, --noncurrent-expire-days, --expire-delete-marker, --expire-all-object-versions and required permissions."
sources: ["https://github.com/minio/docs/blob/main/source/administration/object-management/create-lifecycle-management-expiration-rule.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Creating MinIO expiration rules

## Permissions
On the target buckets: `s3:PutLifecycleConfiguration` and `s3:GetLifecycleConfiguration`. For transition rules also `admin:SetTier` and `admin:ListTier` on the cluster. The alias user must hold them.

## Expire after N days
```
mc ilm rule add ALIAS/PATH --expire-days "DAYS"
```
`30` expires objects 30 days after creation.

## Versioned buckets
```
mc ilm rule add ALIAS/PATH \
   --noncurrent-expire-days NONCURRENT_DAYS \
   --expire-delete-marker
```
- `--noncurrent-expire-days` expires versions that have been non-current that long (the docs use `30d` as an example value).
- `--expire-delete-marker` removes delete markers with no remaining versions.
- `mc ilm rule add ALIAS/PATH --expire-all-object-versions` expires all versions, but only for objects that do **not** have a `DeleteMarker` as the current version.

## Interactions
- Expiry respects object locks: current-version rules create delete markers on locked objects; non-current expiry waits for retention to end or legal holds to lift (`computing-software.cloud-infrastructure-engineering.minio.object-locking`).
- Scanner timing means actual removal can lag the rule period.

Overview: `computing-software.cloud-infrastructure-engineering.minio.lifecycle-management`.

## Checked

2026-11-03. Confirmed against the MinIO docs source: create-lifecycle-management-expiration-rule page: permissions, expire-days, noncurrent, delete-marker and expire-all-object-versions flags; object-retention page for lock interaction; lifecycle page for scanner lag. Removed or fixed: nothing.

Method: documentation only; no commands were run.
