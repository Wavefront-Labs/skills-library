---
id: computing-software.data-engineering.apache-kafka.kafka-version-upgrades
name: kafka-version-upgrades
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, kafka-operations, kafka-upgrade, metadata-version, inter-broker-protocol-version, rolling-upgrade, client-compatibility, kafka-features, kafka-4]
level: sme
status: docs-checked
description: "Upgrade Kafka safely: read upgrade notes, roll binaries, then bump metadata.version (KRaft) or inter.broker.protocol.version (ZK); client compatibility and rollback."
sources:
  - https://kafka.apache.org/40/getting-started/upgrade/
  - https://kafka.apache.org/39/getting-started/upgrade/
  - https://kafka.apache.org/39/operations/kraft/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kafka version upgrades

**Goal:** move brokers (and clients) to a new Kafka release with a rollback path until you deliberately close it.

## Plan
1. Read the target release's **Upgrade notes** section in full (and every intermediate release's notes): removed configs, changed defaults, protocol removals. Kafka 4.0 removed ZooKeeper mode, the `log.message.format.version` / `message.format.version` configs and many deprecated configs and tools, and removed old protocol API versions (KIP-896): clients, Connect and Streams must be on 2.1 or later before upgrading to 4.0, and brokers must be 2.1 or later before upgrading Java clients to 4.0.
2. Check supported upgrade paths: 4.0 upgrades are supported from 3.3.x through 3.9.x in KRaft mode; KRaft clusters older than 3.3 should go to 3.9.x first, and ZooKeeper clusters must be migrated to KRaft before upgrading to 4.0.
3. Test in a staging cluster with production-like clients.

## KRaft cluster procedure
```bash
# 0. record current feature level
kafka-features.sh --bootstrap-server $B describe
# 1. rolling restart every node (controllers first or brokers first per notes) onto new binaries, same configs
#    (see rolling-restarts-and-leader-balancing; wait for URP=0 between nodes)
# 2. soak for days; rollback = roll back binaries (metadata.version unchanged keeps this possible)
# 3. finalise
kafka-features.sh --bootstrap-server $B upgrade --metadata 3.9      # or --release-version 4.0 in 4.x
```
Raising `metadata.version` enables new features and makes binary downgrade unsafe (downgrade of metadata.version is often not supported or lossy).

## ZooKeeper cluster (pre-4.0)
Follow the "Upgrading" notes of the target 3.x release: set `inter.broker.protocol.version` to the current version, roll new binaries, soak, then bump `inter.broker.protocol.version` to the new version with a second roll. Check that release's notes for the `log.message.format.version` step.

## Clients
- Check the compatibility matrix and KIP-896 for client and broker version minimums (2.1 for 4.0).
- Upgrade Kafka Streams apps carefully: some versions need the `upgrade.from` setting for a rolling-bounce upgrade (see the notes for your version pair).
- Default changes in clients bite (e.g. `enable.idempotence=true` and `acks=all` by default since 3.0; producing to brokers older than 2.8.0 then needs the `IDEMPOTENT_WRITE` permission; consumer `session.timeout.ms` 45 s since 3.0).

## Verify
- [ ] All nodes run the new binaries and `kafka-features.sh --bootstrap-server $B describe` shows the expected finalized `metadata.version`.
- [ ] Client error rates unchanged through the roll.
- [ ] `metadata.version` bumped only after the agreed soak period, and recorded in the change log.

## Checked
2026-10-28. Confirmed in the Kafka 3.9 and 4.0 upgrade notes and FeatureCommand source (3.9): 4.0 is KRaft only, supported from 3.3.x to 3.9.x, finalize with `kafka-features.sh upgrade --release-version 4.0` (and `--metadata` in 3.x), metadata downgrade unsupported when versions carry metadata changes, clients and brokers must be 2.1 or later for 4.0 (KIP-896), message-format configs removed in 4.0, `upgrade.from` for Streams, `enable.idempotence` default and the `IDEMPOTENT_WRITE` note (brokers older than 2.8.0). Removed: the Java version claim, the ZooKeeper `log.message.format.version` remark, the Connect ordering advice and the `kafka-broker-api-versions.sh` verification.
Method: documentation only; no commands were run.
