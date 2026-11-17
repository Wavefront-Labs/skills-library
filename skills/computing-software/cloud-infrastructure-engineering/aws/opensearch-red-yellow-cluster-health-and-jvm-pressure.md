---
id: computing-software.cloud-infrastructure-engineering.aws.opensearch-red-yellow-cluster-health-and-jvm-pressure
name: opensearch-red-yellow-cluster-health-and-jvm-pressure
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, opensearch, cluster-health-red, jvm-memory-pressure, unassigned-shards, clusterindexwritesblocked, troubleshooting]
level: advanced
status: docs-checked
description: "Recover OpenSearch Service domains from red/yellow status, JVM memory pressure and write blocks using cat APIs, allocation explain and the AWS-recommended CloudWatch alarms."
sources: ["https://docs.aws.amazon.com/opensearch-service/latest/developerguide/handling-errors.html", "https://docs.aws.amazon.com/opensearch-service/latest/developerguide/cloudwatch-alarms.html", "https://docs.aws.amazon.com/opensearch-service/latest/developerguide/bp.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenSearch red/yellow health and JVM pressure

## 1. Status meanings
- **Red**: at least one primary shard and its replicas are not allocated to a node.
  Automated snapshots keep being attempted but fail while red persists. Most common causes:
  failed nodes, and the OpenSearch process crashing under continuous heavy load.
- **Yellow**: primaries for all indexes are allocated but replicas for at least one index
  are not. Single-node clusters always start yellow (no node to hold the replica). Multi-node
  clusters can be briefly yellow after creating an index or after a node failure, and lack of
  disk space can also cause it.

## 2. Diagnose red
- `GET /_cluster/allocation/explain` picks the first unassigned shard it finds and explains
  why it cannot be allocated.
- `GET /_cat/indices?v` shows each index's health, doc count and disk use. "Ultimately, red
  shards cause red clusters, and red indexes cause red shards."
- Deleting red indexes is the fastest fix. If that is not feasible: restore a snapshot,
  delete documents, change index settings, reduce replicas, or delete other indexes to free
  disk. Fix red before reconfiguring the domain; reconfiguring while red can leave the domain
  stuck in Processing.
- Retention clock: automated snapshots are kept 14 days regardless of status, so a red state
  lasting over two weeks can delete the last healthy snapshot and lose data. If continuously
  red for over an hour the service tries rerouting unallocated shards or restoring snapshots.
  After 14 days red, domains with one AZ, no dedicated masters or T2/T3 instances get daily
  warnings for 7 days, then unassigned shards on red indexes are deleted at 21 days.
- Check snapshots with `GET domain_endpoint/_snapshot/cs-automated/_all` (or
  `cs-automated-enc` for encrypted domains).

## 3. ClusterBlockException
- **Storage:** when a node has less than the minimum of 20% free space or 20 GiB, basic
  writes can fail. Watch `FreeStorageSpace`; `GET /_cat/allocation?v` shows disk use. Fix by
  scaling to larger instances, more instances or more EBS storage.
- **High JVM memory pressure:** when `JVMMemoryPressure` exceeds 92% for 30 minutes the
  service blocks all writes (`ClusterBlockException`, and `IndexCreateBlockException` for new
  indexes) to avoid going red. It unblocks when pressure is 88% or lower for five minutes.
  Remedies from the page: keep max heap per node at 32 GB, delete old or unused indexes to
  cut shards, clear the fielddata cache (`POST index-name/_cache/clear?fielddata=true`, which
  can disrupt running queries). Avoid aggregating on text fields (use keyword), size shard
  counts correctly, and use ISM to remove unused indexes.
- **Read-only after quorum loss:** with more than one node the service restores quorum and
  sets the cluster read-only; verify `GET _cat/health?v` is green and indexes are present,
  then `PUT _cluster/settings {"persistent":{"cluster.blocks.read_only":false}}`, or restore
  from a snapshot if red.

## 4. Other documented causes
- **JVM OutOfMemoryError:** a circuit breaker was hit. Defaults: parent
  `indices.breaker.total.limit` 95%, fielddata 40%, request 60%.
- **Garbage collection:** on x86 instances it uses CMS; Graviton uses G1. A rule of thumb on
  all types is to keep heap usage below 80%. `GET domain-endpoint/_nodes/stats/jvm?pretty`
  summarises JVM stats. A pattern of ever smaller drops in `JVMMemoryPressure` suggests
  complex queries or large data fields.
- **Shard limit:** default 1,000 shards per node (`cluster.max_shards_per_node`); options are
  more data nodes, raising the setting, or `_shrink`. AWS also advises at most 25 shards per
  GiB of Java heap per node.
- **Skew:** compare `shards` and `disk.indices` in `GET _cat/allocation`; over 10% from the
  average is significant. Use shard counts that are multiples of the data node count.
- **Failed nodes:** if `Nodes` shows fewer than configured for over a day, contact AWS
  Support. Always keep at least one replica per index.
- **Throttling:** persistent 403 "Request throttled" or 429 means scale vertically.

## 5. Recommended alarms (CloudWatch page)
| Metric condition | Meaning |
|---|---|
| `ClusterStatus.red` max >= 1 for 1 min | red cluster |
| `ClusterStatus.yellow` max >= 1 for 1 min, 5 consecutive | unallocated replica |
| `FreeStorageSpace` min <= 20480 (MiB) | page says to prefer 25% of each node's storage |
| `ClusterIndexWritesBlocked` >= 1 for 5 min | writes blocked |
| `Nodes` min < configured count for 1 day | node unreachable |
| `AutomatedSnapshotFailure` max >= 1 | often a red cluster |
| `CPUUtilization` max >= 80% for 15 min, 3 times | sustained high CPU |
| `JVMMemoryPressure` max >= 95% for 1 min, 3 times | scale vertically |
| `OldGenJVMMemoryPressure` max >= 80% for 1 min, 3 times | old-gen pressure |
| `MasterCPUUtilization` >= 50%; `MasterJVMMemoryPressure` >= 95%; `MasterOldGenJVMMemoryPressure` >= 80% | dedicated master load |
| `KMSKeyError` / `KMSKeyInaccessible` >= 1 | key disabled / deleted or grants revoked |
| `shards.active` >= 25 x heap GiB x data nodes | over the shard recommendation |
| Increase in `ThreadpoolWriteRejected` / `ThreadpoolSearchRejected` >= 1 | rejections |

## Verify
- [ ] Cluster green; no unassigned shards.
- [ ] Red, yellow, `FreeStorageSpace`, `ClusterIndexWritesBlocked` and JVM alarms exist.
- [ ] Every index has at least one replica; unused indexes are removed or managed by ISM.

## Checked
Checked 2026-11-08 against the OpenSearch Service Troubleshooting, Recommended CloudWatch alarms and Best practices pages.
Corrected: the write-block threshold (92% for 30 minutes, released at 88% for 5 minutes; not "requests rejected above 92%"), the alarm thresholds (JVM 95%, old-gen 80%, write-blocked 5 minutes, yellow 5 consecutive), and the clearing of read-only blocks. Removed: the `read_only_allow_delete` null setting, the `_restore` command, the 10-50 GB shard sizing rule, "under about 25 shards per GB" wording, the `from+size` / `search_after` advice and the Multi-AZ-with-standby verify line, none of which the cited pages state.
Method: docs-only read of cited pages, 2026-11-08
