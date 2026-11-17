---
id: computing-software.cloud-infrastructure-engineering.aws.redshift-snapshots-and-resize
name: redshift-snapshots-and-resize
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, redshift, redshift-snapshot, automated-snapshots, manual-snapshots, cross-region-snapshot-copy, snapshot-copy-grant, restore-table-from-snapshot, elastic-resize, classic-resize, ra3, redshift-serverless, recovery-points]
level: practitioner
status: docs-checked
description: "Protect and resize Redshift: automated/manual snapshots, cross-Region copy with KMS grants, table-level restore, Serverless recovery points, and elastic vs classic resize."
sources: ["https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-snapshots.html", "https://docs.aws.amazon.com/redshift/latest/mgmt/cross-region-snapshot-copy.html", "https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-snapshot-restore-table-from-snapshot.html", "https://docs.aws.amazon.com/redshift/latest/mgmt/resizing-cluster.html", "https://docs.aws.amazon.com/redshift/latest/mgmt/serverless-snapshots-recovery-points.html", "https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-snapshot-share-snapshot.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Redshift snapshots and resize

**Goal:** a dropped table is back in minutes, a lost Region is recoverable from snapshots in
another, and the cluster changes size with a short, planned interruption.

## 1. Snapshots (provisioned)
- **Automated**: incremental; by default about every eight hours or every 5 GB per node of changes, whichever
  comes first (minimum 15 minutes apart when data exceeds 5 GB x nodes). Default retention is 1 day. RG and RA3
  clusters cannot disable automated snapshots and take a retention of 1 to 35 days (`--automated-snapshot-retention-period`);
  on other node types 0 disables them and deletes existing automated snapshots. Automated snapshots are deleted
  when the cluster is deleted. A paused cluster takes no automated snapshots, except a data sharing producer.
- **Custom schedule**: a snapshot schedule (cron syntax in UTC) replaces the default; maximum frequency one per hour,
  minimum one per day, and overlapping schedules within an hour fail validation.
- **Manual**: kept indefinitely by default, even after the cluster is deleted, unless you set
  `--manual-snapshot-retention-period`; take one before every risky change.
```bash
aws redshift modify-cluster --cluster-identifier dw --automated-snapshot-retention-period 14
aws redshift create-cluster-snapshot --cluster-identifier dw --snapshot-identifier dw-pre-upgrade-20261016
aws redshift create-snapshot-schedule --schedule-identifier weekdays --schedule-definitions "cron(0 9,17 MON-FRI)"
```
### Cross-Region copy
```bash
# in the DESTINATION region, for KMS-encrypted clusters
aws redshift create-snapshot-copy-grant --snapshot-copy-grant-name dw-dr --kms-key-id <DEST_KEY_ARN> --region us-west-2
# on the source cluster
aws redshift enable-snapshot-copy --cluster-identifier dw --destination-region us-west-2 \
  --retention-period 7 --snapshot-copy-grant-name dw-dr
```
Without a grant, snapshots copied from an encrypted cluster are encrypted in the destination with a default
AWS-owned key. Disable cross-Region copy before changing the cluster's encryption.
### Restore
```bash
aws redshift restore-from-cluster-snapshot --cluster-identifier dw-restore --snapshot-identifier <SNAP> \
  --node-type ra3.4xlarge --number-of-nodes 4        # node type and count can change on restore
aws redshift restore-table-from-cluster-snapshot --cluster-identifier dw --snapshot-identifier <SNAP> \
  --source-database-name prod --source-schema-name sales --source-table-name orders \
  --new-table-name orders_restored
aws redshift describe-table-restore-status --cluster-identifier dw
```
Table restore limits: only into the same running cluster the snapshot came from, one table at a time, the new
table name must not exist (rename or drop the original first), no foreign keys, views or grants are carried over,
and not from a snapshot taken before a resize (except after an elastic resize that kept the node type).
Possible restore configurations depend on the original node count and the target node type.

## 2. Redshift Serverless
- **Recovery points**: created automatically about every 30 minutes or every 5 GB per node of changes (minimum
  15 minutes for larger datasets) and kept for 24 hours; you cannot set a schedule for them. Promote one to a
  snapshot with `aws redshift-serverless convert-recovery-point-to-snapshot --recovery-point-id <id> --snapshot-name <n>`.
- **Snapshots**: `aws redshift-serverless create-snapshot --namespace-name ns --snapshot-name x --retention-period 30`
  (`retentionPeriod` is an integer number of days); restore into a namespace or a provisioned cluster
  (`restore-from-snapshot`) or a single table (`restore-table-from-snapshot`). Cross-Region copy uses a snapshot copy
  configuration (`create-snapshot-copy-configuration` with `--destination-region`, optional destination KMS key).

## 3. Resize
| | Elastic resize | Classic resize |
|---|---|---|
| Time | About ten minutes on average | Longer |
| Interruption | Running queries can be dropped (in place) or are dropped on completion when the node type changes | To an RG or RA3 target: source restarts for a few minutes, then reads and writes continue while it runs |
| What changes | Node count within limits (RG/RA3: up to 4x more, down to a quarter) and node type | Any node type or count |
```bash
aws redshift resize-cluster --cluster-identifier dw --number-of-nodes 8 --no-classic
aws redshift resize-cluster --cluster-identifier dw --node-type ra3.4xlarge --number-of-nodes 6 --classic
aws redshift describe-resize --cluster-identifier dw
```
- Check allowed target sizes first: `aws redshift describe-node-configuration-options --action-type resize-cluster --cluster-identifier dw`.
- Classic resize to RG or RA3 keeps read and write access only if prerequisites hold: data under 2 PB and a manual
  snapshot no more than 10 hours old.
- Elastic resize does not sort tables or reclaim disk space.
- For predictable bursts consider concurrency scaling or a scheduled elastic resize (`create-scheduled-action`,
  which needs a schedule and an IAM role) instead of a permanent size.

## Gotchas
- Snapshots accrue storage charges until their retention ends; manual snapshots persist until deleted. Prices were not checked.
- Restoring a KMS-encrypted snapshot in another account needs the key shared and the snapshot authorised
  (`authorize-snapshot-access`); each snapshot can be authorised for up to 20 accounts and each KMS key for 100.
- Elastic resize with a node-type change takes a snapshot first.

## Verify
- [ ] `describe-cluster-snapshots --cluster-identifier dw --snapshot-type automated` shows recent snapshots within schedule.
- [ ] Destination Region lists copied snapshots; a test restore there completes.
- [ ] A table restore drill completes in the documented time.
- [ ] Resize dry-run: `describe-node-configuration-options` lists the target; maintenance window agreed.

## Checked
Date: 2026-10-27. Documentation release: Amazon Redshift Management Guide (latest), botocore redshift
2012-12-01 and redshift-serverless 2021-04-21 models. Confirmed: automated snapshot cadence, retention rules and
RG/RA3 limits, schedule format limits, manual retention default, copy grant behaviour, table restore limits,
Serverless recovery point cadence and retention, resize durations and limits, CLI parameter names. Removed
`rate(1 hour)` (the docs define cron schedule syntax), the claim that a paused cluster bills snapshot storage,
the post-resize `skew_rows` advice and the "hours historically" classic resize timing.
Method: documentation only; no commands were run.
