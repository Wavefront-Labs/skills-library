---
id: computing-software.cloud-infrastructure-engineering.aws.msk-replicator-cross-region
name: msk-replicator-cross-region
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, msk, kafka, msk-replicator, cross-region-kafka, kafka-replication, mirrormaker, consumer-group-offset-sync, active-passive, active-active, disaster-recovery, iam-auth]
level: advanced
status: docs-checked
description: "Replicate Kafka topics and consumer offsets between MSK clusters across Regions or accounts with MSK Replicator: setup, topic naming, failover/failback and lag monitoring."
sources: ["https://docs.aws.amazon.com/msk/latest/developerguide/msk-replicator.html", "https://docs.aws.amazon.com/msk/latest/developerguide/msk-replicator-monitor.html", "https://docs.aws.amazon.com/msk/latest/developerguide/msk-replicator-create-cli.html", "https://docs.aws.amazon.com/msk/latest/developerguide/msk-replicator-troubleshooting.html", "https://docs.aws.amazon.com/msk/latest/developerguide/msk-replicator-patterns.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MSK Replicator — cross-Region Kafka replication

**Goal:** topics, configurations and consumer group offsets in a primary MSK cluster are
continuously copied to a cluster in another Region (or the same Region) without running
MirrorMaker 2 yourself, so consumers can fail over and resume close to where they were.

## 1. Prerequisites
- Both clusters are MSK clusters in the **same AWS account** when replicating between MSK
  clusters (self-managed Kafka to MSK Provisioned is also supported). Create the source and
  target clusters first. Replicator authenticates with IAM, so the clusters need IAM access control.
- For cross-Region replication, the source cluster needs multi-VPC connectivity turned on for IAM
  access control and a cluster policy (see the MSK multi-VPC pages).
- A service execution role that can read and write the source and target clusters, including
  writing to topics. A wrong role shows up as `AuthError` or `ReplicatorFailure` above 0.

## 2. Create
```bash
aws kafka create-replicator --replicator-name orders-to-usw2 --region us-west-2 \
  --service-execution-role-arn arn:aws:iam::<ACCOUNT_ID>:role/msk-replicator \
  --kafka-clusters '[
    {"AmazonMskCluster":{"MskClusterArn":"<SOURCE_ARN>"},"VpcConfig":{"SubnetIds":["subnet-a","subnet-b"],"SecurityGroupIds":["sg-src"]}},
    {"AmazonMskCluster":{"MskClusterArn":"<TARGET_ARN>"},"VpcConfig":{"SubnetIds":["subnet-c","subnet-d"],"SecurityGroupIds":["sg-tgt"]}}]' \
  --replication-info-list '[{"SourceKafkaClusterArn":"<SOURCE_ARN>","TargetKafkaClusterArn":"<TARGET_ARN>",
    "TargetCompressionType":"GZIP",
    "TopicReplication":{"TopicsToReplicate":["orders.*"],"TopicsToExclude":[],"CopyTopicConfigurations":true,
       "CopyAccessControlListsForTopics":true,"DetectAndCopyNewTopics":true,
       "StartingPosition":{"Type":"EARLIEST"},"TopicNameConfiguration":{"Type":"IDENTICAL"}},
    "ConsumerGroupReplication":{"ConsumerGroupsToReplicate":[".*"],"SynchroniseConsumerGroupOffsets":true,"DetectAndCopyNewConsumerGroups":true}}]'
```
Allowed values in the API model: `StartingPosition.Type` is `LATEST` or `EARLIEST`;
`TopicNameConfiguration.Type` is `PREFIXED_WITH_SOURCE_CLUSTER_ALIAS` or `IDENTICAL` (the CLI
examples in the guide write `PREFIXED`, so check the current accepted spelling);
`TargetCompressionType` is `NONE`, `GZIP`, `SNAPPY`, `LZ4` or `ZSTD` and is required;
`ConsumerGroupOffsetSyncMode` is `LEGACY` or `ENHANCED`. Log delivery to CloudWatch Logs, S3 or
Firehose is off by default (`--log-delivery`).

## 3. Topic naming decides your topology
- **Prefixed**: the target topic name carries a source-cluster prefix (`<sourceClusterAlias>.orders`),
  so replicas are distinguishable from local topics; consumers that read both must subscribe to both names.
- **Identical** names: the target topic is `orders`. Simplest for **active-passive** DR because
  consumers point at the new bootstrap and keep the same topic names. Read the guide's
  "Replication patterns" page (active-passive, active-active) before using identical names in
  both directions.

## 4. Failover / failback
1. Planned failover: stop producers to the primary and confirm replicator lag is near zero.
2. Point producers and consumers to the target bootstrap; consumers resume from the
   synchronized consumer group offsets. Replicator optimizes offset sync for consumers reading near
   the end of a partition, so lagging consumers can show higher lag on the target; design consumers
   to tolerate reprocessing.
3. Failback and unplanned failover steps are in the "Replication patterns" page.

## 5. Monitor
CloudWatch metrics in the **target** cluster's Region, namespace `AWS/Kafka`, dimension
`ReplicatorName`: `ReplicationLatency`, `MessageLag` and `ReplicatorThroughput` (topic and
aggregate level), plus `ReplicatorFailure`, `AuthError` and `ThrottleTime`; also
`KafkaClusterPingSuccessCount` for reachability. Alarm on `MessageLag` against your RPO and on
any `ReplicatorFailure` or `AuthError` above 0.

## Gotchas
- Target cluster must have capacity (storage, partitions, throughput) for the replicated
  load plus its own.
- The Troubleshooting page lists a recommended minimum partition count per throughput; check it
  when replication latency grows.

## Verify
- [ ] `describe-replicator` shows `RUNNING`; a new topic matching the pattern appears on the target.
- [ ] Produce N messages on source, consume N on target; `MessageLag` returns to ~0.
- [ ] Failover drill: a consumer group restarts on target and reprocesses only a small, bounded window.

## Checked

2026-10-27, AWS documentation (current release as read on that date). MSK Developer Guide Replicator overview, monitoring, CLI creation, troubleshooting and patterns pages; botocore kafka 2018-11-14 model (CreateReplicator, enums, ReplicatorState). Fixed: MSK-to-MSK replication requires both clusters in the same AWS account (the skill said cross-account); metrics are read in the target Region; removed the invented kafka.amazonaws.com principal in the source cluster policy. Conflict noted: the guide CLI examples use TopicNameConfiguration PREFIXED while the API model enum is PREFIXED_WITH_SOURCE_CLUSTER_ALIAS. Confirmed: create-replicator parameters, StartingPosition, TargetCompressionType, ConsumerGroupOffsetSyncMode and ReplicatorState values, metric names ReplicationLatency, MessageLag, ReplicatorThroughput, ReplicatorFailure, AuthError, ThrottleTime. Removed unsourced claims on identical-name loops, periodic config copying, partition counts, exactly-once and cost.
Method: documentation only; no commands were run.
