---
id: computing-software.cloud-infrastructure-engineering.aws.elasticache-backups-and-restore
name: elasticache-backups-and-restore
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, elasticache, elasticache-backup, snapshots, rdb-export, restore]
level: practitioner
status: docs-checked
description: "Back up and restore ElastiCache Valkey/Redis OSS: automatic and manual snapshots, taking them from replicas, memory overhead, export to S3 and seeding from RDB files."
sources: ["https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/backups.html", "https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/backups-exporting.html", "https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/backups-seeding-redis.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ElastiCache backups and restore

## 1. Automatic and manual
```bash
aws elasticache modify-replication-group --replication-group-id sessions \
  --snapshot-retention-limit 7 --snapshot-window 03:00-04:00 --apply-immediately
aws elasticache create-snapshot --replication-group-id sessions --snapshot-name sessions-pre-upgrade
aws elasticache describe-snapshots --replication-group-id sessions
```
Serverless caches use `create-serverless-cache-snapshot` (API `CreateServerlessCacheSnapshot`). Backup and restore
work for Valkey, Redis OSS and Serverless Memcached; node-based Memcached clusters have no backups. Limits from the
User Guide: at most 24 manual backups in a 24-hour period per serverless cache, and at most 20 manual backups per node
for node-based clusters. Cluster mode enabled backs up only at the replication group level, not per shard.

## 2. Performance impact
- Serverless backups have no performance impact. For node-based clusters you can back up from the primary or a read
  replica; the User Guide recommends a replica (choose it as the backup node), because of the resources used. A final
  backup on replication group deletion is always taken from the primary.
- Set `reserved-memory-percent` (and consider a larger node) to avoid paging during backups.
- Data tiering (r6gd): backups cannot be exported to S3, and an r6gd backup restores only to r6gd clusters.

## 3. Export to S3
```bash
aws elasticache copy-snapshot --source-snapshot-name sessions-pre-upgrade \
  --target-snapshot-name sessions-pre-upgrade-export --target-bucket cache-exports-<ACCOUNT_ID>
```
The bucket must be in the same Region as the backup. Grant ElastiCache access with a bucket policy for the service
principal `<region>.elasticache-snapshot.amazonaws.com` (the User Guide gives the policy), and the caller needs IAM
permission for `CopySnapshot` plus S3 actions listed on the export page. The export is an `.rdb` file.

## 4. Restore / seed
```bash
aws elasticache create-replication-group --replication-group-id sessions-restored \
  --replication-group-description restored --snapshot-name sessions-pre-upgrade \
  --cache-node-type cache.r7g.large --engine valkey
aws elasticache create-replication-group ... --snapshot-arns arn:aws:s3:::cache-exports-<ACCOUNT_ID>/dump.rdb
```
Restore always creates a new cache; point clients at it. Seeding from an `.rdb` file: you cannot seed a cluster mode
disabled group from a cluster mode enabled `.rdb`, and the data must fit the node's memory. Grant ElastiCache read
access to the `.rdb` object first (see the seeding page). Serverless caches accept RDB files compatible with Valkey 7.2
and above and Redis OSS 5.0 to the latest.

## Verify
- [ ] `DBSIZE` on the restored cluster matches the source at snapshot time.

## Checked
Date: 2026-10-27. Sources: ElastiCache User Guide pages backups (constraints, performance), backups-exporting (bucket
Region, service principal), backups-seeding-redis, backups-restoring; botocore `elasticache` model (CopySnapshot
`TargetBucket`, CreateReplicationGroup `SnapshotName`/`SnapshotArns`, CreateServerlessCacheSnapshot).
Corrected the serverless snapshot command name (`create-serverless-cache-snapshot`) and replaced the fork/forkless
claim with the documented guidance. Retention and window flags and the export-per-shard claim were removed or confirmed
only by the model.
Method: documentation only; no commands were run.
