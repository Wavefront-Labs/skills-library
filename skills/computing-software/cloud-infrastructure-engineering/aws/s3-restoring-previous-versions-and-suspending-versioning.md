---
id: computing-software.cloud-infrastructure-engineering.aws.s3-restoring-previous-versions-and-suspending-versioning
name: s3-restoring-previous-versions-and-suspending-versioning
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, s3, restore-previous-version, versioning-suspended, delete-marker-removal, list-object-versions, undelete]
level: practitioner
status: docs-checked
description: "Recover from S3 overwrites and deletes with versioning: list versions, undelete by removing delete markers, restore an older version in place, bulk recovery, and suspending."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/RestoringPreviousVersions.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/ManagingDelMarkers.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/VersionSuspendedBehavior.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/DeleteMarker.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Restoring previous versions and suspending versioning

## 1. See the history
```bash
aws s3api list-object-versions --bucket b --prefix reports/q3.xlsx \
  --query '{versions:Versions[].{id:VersionId,latest:IsLatest,mod:LastModified,size:Size},markers:DeleteMarkers[].{id:VersionId,latest:IsLatest,mod:LastModified}}'
```

## 2. Undelete (object was deleted)
A simple DELETE in a versioned bucket adds a **delete marker** as the latest version.
Remove the marker and the previous version becomes current again:
```bash
aws s3api delete-object --bucket b --key reports/q3.xlsx --version-id <delete-marker-version-id>
```
Deleting a specific version ID permanently deletes that version (no recovery); only delete
the marker's version ID.

## 3. Restore an older version (object was overwritten or corrupted)
Copy the old version on top, making it the newest version (history is preserved):
```bash
aws s3api copy-object --bucket b --key reports/q3.xlsx \
  --copy-source "b/reports/q3.xlsx?versionId=<good-version-id>"
```
The console cannot copy a version in place; use the CLI or SDKs. For batches, use an S3 Batch Operations copy job
(copy non-current versions first, then current versions in a second job, because order is not guaranteed). Alternatively
delete the bad newer versions permanently (destructive, and requires `s3:DeleteObjectVersion`). You can undelete only an object deleted as the
latest version; you cannot undelete a previous version that was deleted.

## 4. Bulk recovery after a mass delete or ransomware-style overwrite
1. Stop the damage (revoke the principal's sessions, block writes with a bucket policy).
2. Build a list with `list-object-versions` (or S3 Inventory including all versions) of
   delete markers created after the incident time.
3. Remove those markers in batches with `delete-objects` (each call takes a list of keys with version IDs), or use S3 Batch Operations with a manifest.
4. For overwrites, copy the last version before the incident time for each key (Batch
   Operations Copy with version IDs in the manifest).
Object Lock or replication to a separate account is what makes this reliable; versioning
alone does not protect against a principal allowed to `DeleteObjectVersion`.

## 5. Suspending versioning
```bash
aws s3api put-bucket-versioning --bucket b --versioning-configuration Status=Suspended
```
- Versioning cannot return to the unversioned state once enabled, only be suspended.
- Existing versions remain (and keep costing); new PUT, POST and copy writes get version ID `null`,
  overwriting any previous `null` version. A `DELETE` without a version ID removes only a `null` version and inserts a delete marker with ID `null`.
- Replication requires versioning on both buckets, and Object Lock buckets cannot suspend versioning.
- To shrink costs, keep versioning on and add `NoncurrentVersionExpiration` instead.

## Gotchas
- Listing calls (`ListObjectsV2`, `aws s3 ls`) do not return objects whose current version is a delete marker; a "missing" file may just have a marker. Only `ListObjectVersions` shows markers.
- Permanently deleting a version, including a delete marker, uses `DeleteObject` with a version ID and needs `s3:DeleteObjectVersion`; restore via copy needs
  `s3:GetObjectVersion` on the source version and `s3:PutObject`.
- MFA delete (if enabled) requires the root user with MFA to permanently delete versions
  or change versioning state.

## Verify
- [ ] After undelete, `aws s3api head-object` returns the object and the marker is gone from `list-object-versions`.
- [ ] Restored object's checksum or content matches the chosen good version.
- [ ] Versioning state is `Enabled` on buckets that need recovery capability, with noncurrent expiration set.

## Checked

2026-10-24 against the AWS documentation (docs.aws.amazon.com, current Amazon S3 User Guide) and the botocore API models. Confirmed: the two restore approaches (copy a version in place, or delete the current version), delete-marker undelete rules, versioning states and suspended-bucket behaviour (null version ID, overwrite, delete marker with null ID), Batch Operations copy ordering note, listing behaviour. Removed unconfirmed claims about `aws s3 cp --version-id` and per-call key counts.

Method: documentation only; no commands were run.
