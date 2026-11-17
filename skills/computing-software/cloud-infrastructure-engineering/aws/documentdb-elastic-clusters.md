---
id: computing-software.cloud-infrastructure-engineering.aws.documentdb-elastic-clusters
name: documentdb-elastic-clusters
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, documentdb, elastic-clusters, sharding, mongodb-compatibility]
level: advanced
status: docs-checked
description: "Scale DocumentDB horizontally with elastic clusters: create shards and capacity, choose hashed shard keys, scale shard count and know the feature differences."
sources: ["https://docs.aws.amazon.com/documentdb/latest/developerguide/docdb-using-elastic-clusters.html", "https://docs.aws.amazon.com/documentdb/latest/developerguide/elastic-get-started.html", "https://docs.aws.amazon.com/documentdb/latest/developerguide/elastic-best-practices.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DocumentDB elastic clusters

## 1. When
Instance-based clusters have one writer. Elastic clusters shard data across many shards; the User Guide describes
support for millions of reads/writes per second and petabytes of storage, with the MongoDB 5.0-compatible wire protocol.

## 2. Create
```bash
aws docdb-elastic create-cluster --cluster-name events \
  --shard-count 4 --shard-capacity 8 --shard-instance-count 2 \
  --admin-user-name dbadmin --auth-type PLAIN_TEXT --admin-user-password <PASSWORD> \
  --subnet-ids subnet-a subnet-b --vpc-security-group-ids sg-docdb
aws docdb-elastic get-cluster --cluster-arn <ARN> --query 'cluster.status'
```
- `--shard-capacity` is vCPUs per shard (allowed values 2, 4, 8, 16, 32, 64); `--shard-count` is at most 32;
  `--shard-instance-count` 1 means one writer per shard and additional instances are replicas for reads and availability.
- `--auth-type` accepts `PLAIN_TEXT` or `SECRET_ARN` (where to fetch the password). The User Guide's limitations list
  also says AWS Secrets Manager is not supported in elastic clusters; check the current page before using
  `SECRET_ARN`. Port 27017 only; IAM authentication to the database is not supported.

## 3. Shard collections
```javascript
sh.shardCollection("app.events", { "deviceId": "hashed" })
```
- Not supported (User Guide limitations): range sharding, sharding an existing collection, multi-field shard keys, changing
  the shard key. Use an evenly distributed hash key, and include the shard key in all read, update and delete
  requests to avoid scatter-gather queries.
- Unsharded collections are co-located on one shard per database; keep highly used unsharded collections in
  different databases to spread load.
- For batch operations set `ordered` to false so shards can work in parallel.

## 4. Scale
```bash
aws docdb-elastic update-cluster --cluster-arn <ARN> --shard-capacity 16
```
Per the best-practices page: scaling can cause brief intermittent errors, so do it outside peak hours with client
retries and exponential backoff and jitter; changing shard capacity (vCPUs per shard) is faster than changing shard
count, which moves data between shards; do not make other changes to the cluster while one is in progress; DDL
commands are not supported during scaling.

## 5. Differences from instance-based
The limitations list names, among others: no unique, partial, text or vector indexes; no ACID transactions or change
streams; no point-in-time restore, cloning, Performance Insights, parameter groups or global clusters; write concern 0 is
not supported. Elastic clusters are not supported on DocumentDB 8.0. Re-read the limitations before migrating, since the list changes.

## Verify
- [ ] Per-shard load and storage look balanced in monitoring; key queries include the shard key.

## Checked
Date: 2026-10-27. Sources: DocumentDB Developer Guide pages docdb-using-elastic-clusters (limitations list, version),
elastic-how-it-works (32 shards, 64 vCPUs), elastic-best-practices (shard keys, scaling), elastic-get-started (CLI
flags); botocore `docdb-elastic` model (CreateCluster and UpdateCluster members, `shardCapacity` allowed values,
auth type enum). Corrected: the draft's "hashed shard keys only" is now the documented list of unsupported sharding
features; transactions and change streams are listed as unsupported (the draft implied version-dependent support).
Method: documentation only; no commands were run.
