---
id: computing-software.cloud-infrastructure-engineering.aws.msk-consumer-lag-and-monitoring-levels
name: msk-consumer-lag-and-monitoring-levels
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, msk, consumer-lag, open-monitoring, enhanced-monitoring, kafka-metrics, prometheus]
level: advanced
status: docs-checked
description: "Monitor Amazon MSK: monitoring levels, the broker metrics that predict trouble (CPU, disk, under-replicated partitions), consumer lag metrics, and Open Monitoring with Prometheus."
sources: ["https://docs.aws.amazon.com/msk/latest/developerguide/metrics-details.html", "https://docs.aws.amazon.com/msk/latest/developerguide/consumer-lag.html", "https://docs.aws.amazon.com/msk/latest/developerguide/open-monitoring.html", "https://docs.aws.amazon.com/msk/latest/developerguide/bestpractices.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MSK consumer lag and monitoring

## 1. Monitoring levels (provisioned clusters)
| Level | Adds | Cost |
|---|---|---|
| `DEFAULT` | `ActiveControllerCount`, `OfflinePartitionsCount`, `CpuUser`/`CpuSystem`, `KafkaDataLogsDiskUsed`, `HeapMemoryAfterGC`, `BytesInPerSec`, `BytesOutPerSec`, `UnderReplicatedPartitions`, `UnderMinIsrPartitionCount`, `ConnectionCount`, `GlobalPartitionCount`, and the consumer lag metrics `MaxOffsetLag`, `SumOffsetLag`, `EstimatedMaxTimeLag` | free |
| `PER_BROKER` | adds metrics such as `ConnectionCreationRate` and replication and remote-fetch byte rates | paid |
| `PER_TOPIC_PER_BROKER` | adds per-topic metrics | paid |
| `PER_TOPIC_PER_PARTITION` | adds per-partition metrics such as `OffsetLag` (high cardinality) | paid |
```bash
aws kafka update-monitoring --cluster-arn <arn> --current-version <ver> --enhanced-monitoring PER_BROKER
```
Consumer lag metrics (`EstimatedMaxTimeLag`, `EstimatedTimeLag`, `MaxOffsetLag`, `OffsetLag`,
`SumOffsetLag`) are supported on Apache Kafka 2.2.1 or later. The first three of the group-level
set are free at `DEFAULT`; `OffsetLag` and `EstimatedTimeLag` need the per-partition level. They are
emitted only while a consumer group is `STABLE` or `EMPTY`, and are absent when the group has no
committed offsets, the group name contains a colon, or the name contains non-ASCII characters
(CloudWatch drops them).

## 2. Alarms that matter
| Metric | Threshold | Why |
|---|---|---|
| `ActiveControllerCount` (Sum over brokers) | != 1 | controller problems |
| `OfflinePartitionsCount` | > 0 | partitions unavailable |
| `UnderReplicatedPartitions` / `UnderMinIsrPartitionCount` | > 0 sustained | replication falling behind; producers with `acks=all` will fail on min ISR |
| `CpuUser + CpuSystem` per broker | average > 60% (AWS recommends staying under 60%) | headroom for broker failure, patching and rolling upgrades |
| `KafkaDataLogsDiskUsed` | >= 85% | act before disks fill (scale storage, adjust retention or use tiered storage) |
| `HeapMemoryAfterGC` | > 60% | memory pressure |
| `MaxOffsetLag` / `EstimatedMaxTimeLag` per consumer group | above SLO (e.g. 60 s) | consumers falling behind |
| `ConnectionCount`, `ConnectionCreationRate` (the latter needs `PER_BROKER`) | spikes | client misconfiguration (reconnect storms) |

## 3. Interpreting lag
- Growing `SumOffsetLag` with flat producer rate: consumers too slow (processing time,
  too few consumers; max useful consumers = partitions).
- Lag on one partition only: hot key or a stuck consumer instance; check
  `PER_TOPIC_PER_PARTITION` or `kafka-consumer-groups.sh --describe --group g`.
- Rebalancing storms (lag sawtooth): `max.poll.interval.ms` exceeded by slow processing;
  tune `max.poll.records` or use cooperative rebalancing.

## 4. Open Monitoring with Prometheus
```bash
aws kafka update-monitoring --cluster-arn <arn> --current-version <ver> \
  --open-monitoring '{"Prometheus":{"JmxExporter":{"EnabledInBroker":true},"NodeExporter":{"EnabledInBroker":true}}}'
```
Scrape the broker endpoints from inside the VPC (the security group must allow the exporter
ports listed on the MSK Open Monitoring page). Open monitoring is free, but cross-AZ data transfer
is charged. It can publish to Amazon Managed Service for Prometheus; CloudWatch metrics remain
for alarms. KRaft-mode clusters and Express brokers cannot have open monitoring and public access
both enabled.

## 5. Broker logs
Enable broker log delivery to CloudWatch Logs, S3 or Firehose for error investigations
(`--logging-info`).

## Verify
- [ ] Monitoring level at least PER_BROKER for production; alarms above exist.
- [ ] Consumer lag dashboards per group with SLO thresholds.
- [ ] Disk usage under 85% with auto scaling or tiered storage configured.

## Checked

2026-10-27, AWS documentation (current release as read on that date). MSK Developer Guide metrics-by-monitoring-level, consumer lag, open monitoring and best practices pages; botocore kafka 2018-11-14 model. Fixed: BytesInPerSec, BytesOutPerSec, UnderReplicatedPartitions, UnderMinIsrPartitionCount, HeapMemoryAfterGC and ConnectionCount are free DEFAULT-level metrics (the skill put the first four at PER_BROKER); OffsetLag and EstimatedTimeLag need PER_TOPIC_PER_PARTITION; lag metrics need Kafka 2.2.1 or later, a STABLE or EMPTY group and ASCII group names without a colon. Confirmed: 60 percent CPU, 85 percent data disk and 60 percent heap guidance, the four monitoring level names, update-monitoring open-monitoring structure, open monitoring is free apart from cross-AZ transfer. Removed the exporter port numbers 11001 and 11002, the Lambda OffsetLag remark and the Serverless metric-set remark, which the pages do not confirm.
Method: documentation only; no commands were run.
