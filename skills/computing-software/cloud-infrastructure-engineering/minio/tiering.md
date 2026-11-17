---
id: computing-software.cloud-infrastructure-engineering.minio.tiering
name: tiering
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, tiering, object-transition, mc-ilm-tier-add, transition-days, warm-tier, remote-tier, standard-warm, not-backup]
level: advanced
status: docs-checked
description: "Tier MinIO objects to a remote MinIO, S3, GCS or Azure target with mc ilm tier add and --transition-days, including the exclusive-access, no-rehydration and not-a-backup caveats."
sources: ["https://github.com/minio/docs/blob/main/source/administration/object-management/object-lifecycle-management.rst", "https://github.com/minio/docs/blob/main/source/administration/object-management/transition-objects-to-minio.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MinIO object tiering (transition)

MinIO moves objects to a remote tier (another MinIO, Amazon S3, Google Cloud Storage or Azure Blob Storage) and fetches them back transparently on read, with no app changes. Directory objects (0-byte names ending in `/`) do not tier.

## Steps
1. Permissions: `s3:PutLifecycleConfiguration`, `s3:GetLifecycleConfiguration`, `admin:SetTier`, `admin:ListTier` on the source; the remote credentials need read, write, list and delete on the remote bucket.
2. Create the remote bucket first. If it holds other data, set `--prefix` to isolate transitioned objects.
3. Register the tier (`mc ilm tier add ...`, see `computing-software.cloud-infrastructure-engineering.minio.tier-targets`).
4. Add the rule:
```
mc ilm rule add ALIAS/BUCKET \
  --transition-tier TIERNAME --transition-days DAYS \
  --noncurrent-transition-days NONCURRENT_DAYS \
  --noncurrent-transition-tier TIERNAME
```
Verify with `mc ls`: since RELEASE.2022-11-10T18-20-21Z output shows `STANDARD` for objects on MinIO and `WARM` for those on the tier.

## Caveats
- **Not a backup.** The remote cannot restore lost metadata and gives no extra BC/DR; use bucket or site replication for that.
- **Exclusive access.** All access to transitioned data must go through MinIO. Modifying objects or metadata directly, or applying lifecycle rules on the remote bucket, can lose data. MinIO writes under a unique per-deployment prefix and supports an optional readable prefix.
- The remote must return objects immediately (milliseconds to seconds); rehydration or manual intervention tiers are unsupported.
- The scanner may delay rule application.

## Checked

2026-11-03. Confirmed against the MinIO docs source: transition-objects pages and the lifecycle page: permissions, prefix isolation, WARM and STANDARD listing, caveats, scanner delay. Removed or fixed: nothing.

Method: documentation only; no commands were run.
