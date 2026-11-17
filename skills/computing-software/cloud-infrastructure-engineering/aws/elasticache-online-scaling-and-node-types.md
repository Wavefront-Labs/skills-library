---
id: computing-software.cloud-infrastructure-engineering.aws.elasticache-online-scaling-and-node-types
name: elasticache-online-scaling-and-node-types
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, elasticache, node-type, online-scaling, resharding, valkey]
level: advanced
status: docs-checked
description: "Scale ElastiCache Valkey/Redis OSS online: vertical node type changes, adding shards and replicas, auto scaling, choosing node families and reserved memory."
sources: ["https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/Scaling.html", "https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/scaling-redis-cluster-mode-enabled.html", "https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/CacheNodes.SupportedTypes.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Online scaling and node types

## 1. Node families
| Family | Use |
|---|---|
| R families (for example r7g, r6g) | memory-optimised choice for caches and session stores |
| M families (for example m7g) | general purpose |
| t4g | burstable, small or dev/test caches |
| r6gd (data tiering) | large datasets with a hot subset; SSD extends memory |
Check the "Supported node types" page for the current families and sizes in your Region. Data tiering (r6gd) and
non-tiered node types cannot be scaled into each other, and a data tiering backup cannot be exported to S3.
Serverless caches skip node sizing entirely.

## 2. Vertical scaling (change node type)
```bash
aws elasticache modify-replication-group --replication-group-id sessions \
  --cache-node-type cache.r7g.xlarge --apply-immediately
```
The User Guide describes online vertical scaling with minimal downtime: ElastiCache creates a cluster with the new node
type and synchronises it with the old nodes. Make sure ENI capacity is sufficient, and when scaling down that the
smaller node has memory for the expected traffic. Scale during your lowest traffic and test in staging first.

## 3. Horizontal (cluster mode enabled)
```bash
aws elasticache modify-replication-group-shard-configuration --replication-group-id sessions \
  --node-group-count 6 --apply-immediately
aws elasticache increase-replica-count --replication-group-id sessions --new-replica-count 2 --apply-immediately
```
Online resharding keeps the cluster serving requests but is compute-intensive, so expect some performance degradation
that depends on your normal CPU use; offline resharding takes the cluster offline for a significant portion of the
process. Auto scaling (Application Auto Scaling target tracking or scheduled) covers shards and replicas for cluster mode enabled
clusters on Valkey 7.2+ or Redis OSS 6.0+, for the instance families and sizes listed on the Auto Scaling page; it is not supported for
global datastores, Outposts or Local Zones.

## 4. Memory headroom
`reserved-memory-percent` defaults to 25% and leaves room for backups, replication buffers and fragmentation; do not
reduce it without testing. Watch `DatabaseMemoryUsagePercentage`, `Evictions`, `EngineCPUUtilization`, `SwapUsage`.

## Verify
- [ ] Scaling event completes with only the client errors your retry policy absorbs; memory headroom remains after scaling.

## Checked
Date: 2026-10-27. Sources: ElastiCache User Guide pages redis-cluster-vertical-scaling, scaling-redis-cluster-mode-enabled
(offline vs online resharding, performance impact), AutoScaling (prerequisites), redis-memory-management (25% default),
CacheNodes.SupportedTypes (families), backups (data tiering limits); botocore `elasticache` model
(`modify-replication-group-shard-configuration` requires `NodeGroupCount` and `ApplyImmediately`; `IncreaseReplicaCount`).
Removed the price-performance and "short failover" claims; auto scaling is limited to cluster mode enabled.
Method: documentation only; no commands were run.
