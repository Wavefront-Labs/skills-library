---
id: computing-software.data-engineering.apache-kafka.mirrormaker2-exactly-once
name: mirrormaker2-exactly-once
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, mirrormaker2, mm2-exactly-once, kafka-geo-replication, exactly-once-source, kafka-connect]
level: advanced
status: docs-checked
description: "Run MirrorMaker 2 with exactly-once delivery (Kafka 3.5+): dedicated-mode settings, the preparing then enabled rollout, internal REST, and read_committed on the source consumer."
sources:
  - https://cwiki.apache.org/confluence/display/KAFKA/KIP-656%3A+MirrorMaker2+Exactly-once+Semantics
  - https://kafka.apache.org/documentation/#georeplication-config-exactly-once
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exactly-once MirrorMaker 2

By default MM2 is at-least-once: after a failure, records already copied are copied again, producing duplicates in the target topic. Since Kafka 3.5, MM2 source connectors support KIP-618 exactly-once: records and source offsets are written in one transaction on the target cluster.

## Dedicated MM2 (connect-mirror-maker.sh)
```properties
clusters=primary, dr
primary.bootstrap.servers=p1:9092
dr.bootstrap.servers=d1:9092
primary->dr.enabled=true
primary->dr.topics=orders.*, payments.*
dr.exactly.once.source.support=enabled          # keyed by the TARGET cluster alias
dedicated.mode.enable.internal.rest=true        # required: workers forward task configs/fencing via REST
listeners=http://0.0.0.0:8083                   # internal REST per node, reachable between MM2 nodes
replication.factor=3
```
Set `exactly.once.source.support` for every target cluster that should be written with exactly-once semantics. For an existing MirrorMaker cluster, first set it to `preparing` on all nodes, then to `enabled` in a second round of restarts. Intra-cluster communication (`dedicated.mode.enable.internal.rest=true`, KIP-710) is required, and the Kafka docs recommend securing those REST servers in production. Dedicated-cluster support starts at 3.5.0.

## MM2 on a Kafka Connect cluster
Set `exactly.once.source.support=enabled` on the Connect workers (two-phase rollout: `preparing` then `enabled`), and in the `MirrorSourceConnector` config `"exactly.once.support": "required"`.

## Requirements
- Target brokers support transactions; the principal needs the ACLs listed in the Kafka Connect user guide (exactly-once source section), including `IdempotentWrite`.
- Configure the MirrorMaker consumer that reads the source to filter aborted-transaction records: `us-west.consumer.isolation.level = read_committed` (alias of the source cluster).
- EOS removes **replication** duplicates, not consumer-side reprocessing after failover.

## Costs
Transaction overhead per poll batch: tune `producer.override.linger.ms`/`batch.size` and keep `tasks.max` reasonable. Monitor replication latency (`replication-latency-ms`, listed in the geo-replication metrics) before and after enabling.

## Verify
- [ ] Kill an MM2 node during mirroring; record counts per partition (source end offset minus start vs target) match with read_committed counting.

## Checked
2026-11-01. Confirmed against the Kafka 3.9 docs: geo-replication page (Exactly once section: 3.5.0, `exactly.once.source.support`, `preparing` then `enabled`, `dedicated.mode.enable.internal.rest`, `listeners`, source-side `consumer.isolation.level = read_committed`, `replication-latency-ms`) and Connect user guide (exactly-once source, `exactly.once.support`). Removed: claims that checkpoint/heartbeat connectors skip it, per-flow worker internals, offset-translation lag, target-consumer isolation advice (the docs place read_committed on the source consumer), log-line check.
Method: documentation only; no commands were run.
