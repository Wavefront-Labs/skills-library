---
id: computing-software.messaging-and-integration.apache-zookeeper.use-cases-hadoop-hbase-kafka
name: use-cases-hadoop-hbase-kafka
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, use-cases, hadoop-failover, hbase, kafka, controller-election]
level: intro
status: docs-checked
description: "How big Apache projects use ZooKeeper: HDFS automatic failover, HBase master election, Kafka controller and broker membership, Solr, Spark and Flink."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperUseCases.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Use cases in Apache projects

- Hadoop HDFS automatic failover: NameNodes hold persistent sessions (expiry triggers failover); an exclusive ephemeral lock znode picks the active one; ZKFC monitors health.
- HBase: master election, server leases, bootstrapping, region assignment, master failover, replication and snapshots.
- Kafka: controller election, topic configuration, ACLs and active broker membership.
- Solr Cloud: configuration management and leader election.
- Spark: leader election and state for standby masters. Flink: JobManager HA.
- Druid: coordinator/overlord election and segment load/drop. Mesos: master election and detection.
- Hive: lock manager for HiveServer2. BookKeeper: ledger and bookie metadata.
- Pulsar: configuration store quorum and local metadata.

Common patterns: leader election, ephemeral membership, configuration store, distributed locks.

Verify: for your project, identify which pattern (election, membership, config, lock) it relies on.

## Checked

Method: docs-checked 2026-11-09 against zookeeperUseCases.html (full page read)
