---
id: computing-software.data-engineering.data-warehouse-architecture.immutable-landing-zones-and-raw-retention
name: immutable-landing-zones-and-raw-retention
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, immutable-landing-zone, raw-retention, object-lock, replayability]
level: advanced
status: docs-checked
description: "Design an immutable landing zone for raw data: write-once layout, object lock and versioning, retention tiers, replay from raw, and deletion requests."
sources:
  - https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html
  - https://docs.cloud.google.com/storage/docs/bucket-lock
  - https://learn.microsoft.com/en-us/azure/storage/blobs/immutable-storage-overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Immutable landing zones and raw retention

**Goal:** every byte received from sources is kept exactly as delivered, so any downstream table can be rebuilt and audited.

## Principles
- **Write-once**: landed files are never modified or overwritten; corrections arrive as new files.
- **As delivered**: original format and encoding; parsing happens downstream (bronze tables read from landing).
- **Self-describing paths**: `s3://acme-landing/<source>/<dataset>/ingest_date=2026-10-18/<batch_id>/part-0001.json.gz` plus a manifest (`_manifest.json` with file list, row counts, checksums, source extract time).

## Enforce immutability
- Bucket policies: only the ingestion role can `PutObject`; nobody (including pipelines) has `DeleteObject` except a retention job.
- Versioning on, so overwrites keep the old version.
- WORM for the retention period on regulated data, per cloud:
  - **S3 Object Lock** needs bucket versioning. Retention applies per object version (fixed retain-until-date, or variable retention with an event hold); legal holds have no expiry. Compliance mode: no one, including the account root user, can overwrite or delete a locked version or shorten its period. Governance mode: users with `s3:BypassGovernanceRetention` (and the `x-amz-bypass-governance-retention:true` header) can override, useful to test settings first. A new PUT to a locked key creates a new version; a simple DELETE only adds a delete marker; a permanent delete of a locked version returns 403.
  - **GCS Bucket Lock** locks a bucket retention policy: once locked it cannot be removed or shortened (it can be extended), and the bucket cannot be deleted until every object meets the retention. Locking is irreversible and places a lien on the project. Deleting a too-young object fails with 403 `retentionPolicyNotMet`.
  - **Azure immutable storage** offers time-based retention (1 day to 146,000 days) and legal holds, at container or version level (version-level needs versioning). An unlocked policy is for testing; lock it for SEC 17a-4(f)-style compliance. A locked policy cannot be deleted or shortened.

## Retention tiers
Illustrative tiers (pick ages from your replay needs):
| Age | Storage | Notes |
|---|---|---|
| 0-30 days | standard | frequent replays and debugging |
| 30-365 days | infrequent access | occasional backfills |
| > 1 year | archive tier | audits; check restore time and retrieval cost |
Lifecycle rules implement this; set expiry per dataset from the retention policy (legal minimum and maximum). A GCS lifecycle delete rule will not delete an object until it meets the bucket retention policy.

## Replay
Downstream layers are rebuildable from landing: bronze ingestion jobs accept an ingest date range; test a full rebuild of one dataset periodically.

## Deletion requests (GDPR) vs immutability
- Avoid landing direct identifiers where possible; or encrypt PII per subject (crypto-shredding: delete the key to make data unreadable).
- Compliance-mode locks cannot be shortened (S3: the only way to delete early is to delete the AWS account; GCS: a locked policy cannot be reduced): use them only for data you are allowed to keep for the full period.
- Crypto-shredding caveat on GCS: Cloud KMS key versions that encrypt objects in a locked bucket cannot be destroyed until those objects meet their retention expiry.
- Azure: page blobs backing active VM disks are discouraged for immutability policies; use block or append blobs. Enable blob soft delete before applying policies.
- Document the legal basis for retaining raw data.

## Verify
An attempted overwrite/delete by a pipeline role is denied; a rebuild of a bronze table from landing matches the current table.

## Checked
2026-11-08: Read in full the S3 Object Lock page, the GCS Bucket Lock page and the Azure immutable storage overview. Confirmed: lock modes, versioning prerequisite, delete behaviour, permissions, 403/retentionPolicyNotMet, irreversible GCS lock with project lien, KMS key-version note, Azure retention range and locked/unlocked behaviour, soft-delete and page-blob advice. Removed: "restores take hours" for archive tiers (not on the pages); generalised the retention tiers table as illustrative. The layout, manifest, replay and GDPR advice is design guidance, not vendor claims; the GDPR retention basis and crypto-shredding are judgement, with the lock caveats above.
Method: documentation only; no commands were run.
