---
id: computing-software.data-engineering.apache-kafka.cluster-linking-and-managed-replication
name: cluster-linking-and-managed-replication
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, geo-replication, cluster-linking, confluent-cluster-linking, mirror-topics, msk-replicator, offset-preserving-replication, cluster-migration]
level: advanced
status: docs-checked
description: "Replicate with Confluent Cluster Linking (offset-preserving mirror topics, promote on failover) or Amazon MSK Replicator instead of self-run MM2; trade-offs and migration use."
sources:
  - https://docs.confluent.io/platform/current/multi-dc-deployments/cluster-linking/index.html
  - https://docs.confluent.io/cloud/current/multi-cloud/cluster-linking/mirror-topics-cc.html
  - https://docs.aws.amazon.com/msk/latest/developerguide/msk-replicator.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cluster Linking and managed replication

**Goal:** replicate between Kafka clusters with less operational burden than MirrorMaker 2, using the vendor mechanism your platform supports.

## Confluent Cluster Linking
Built into Confluent Server and Confluent Cloud, so it needs no Connect cluster. **Mirror topics** are byte-for-byte copies that preserve offsets (globally consistent offsets and identical content across partitions). Consumer group offsets can be synced too (`consumer.offset.sync.enable`).
```bash
# on the destination (Confluent Platform)
kafka-cluster-links --bootstrap-server $DST --create --link primary-to-dr \
  --config-file link.properties              # bootstrap.servers of source, security, consumer.offset.sync.enable=true
kafka-mirrors --bootstrap-server $DST --create --mirror-topic orders.v1 --link primary-to-dr
# failover: make the mirror writable
kafka-mirrors --bootstrap-server $DST --failover --topics orders.v1      # stops mirroring; for disaster recovery
kafka-mirrors --bootstrap-server $DST --promote  --topics orders.v1      # graceful: checks for 0 lag and does a final metadata sync (migration)
```
Confluent CLI: `confluent kafka link create` and `confluent kafka mirror failover|promote` (both take `--link`).
- Both `--failover` and `--promote` permanently convert the mirror topic into a regular, writable topic.
- Source-initiated links mean your datacenter always makes an outbound connection (no firewall holes or special IP filters).
- The destination must be Confluent Server (Confluent Platform 7.8.x or later per the overview page) or Confluent Cloud; the source can be Kafka, Confluent Server or Confluent Cloud.

## Amazon MSK Replicator
Automatic asynchronous replication of data and consumer group offsets between MSK clusters, with no custom code, infrastructure or cross-region networking to manage. It supports cross-region and same-region replication and also replicates topic configurations, ACLs and consumer group offsets. It can also move workloads from self-managed Kafka to MSK Provisioned clusters with consumer group offset synchronization. For pricing see the AWS pricing page.

## Choosing
| Need | Pick |
|---|---|
| OSS Kafka, any vendor, full control | MirrorMaker 2 |
| Confluent destination, offset-identical failover, migrations | Cluster Linking |
| MSK to MSK, minimal ops | MSK Replicator |
| Migration into Confluent Cloud | Cluster Linking (the source can be Kafka) |

## Migration pattern (cluster A -> B)
1. Link/mirror all topics; sync offsets.
2. Move consumers to B (they read mirror topics with synced offsets).
3. Move producers: promote mirrors (writable) and repoint producers.
4. Remove the link once A is idle.

## Checked
2026-10-28. Confirmed on the Confluent Cluster Linking overview and command pages and CLI reference: byte-for-byte mirror topics preserving offsets, built into Confluent Server and Confluent Cloud, destination requirement (Confluent Platform 7.8.x or later), source-initiated links, `kafka-mirrors --failover` and `--promote` behaviour, `consumer.offset.sync.enable`, `confluent kafka mirror failover|promote`; on the MSK Replicator page: asynchronous replication of data, topic configurations, ACLs and consumer group offsets, cross-region and same-region. Removed: pricing structure, IAM requirement, topic-name prefix option, offset-translation claim, partition-count claim.
Method: documentation only; no commands were run.

## Verify
- [ ] Mirror lag stays near zero in steady state.
- [ ] In a drill, `failover` makes the topic writable and consumers continue from synced offsets.
- [ ] Cost estimate from the vendor's current pricing page reviewed.
