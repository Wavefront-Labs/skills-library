---
id: computing-software.cloud-infrastructure-engineering.aws.s3-mfa-delete-and-delete-marker-handling
name: s3-mfa-delete-and-delete-marker-handling
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, versioning, mfa-delete, delete-marker-replication, delete-markers, undelete, data-recovery]
level: practitioner
status: docs-checked
description: "Protect versioned S3 buckets: MFA delete via the root user, recovering objects by removing delete markers, delete marker replication choices and cleanup."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/MultiFactorAuthenticationDelete.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/DeleteMarker.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/ManagingDelMarkers.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/delete-marker-replication.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication-what-is-isnot-replicated.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# S3 MFA delete and delete marker handling

## 1. Delete markers (versioned buckets)
`DELETE` without a version ID adds a **delete marker** as the current version; the data
versions remain. "Undelete" = delete the marker:
```bash
aws s3api list-object-versions --bucket docs --prefix reports/q3.pdf \
  --query '{markers:DeleteMarkers[?IsLatest].[Key,VersionId],versions:Versions[].[VersionId,LastModified]}'
aws s3api delete-object --bucket docs --key reports/q3.pdf --version-id <DELETE_MARKER_VERSION_ID>
```
Bulk undelete after an accidental `aws s3 rm --recursive`: list markers with `IsLatest=true`
created in the incident window and delete them (script or Batch Operations with a manifest).

## 2. MFA delete
Requires MFA to (a) permanently delete an object **version** and (b) change the bucket's
versioning state. Only the **root user** of the bucket owner can enable it, via API/CLI with
the root MFA device:
```bash
aws s3api put-bucket-versioning --bucket docs \
  --versioning-configuration Status=Enabled,MFADelete=Enabled \
  --mfa "arn:aws:iam::<ACCOUNT_ID>:mfa/root-account-mfa-device 123456"
```
Details: the `--mfa` value is the device serial number (for a virtual device, its ARN), a space, and the current code. MFA delete cannot be
enabled in the console (CLI or API only), and the S3 docs state it cannot be used with lifecycle configurations, so there is no automated version
expiry on that bucket. Consider **Object Lock** and policy controls (for example an SCP denying `s3:DeleteObjectVersion`
and `s3:PutBucketVersioning`) as alternatives; whether MFA delete satisfies a compliance framework is a decision for your compliance team.

## 3. Delete marker replication
- By default delete markers are not replicated (the latest configuration schema, with `Filter`) — deletes in the source don't
  propagate; good for backup/vault replicas. Without a `Filter` (V1 schema) user-created delete markers are replicated.
- Enable (`DeleteMarkerReplication: Enabled`) for active-active/MRAP data where both sides must agree.
- Deletes **with a version ID** are never replicated (protects against malicious permanent deletes).
- Tag-based rules: delete marker replication is not supported. Delete markers created by lifecycle expiration are not replicated, and delete marker replication is outside the S3 RTC 15-minute SLA.

## 4. Cleanup
An expired object delete marker is one where all object versions are deleted and only the marker remains; lifecycle
`ExpiredObjectDeleteMarker: true` (or an expiration of current versions) removes it. Delete markers cost a minimal amount of storage (the size of the key name).

## Gotchas
- Listing calls such as `ListObjectsV2` do not return objects whose current version is a delete marker (`aws s3 ls` follows suit); use `list-object-versions`. A GET without a version ID returns 404 with `x-amz-delete-marker: true`.
- Suspending versioning doesn't delete versions; it stops creating new ones.
- A `DELETE` without a version ID when the current version is already a delete marker adds another delete marker; delete the marker by its version ID to undelete.

## Verify
- [ ] Removing a delete marker restores the object (GET succeeds).
- [ ] `get-bucket-versioning` shows `MFADelete: Enabled` where required by policy.
- [ ] Replication config's `DeleteMarkerReplication` matches the bucket's purpose (vault: Disabled).

## Checked

2026-10-24 against the AWS documentation (docs.aws.amazon.com, current Amazon S3 User Guide) and the botocore API models. Confirmed: delete-marker mechanics (undelete by deleting the marker's version ID), MFA delete scope, root-only enablement, CLI/API-only and `--mfa` format, MFA delete incompatible with lifecycle, delete marker replication defaults and exclusions, `ExpiredObjectDeleteMarker`, listing behaviour. Removed the unconfirmed claim that delete markers slow listings.

Method: documentation only; no commands were run.
