---
id: computing-software.data-engineering.apache-kafka.rack-awareness
name: rack-awareness
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, rack-awareness, broker-rack, replica-placement, availability-zones, kafka-topic-design]
level: practitioner
status: docs-checked
description: "Spread Kafka replicas across racks or availability zones with broker.rack, check placement after creation and reassignment, and avoid uneven AZ layouts."
sources:
  - https://kafka.apache.org/documentation/#basic_ops_racks
  - https://github.com/apache/kafka/blob/trunk/docs/operations/basic-kafka-operations.md
  - https://github.com/apache/kafka/blob/trunk/tools/src/main/java/org/apache/kafka/tools/reassign/ReassignPartitionsCommand.java
  - https://github.com/apache/kafka/blob/trunk/server/src/main/java/org/apache/kafka/server/config/ReplicationConfigs.java
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rack awareness (replica placement across AZs)

**Goal:** losing one rack or availability zone never loses all replicas of a partition.

## Configure
On each broker (`server.properties`):
```properties
broker.rack=eu-west-1a        # the AZ/rack name; same string for all brokers in that rack
```
- Set it **before** creating topics: the rack constraint is honoured when a topic is created, modified or its replicas are redistributed, so existing replicas do not move on their own when you add rack information.
- A partition spans min(#racks, replication factor) racks, so RF=3 over 3 AZs puts one replica in each. The same mechanism works for other groupings such as availability zones.
- Keep the **same number of brokers per rack**. The assignment keeps the number of leaders per broker constant, but racks with fewer brokers get more replicas and use more storage and replication resources.
- If some brokers lack rack information, `kafka-reassign-partitions.sh --generate` fails with "Not all brokers have rack information" unless you pass `--disable-rack-aware`, which assigns replicas without rack awareness (do not).

## Check placement
```bash
kafka-topics.sh --bootstrap-server $BS --describe --topic orders
```
Map broker ids to racks with the Admin API (each `Node` returned by `describeCluster` has a rack), then check that for every partition the set of racks of its replicas has size min(RF, racks). Topics created before racks were configured, or reassigned with a hand-written plan, can violate it. Fix with a `kafka-reassign-partitions.sh --generate` plan, which is rack-aware unless `--disable-rack-aware` is given.

## Pair with
- `min.insync.replicas=2` and RF=3 over 3 AZs: survives one AZ loss while still accepting `acks=all` writes.
- Consumers can read from a nearby follower: set `client.rack` on the consumer and `replica.selector.class` on the brokers (default selector returns the leader; `org.apache.kafka.common.replica.RackAwareReplicaSelector` is the rack-based implementation).
- KRaft controllers need a majority alive, so with controllers in only two AZs, losing the AZ that holds the majority stops the quorum; spread them across three.

## Verify
- [ ] Every partition's replicas span distinct racks.
- [ ] Simulate AZ loss in staging (stop one rack's brokers): no offline partitions, producers with acks=all keep writing.

## Checked

2026-10-25, against Apache Kafka trunk documentation (apache/kafka docs/, commit date 2026-10-24). Confirmed: `broker.rack`, the min(#racks, replication-factor) spanning rule, constant leaders per broker with uneven replica counts across unequal racks, rack handling at topic creation, modification and redistribution, `--disable-rack-aware` and its error text (ReassignPartitionsCommand source), `replica.selector.class` default (returns the leader) and `client.rack`, and `Node` carrying a rack. Fixed: the earlier claim that lone brokers carry far more leaders is wrong (leaders stay constant, replicas do not), and the mixed-rack failure belongs to `--generate`, not topic creation. Removed: Strimzi and Cruise Control references and the `kafka-broker-api-versions.sh | grep rack` check.

Method: documentation only; no commands were run.
