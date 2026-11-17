---
id: computing-software.cloud-infrastructure-engineering.aws.aws-backup-legal-holds-and-backup-search
name: aws-backup-legal-holds-and-backup-search
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, aws-backup, backup-legal-hold, backup-search, ediscovery, item-level-restore]
level: advanced
status: docs-checked
description: "Place AWS Backup legal holds that stop recovery point deletion, release them, and find and restore individual files or objects with backup indexing and search."
sources: ["https://docs.aws.amazon.com/aws-backup/latest/devguide/legalhold.html", "https://docs.aws.amazon.com/aws-backup/latest/devguide/backup-search.html", "https://docs.aws.amazon.com/aws-backup/latest/devguide/restoring-s3.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Legal holds and backup search

## 1. Legal hold
```bash
aws backup create-legal-hold --title "Case 2026-114" --description "Retain finance backups" \
  --recovery-point-selection '{"VaultNames":["finance"],"DateRange":{"FromDate":"2026-01-01T00:00:00Z","ToDate":"2026-06-30T23:59:59Z"}}' \
  --tags case=2026-114
aws backup list-legal-holds
aws backup list-recovery-points-by-legal-hold --legal-hold-id <ID>
```
- `Title` and `Description` are required. `RecoveryPointSelection` can name `VaultNames`, `ResourceIdentifiers` and a
  `DateRange`.
- A held recovery point cannot be deleted, and lifecycle actions that would delete it are delayed until every legal
  hold on it is removed; the hold does not expire by itself. A backup can carry several holds.
- Limits and scope from the legal hold page: legal holds do not apply to continuous backups; only recovery points
  created by AWS Backup can be held; a hold does not follow a copy to another Region or account; recovery points
  with status `EXPIRED` or `DELETING` are not included; each account can have at most 50 active legal holds.
- Hold statuses: `CREATING`, `ACTIVE`, `CANCELED`, `CANCELING`. Delete requests can still succeed while a hold is
  `CREATING` or `CANCELING`.
- A legal hold protects individual recovery points; Vault Lock is the separate vault-level control.
- Release:
```bash
aws backup cancel-legal-hold --legal-hold-id <ID> --cancel-description "Case closed" --retain-record-in-days 365
```
`CancelDescription` is required; `RetainRecordInDays` (how long the hold record is kept) is optional. Recovery points
that expired during the hold are deleted within 24 hours after release.
Restrict `backup:CreateLegalHold` and `backup:CancelLegalHold` to the legal/compliance role.

## 2. Backup indexing and search (EBS snapshots and S3 backups)
1. Turn on indexing in the plan rule (`IndexActions` with `ResourceTypes` of `EBS` and/or `S3`), when creating an
   on-demand backup, or retroactively for an existing recovery point.
2. Search across indexed recovery points. `SearchScope.BackupResourceTypes` takes exactly one of `S3` or `EBS`:
```bash
aws backupsearch start-search-job --name find-invoice \
  --search-scope '{"BackupResourceTypes":["S3"],"BackupResourceCreationTime":{"CreatedAfter":"2026-09-01T00:00:00Z"}}' \
  --item-filters '{"S3ItemFilters":[{"ObjectKeys":[{"Value":"invoices/2026/","Operator":"BEGINS_WITH"}]}]}'
aws backupsearch list-search-job-results --search-job-identifier <ID>
```
3. Restore just the found items: S3 restores accept up to five objects or folders (`ItemsToRestore`); an EBS
   recovery point restores to a new volume.
- Index permissions for EBS come from the managed policy `AWSBackupServiceRolePolicyForIndexing`; search permissions
  (`backup:ListIndexedRecoveryPointsForSearch`, `backup:SearchRecoveryPoint`) are in `AWSBackupSearchOperatorAccess`.
- Recovery points in a logically air-gapped vault cannot be indexed; EBS snapshots in the archive (cold) tier cannot
  be indexed; indexable file systems are ext2, ext3, ext4, vfat, xfs and ntfs.
- Each index creation, each search job and index storage is charged; scope searches narrowly. Prices were not checked.

## Verify
- [ ] An expired, held recovery point still exists; after release it is deleted on schedule.
- [ ] A search returns the expected object and the item-level restore recovers it.

## Checked
Date: 2026-10-27. Documentation release: AWS Backup Developer Guide (latest), botocore backup 2018-11-15 and
backupsearch 2018-05-10 models. Confirmed: required `create-legal-hold` and `cancel-legal-hold` parameters,
legal hold scope limits and the 50-hold quota, hold statuses, 24-hour deletion after release, `IndexAction`
resource types, `StartSearchJob` scope and item-filter shapes and `BEGINS_WITH` operator, the single-resource-type
scope, index eligibility rules, managed policy names and S3 five-item restore. Corrected the legal hold source URL
(the page is `legalhold.html`) and removed an empty `ResourceIdentifiers` example value.
Method: documentation only; no commands were run.
