---
id: computing-software.cloud-infrastructure-engineering.aws.msk-and-amazon-mq
name: msk-and-amazon-mq
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, msk, managed-kafka, kafka, msk-serverless, msk-connect, amazon-mq, activemq, rabbitmq, iam-auth, sasl-scram, mtls, broker-storage, tiered-storage, lambda-event-source-mapping, message-broker, jms, amqp]
level: practitioner
status: draft
description: "Choose and run Amazon MSK (provisioned vs serverless, IAM/SCRAM/mTLS auth, storage autoscaling, MSK Connect) and Amazon MQ (ActiveMQ/RabbitMQ active-standby brokers) for Kafka/JMS/AMQP workloads."
sources: ["Amazon MSK Developer Guide - Client authentication and authorization", "Amazon MSK Developer Guide - Best practices for standard brokers", "Amazon MSK Developer Guide - MSK Serverless", "Amazon MQ Developer Guide - Broker deployment modes and best practices"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Amazon MSK and Amazon MQ — managed brokers without the 3 a.m. disk-full page

**Goal:** pick the right managed broker, authenticate clients with IAM instead of shared
passwords, and size storage/throughput so the cluster never stalls.
(Topic and partition design is tool-level Kafka knowledge; see
`computing-software.data-engineering.apache-kafka.topic-partition-and-consumer-design`.)

## 1. Which service
| Workload | Service |
|---|---|
| Kafka protocol, high-throughput event streaming, replay, Kafka ecosystem (Connect, Streams, Flink) | **MSK** |
| Lift-and-shift of JMS / AMQP / MQTT / STOMP apps (ActiveMQ, RabbitMQ), queue semantics, request/reply | **Amazon MQ** |
| New app, no protocol constraint, want zero ops | SQS/SNS/EventBridge first; MSK Serverless if Kafka semantics are needed |

## 2. MSK provisioned vs serverless
- **Serverless**: no broker sizing, pays per cluster-hour + per-partition-hour + GB; only
  **IAM auth**; per-cluster throughput caps (hundreds of MiB/s class) and partition caps
  (~2 400 class) — check the quotas page. Good for dev and bursty prod under the caps.
- **Provisioned (standard brokers)**: choose `kafka.m7g.large`+ (Graviton), ≥ 3 brokers across
  3 AZs, replication factor 3, `min.insync.replicas=2`, `acks=all` for durable topics.
- **Express brokers**: higher throughput per broker, storage managed by AWS, faster scaling
  and recovery — pick them for new provisioned clusters unless you need a feature they lack.
- Storage: enable **auto-expansion** (`storage-mode` + scaling policy at ~60 % disk) and
  **tiered storage** for long retention cheaply. A broker at 100 % disk makes the whole
  cluster read-only; alarm on `KafkaDataLogsDiskUsed` > 70 %.
- Rough capacity: use the MSK sizing sheet; keep per-broker ingress under ~70 % of the
  instance's network/EBS throughput and total partitions per broker within the per-size
  recommendation (a few thousand on large sizes).

## 3. Authentication and authorisation
| Method | Notes |
|---|---|
| **IAM** (`SASL/IAM`, port 9098) | No secrets; client uses `aws-msk-iam-auth` jar / `aws-msk-iam-sasl-signer` libs; authz via IAM policy actions `kafka-cluster:Connect`, `WriteData`, `ReadData` on cluster/topic/group ARNs. Preferred. |
| **SASL/SCRAM** (9096) | Users stored in Secrets Manager (secret name must start `AmazonMSK_`, KMS CMK required); authz via Kafka ACLs. |
| **mTLS** (9094) | Certs from a Private CA; authz via ACLs; keep `allow.everyone.if.no.acl.found=false`. |
| Unauthenticated (9092) | Dev only. |
Cluster policies also allow cross-account access and **multi-VPC private connectivity**
(PrivateLink-style) so consumers in other VPCs do not need peering.

## 4. Operations
- Config via a **cluster configuration** (`server.properties`-style): set
  `auto.create.topics.enable=false`, `default.replication.factor=3`,
  `min.insync.replicas=2`, `num.partitions`, `log.retention.hours`.
- Broker patching is a rolling AWS-managed operation; it is only safe if RF ≥ 3 and
  `min.insync.replicas ≤ RF-1`. Clients must retry on `NotLeaderForPartition`.
- Rebalance after adding brokers: partitions do not move themselves — use **Cruise Control**
  or `kafka-reassign-partitions.sh` from a bastion/container in the VPC.
- Monitoring levels: `PER_TOPIC_PER_PARTITION` for lag; or **open monitoring** (Prometheus
  JMX/Node exporter) scraped by AMP/Grafana. Key metrics: `UnderReplicatedPartitions` (> 0 bad),
  `ActiveControllerCount` (must be 1), `MaxOffsetLag`, `CpuUser+CpuSystem` < 60 %.
- **Lambda** reads MSK via an event source mapping (IAM auth, consumer group auto-created);
  **MSK Connect** runs Connect plugins (Debezium, S3 sink) as managed workers with autoscaling.

## 5. Amazon MQ
- Engines: **ActiveMQ Classic** (JMS/OpenWire, STOMP, MQTT, AMQP 1.0) and **RabbitMQ** (AMQP 0-9-1).
- Deployment: `SINGLE_INSTANCE` (dev) or **active/standby** across two AZs with EFS-backed
  storage (ActiveMQ) / **cluster** of 3 nodes (RabbitMQ). Failover changes the endpoint —
  clients must use the `failover:(ssl://a,ssl://b)` transport (ActiveMQ) or reconnect logic.
- Brokers live in your VPC; private access by default. Scale by instance size
  (`mq.m5.large`…); throughput-sensitive ActiveMQ apps benefit from
  `concurrentStoreAndDispatchQueues=false` for small messages and from avoiding persistent
  messages they do not need.
- RabbitMQ quorum queues are the durable default; classic mirrored queues are deprecated.
- Alarms: `CpuUtilization`, `StorePercentUsage` (ActiveMQ; 100 % = producer flow control),
  `MessageUnacknowledgedCount` per queue, `RabbitMQMemUsed` vs high watermark.

## Gotchas
- MSK IAM auth throughput: each client connection is signed; connection storms (Lambda scale-out
  without keep-alive) hit `kafka-cluster:Connect` throttles — reuse clients.
- Changing broker instance type or auth modes on a provisioned cluster is a rolling update of
  tens of minutes per broker; schedule it.
- Topics with RF=1 lose data on every patch cycle; MSK will not stop you.
- Amazon MQ active/standby is not load-balanced: the standby does nothing until failover.
- Unconfirmed: current MSK Serverless caps and Express broker instance list — verify in docs.

## Verify
- [ ] Clients connect on 9098 with IAM; 9092 is blocked by the security group.
- [ ] `UnderReplicatedPartitions` stays 0 during a forced broker reboot (`reboot-broker`).
- [ ] Disk-used alarm at 70 % and storage auto-expansion policy exist.
- [ ] Producer `acks=all`, topics RF=3 / `min.insync.replicas=2` (`kafka-topics --describe`).
- [ ] Amazon MQ: kill the active broker; clients reconnect via failover transport within seconds.
