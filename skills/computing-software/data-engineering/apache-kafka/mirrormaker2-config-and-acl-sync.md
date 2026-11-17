---
id: computing-software.data-engineering.apache-kafka.mirrormaker2-config-and-acl-sync
name: mirrormaker2-config-and-acl-sync
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, mirrormaker2, acl-sync, topic-config-sync, kafka-geo-replication, sync-topic-configs, config-properties-exclude]
level: practitioner
status: docs-checked
description: "Keep mirrored Kafka topics' configs, partitions and ACLs in step with MirrorMaker 2: sync intervals, exclusion lists, ACL downgrade to READ, and what never syncs."
sources:
  - https://kafka.apache.org/documentation/#georeplication-mirrormaker
  - https://github.com/apache/kafka/blob/trunk/connect/mirror/src/main/java/org/apache/kafka/connect/mirror/MirrorSourceConfig.java
  - https://github.com/apache/kafka/blob/trunk/connect/mirror/src/main/java/org/apache/kafka/connect/mirror/MirrorSourceConnector.java
  - https://github.com/apache/kafka/blob/trunk/connect/mirror/src/main/java/org/apache/kafka/connect/mirror/DefaultConfigPropertyFilter.java
  - https://github.com/apache/kafka/blob/trunk/docs/security/authorization-and-acls.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Topic config and ACL synchronisation in MirrorMaker 2

MirrorSourceConnector does more than copy records: it creates remote topics and periodically syncs their configuration, partition counts and ACLs.

## Settings
```properties
primary->dr.sync.topic.configs.enabled=true                 # default true
primary->dr.sync.topic.configs.interval.seconds=600
primary->dr.sync.topic.acls.enabled=true                    # default true
primary->dr.sync.topic.acls.interval.seconds=600
primary->dr.refresh.topics.interval.seconds=600              # new topics and partition increases
primary->dr.config.properties.exclude=follower\.replication\.throttled\.replicas, leader\.replication\.throttled\.replicas, message\.timestamp\.difference\.max\.ms, log\.message\.timestamp\.before\.max\.ms, log\.message\.timestamp\.after\.max\.ms, message\.timestamp\.type, unclean\.leader\.election\.enable, mirror\.unclean\.leader\.election\.enable, min\.insync\.replicas   # this is the default list
replication.factor=3                                         # RF for newly created remote topics (default 2)
```
- Partition increases on the source are mirrored; decreases are impossible in Kafka.
- `config.properties.exclude` (topic properties and/or regexes that are not replicated) keeps local-only settings out; the default list above is why `min.insync.replicas` on the target is not overwritten. It is read by the default `config.property.filter.class`, `DefaultConfigPropertyFilter`, and a custom filter class can replace it.
- Topic config sync applies the source configuration to the remote topics with incremental alter-config operations.

## ACL sync rules
- Only ACLs on **topics** with a **literal** resource pattern, for topics MM2 replicates, are synced; the target ACL names the remote topic with a literal pattern. Prefixed topic ACLs are not synced.
- `ALLOW ... WRITE` ACLs are skipped, and `ALLOW ... ALL` ACLs are downgraded to `READ` on the target, so remote topics stay read-only for everyone except MM2. Other ACL entries, including DENY entries, are copied as they are.
- Group, cluster and transactional-id ACLs are **not** synced: manage those (including consumer group ACLs needed for failover) through your own ACL tooling on both clusters.
- Listing ACLs on the source needs Describe on the Cluster resource (DescribeAcls) and creating them on the target needs Alter on the Cluster resource (CreateAcls).

## Not synced
Consumer group offsets are handled separately by the checkpoint connector (`emit.checkpoints.enabled`, `sync.group.offsets.enabled`).

## Verify
- [ ] Change `retention.ms` on a source topic; within the interval the remote topic shows it (`kafka-configs --describe`).
- [ ] Remote topic ACLs list READ for principals that have WRITE on source.
- [ ] Failover runbook covers group ACLs and write permissions for producers on the DR cluster.

## Checked

2026-10-25, against Apache Kafka trunk documentation (apache/kafka docs/, commit date 2026-10-24). Confirmed against MirrorSourceConfig, MirrorSourceConnector and DefaultConfigPropertyFilter source: `sync.topic.configs.enabled` and `sync.topic.acls.enabled` (default true), the 600 second intervals for config sync, ACL sync and topic refresh, `replication.factor` default 2, the default `config.properties.exclude` list, `config.property.filter.class`, ACL sync filtering (topic resources with LITERAL patterns only, ALLOW WRITE skipped, ALLOW ALL downgraded to READ, target LITERAL), and the ACL operations for DescribeAcls and CreateAcls (authorization docs). Fixed: prefixed ACLs are not synced, `ALLOW WRITE` is skipped rather than downgraded, DENY entries are not excluded, and the exclude default list was incomplete. Removed: `use.incremental.alter.configs` (not present in the current source), the same-principal-names advice, and the list of items MM2 does not sync that no source covers.

Method: documentation only; no commands were run.
