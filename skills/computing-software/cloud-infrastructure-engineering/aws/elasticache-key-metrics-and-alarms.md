---
id: computing-software.cloud-infrastructure-engineering.aws.elasticache-key-metrics-and-alarms
name: elasticache-key-metrics-and-alarms
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, elasticache, enginecpuutilization, cache-hit-rate, evictions, databasememoryusagepercentage, valkey, redis]
level: practitioner
status: docs-checked
description: "Monitor ElastiCache (Valkey/Redis OSS, Memcached): EngineCPUUtilization vs CPUUtilization, memory and evictions, hit rate, connections, replication lag, and alarm thresholds."
sources: ["https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/CacheMetrics.WhichShouldIMonitor.html", "https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/CacheMetrics.Redis.html", "https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/CacheMetrics.HostLevel.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ElastiCache key metrics and alarms

Namespace `AWS/ElastiCache`, dimensions `CacheClusterId` (node) and `CacheNodeId` for node-based clusters.
Serverless caches use the dimension `clusterId` and their own metrics (for example `ElastiCacheProcessingUnits`, the
ECPUs consumed, and `BytesUsedForCache`).

## 1. CPU: use the right metric
- Valkey/Redis OSS are single-threaded. `CPUUtilization` is a host-level metric; `EngineCPUUtilization` reports usage of
  the engine core.
- The User Guide's guidance: for node types with 2 vCPUs or fewer use `CPUUtilization` (background host processes can
  take a significant share on small hosts); for 4 vCPUs or more use `EngineCPUUtilization` to set scaling thresholds.
- Suggested threshold: 90% of available CPU; because the engine is single-threaded, for `CPUUtilization` divide by the number
  of cores (a two-core node: 90/2 = 45%). Tune to your workload.
- If the CPU threshold is exceeded with a mostly read workload, add read replicas; with writes, scale up (cluster
  mode disabled) or add shards (cluster mode enabled).
- Look for expensive commands and hot keys: check `SLOWLOG GET` and command latency metrics such as
  `GetTypeCmdsLatency` and `SetTypeCmdsLatency`.

## 2. Memory
- `DatabaseMemoryUsagePercentage`: share of memory used by the engine; pick a threshold for your workload.
- `Evictions`: keys evicted because of memory pressure; choose your own alarm threshold. For a cache some evictions
  are fine; for data that must persist (sessions, queues) any eviction is a bug.
- Memory pressure: the User Guide says `FreeableMemory` close to 0 (below 100 MB) or `SwapUsage` greater than
  `FreeableMemory` indicates a node under memory pressure; see reserved memory (`reserved-memory-percent`) and node size.
- `BytesUsedForCache`, `FreeableMemory` for capacity planning.
- `CurrItems` growth without TTLs means unbounded keys: set TTLs.

## 3. Effectiveness
- `CacheHitRate`, or compute `CacheHits / (CacheHits + CacheMisses)`; alarm if it drops below your recorded baseline
  after a deploy changing key formats, or memory pressure evicting useful data.

## 4. Connections and network
- `CurrConnections`: sudden climb indicates connection leaks or missing pooling. Connections rejected because
  `maxclients` was reached are counted by `RejectedConnections` (derived from `rejected_connections` in `INFO`).
- `NewConnections`: high churn costs CPU (TLS handshakes especially); use pooling.
- Network allowance: `NetworkBandwidthInAllowanceExceeded`/`OutAllowanceExceeded`,
  `NetworkPacketsPerSecondAllowanceExceeded` show the instance network cap being hit.

## 5. Replication and availability
- `ReplicationLag` (seconds) on replicas: choose a threshold from your RPO.
- `IsMaster` and ElastiCache events via an SNS notification topic on the replication group.
- Global datastore: `GlobalDatastoreReplicationLag`.

## 6. Example alarm
```bash
aws cloudwatch put-metric-alarm --alarm-name cache-engine-cpu \
  --namespace AWS/ElastiCache --metric-name EngineCPUUtilization \
  --dimensions Name=CacheClusterId,Value=sessions-0001-001 \
  --statistic Average --period 60 --evaluation-periods 5 --threshold 90 \
  --comparison-operator GreaterThanThreshold --alarm-actions <sns-arn>
```
Create one alarm per node (the dimension value is the node id such as `sessions-0001-001`), or use CloudWatch metric
math to alarm on the worst node.

## Verify
- [ ] Alarms on EngineCPUUtilization, DatabaseMemoryUsagePercentage, Evictions (where relevant), CurrConnections, ReplicationLag for every production node.
- [ ] Hit rate baseline recorded; dashboard shows it per cluster.
- [ ] SLOWLOG reviewed after any engine CPU alarm.

## Checked
Date: 2026-10-27. Sources: ElastiCache User Guide pages CacheMetrics.WhichShouldIMonitor (CPU guidance, 90% /
cores, memory pressure rule), CacheMetrics.Redis and CacheMetrics.HostLevel (metric names), serverless-metrics-events-redis
(`clusterId` dimension, `ElastiCacheProcessingUnits`, `BytesUsedForCache`), CloudWatchMetrics (namespace and
dimensions). Corrected the serverless metric name (`ECPUs` is not a metric name), the 70%/90% thresholds, the
50 MB swap rule and the 65,000 `maxclients` figure (not found in the documentation read); removed the Metrics Insights
query, the 80% memory and 1-2 s lag thresholds and the failover event name.
Method: documentation only; no commands were run.
