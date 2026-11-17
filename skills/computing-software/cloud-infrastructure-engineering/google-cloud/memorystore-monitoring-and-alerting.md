---
id: computing-software.cloud-infrastructure-engineering.google-cloud.memorystore-monitoring-and-alerting
name: memorystore-monitoring-and-alerting
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, memorystore, memorystore-monitoring, redis-metrics, alerting, eviction]
level: practitioner
status: docs-checked
description: "Monitor Memorystore for Redis and Valkey: memory usage ratio, evictions, CPU per node, connections, cache hit ratio and replication lag, with alert thresholds that matter."
sources: ["https://docs.cloud.google.com/memorystore/docs/redis/supported-monitoring-metrics", "https://docs.cloud.google.com/memorystore/docs/redis/monitor-instances", "https://docs.cloud.google.com/memorystore/docs/redis/memory-management-best-practices", "https://docs.cloud.google.com/memorystore/docs/valkey/monitor-instances"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Memorystore monitoring and alerting

## 1. Key metrics (Redis: `redis.googleapis.com/...`)
| Metric | Alert when |
|---|---|
| `stats/memory/system_memory_usage_ratio` | reaches 80% (Google's recommended alert); at 100% writes are blocked with `-OOM command not allowed under OOM prevention.` |
| `stats/memory/system_memory_overload_duration` | any value: writes are being blocked |
| `stats/memory/usage_ratio` | trending toward 1: how close the working set is to maxmemory; evictions follow unless the policy is no-eviction |
| `stats/evicted_keys` | rate > 0 if the cache must not evict (session stores) |
| `stats/cpu_utilization_main_thread` | sustained high: CPU is a common cause of latency |
| `clients/connected` | approaching `maxclients`; also watch `stats/reject_connections_count` |
| `stats/cache_hit_ratio` | drop vs baseline |
| `replication/offset_diff`, `replication/role` | replica lag (bytes not replicated), failover role changes |
For Memorystore for Valkey see its own monitoring page for metric names.

## 2. Alert policy example
```yaml
displayName: memorystore-system-memory-high
combiner: OR
conditions:
- displayName: system memory > 80%
  conditionThreshold:
    filter: resource.type="redis_instance" AND metric.type="redis.googleapis.com/stats/memory/system_memory_usage_ratio"
    comparison: COMPARISON_GT
    thresholdValue: 0.8
    duration: 300s
    aggregations: [{alignmentPeriod: 60s, perSeriesAligner: ALIGN_MAX}]
```
`gcloud monitoring policies create --policy-from-file=policy.yaml`

## 3. Responding
- System memory high while used memory is low = fragmentation: turn on `activedefrag` (Redis 4.0+; Memorystore defaults it to no, and it costs CPU), lower maxmemory, or scale up.
- High usage ratio: review the eviction policy, add TTLs, or scale.
- CPU hot: compare command latency with the `commands/usec_per_call` and `commands/total_time` metrics.

## Gotchas
- Persistence work (RDB export) raises memory use; track `persistence/rdb/bgsave_in_progress` against memory spikes.

## Checked
2026-10-31. Confirmed against the Memorystore for Redis supported-metrics page (metric names, `cpu_utilization_main_thread`, `reject_connections_count`, replication metrics) and the memory-management best-practices page (80% system memory alert, OOM error text, `activedefrag` default and CPU trade-off, `redis_instance` monitored resource). Removed unconfirmed: 0.9 thresholds, 65k maxclients, `is_in_failover`, Valkey metric prefix, eviction-policy value, SLOWLOG advice, alignment claim. Policy YAML field names follow the Cloud Monitoring alert policy API.
Method: documentation only; no commands were run.

## Verify
- [ ] Dashboard per instance shows the table above; a test alert fires to the on-call channel.
