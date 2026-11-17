---
id: computing-software.data-engineering.apache-kafka.kraft-mode-and-zookeeper-migration
name: kraft-mode-and-zookeeper-migration
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, kafka-operations, kraft, zookeeper-migration, controller-quorum, kafka-storage-format, metadata-quorum, process-roles, kafka-4]
level: sme
status: docs-checked
description: "Run Kafka in KRaft mode: controller quorum layout, formatting storage with a cluster id, checking quorum health, and the ZooKeeper-to-KRaft migration path before Kafka 4.0."
sources:
  - https://kafka.apache.org/documentation/#kraft
  - https://github.com/apache/kafka/blob/trunk/docs/operations/kraft.md
  - https://github.com/apache/kafka/blob/3.9/docs/operations/kraft.md
  - https://github.com/apache/kafka/blob/trunk/docs/getting-started/upgrade.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KRaft mode and ZooKeeper migration

**Goal:** run Kafka metadata on the built-in Raft quorum (required from Kafka 4.0, which removed ZooKeeper) and migrate existing ZooKeeper clusters safely.

## Layout
- **Controllers** (`process.roles=controller`): a majority must be alive, so 3 controllers tolerate 1 failure and 5 tolerate 2. Combined `broker,controller` servers are simpler for small use cases such as development; their disadvantage is that controller and broker failures are no longer isolated from each other.
- **Brokers** (`process.roles=broker`) learn metadata from the active controller.
```properties
# controller.properties
process.roles=controller
node.id=3001
controller.quorum.bootstrap.servers=ctl1:9093,ctl2:9093,ctl3:9093    # older static form: controller.quorum.voters
listeners=CONTROLLER://:9093
controller.listener.names=CONTROLLER
log.dirs=/var/lib/kafka/meta
```

## Bootstrap a new cluster
```bash
CLUSTER_ID=$(kafka-storage.sh random-uuid)                    # same id on every node
kafka-storage.sh format --cluster-id $CLUSTER_ID --config controller.properties --standalone   # first controller
kafka-storage.sh format --cluster-id $CLUSTER_ID --config broker.properties
```
`--standalone` bootstraps a one-voter quorum and the other controllers are added dynamically (the recommended method); alternatively `--initial-controllers "<id>@<host>:<port>:<directory-uuid>,..."` bootstraps several voters, with the same value on every controller. Kafka no longer auto-formats storage directories: every server must be formatted with the cluster id before first start.

## Health checks
```bash
kafka-metadata-quorum.sh --bootstrap-server $B describe --status        # LeaderId, HighWatermark, voters
kafka-metadata-quorum.sh --bootstrap-server $B describe --replication   # lag per voter/observer
kafka-features.sh --bootstrap-server $B describe                         # metadata.version, kraft.version
```
Watch for controller leadership changing repeatedly and for voter or observer lag growing. `kafka-metadata-shell.sh` inspects the cluster metadata partition.

## ZooKeeper -> KRaft migration (bridge release 3.9)
The current documentation points to the 3.9 documentation for the steps: migration needs a bridge release and the last one is 3.9. Phases: initial (ZK controller), initial metadata load, hybrid (some brokers still ZK mode, KRaft controller), dual-write (all brokers KRaft, controller still writes to ZK), finalized.
1. Upgrade brokers to 3.9.1 with `inter.broker.protocol.version=3.9`. Do not change the metadata version during the migration.
2. Deploy KRaft controllers with `zookeeper.metadata.migration.enable=true` and `zookeeper.connect`, formatted with the existing cluster id (`get /cluster/id` in `zookeeper-shell.sh`). KRaft `node.id` values must differ from every ZK `broker.id`.
3. Roll the ZK brokers with `zookeeper.metadata.migration.enable=true`, `controller.quorum.bootstrap.servers` and `controller.listener.names` (add the controller listener to the protocol map). The migration starts when the last broker restarts; the active controller logs "Completed migration of metadata from Zookeeper to KRaft".
4. Reconfigure and roll the brokers as KRaft brokers.
5. Finalize by rolling the controllers without migration and ZooKeeper settings. After finalization you cannot revert to ZooKeeper mode.
Then upgrade to 4.x: 4.0 and later support only KRaft mode, and a ZooKeeper-mode cluster must be migrated first.

## Gotchas
- Features not fully implemented in KRaft block migration: check the 3.9 documentation limitations before starting. Also, a ZK broker with several log directories shuts down on any directory failure during migration (KAFKA-16431).
- ACLs move to `StandardAuthorizer` (`authorizer.class.name=org.apache.kafka.metadata.authorizer.StandardAuthorizer`).
- Check the finalized `metadata.version` and `kraft.version` with `kafka-features.sh describe`, and raise them with `kafka-features.sh upgrade` only after all nodes run the new binaries.

## Verify
- [ ] `describe --status` shows the expected voters and a stable leader.
- [ ] All brokers appear as observers in `kafka-metadata-quorum.sh describe --replication`.
- [ ] After migration, no broker config references `zookeeper.connect`.

## Checked

2026-10-25, against Apache Kafka trunk documentation (apache/kafka docs/, commit date 2026-10-24) and the 3.9 branch kraft.md. Confirmed: majority rule and 3/5 controller fault tolerance, combined-server trade-off, `--standalone` and `--initial-controllers` formatting and why formatting is explicit, `kafka-metadata-quorum.sh describe --status/--replication`, `kafka-features.sh describe` showing `kraft.version` and `metadata.version`, `controller.quorum.bootstrap.servers` replacing `controller.quorum.voters`, the migration phases, 3.9.1 and IBP 3.9 prerequisite, `zookeeper.metadata.migration.enable`, node id rule, finalization being irreversible (3.9 branch kraft.md), and that Kafka 4.0 and later support only KRaft (upgrade notes). Fixed: "dual-write" does not happen when brokers first roll (it follows all brokers becoming KRaft). Removed: the unconfirmed per-feature 3.x availability list and `kafka-cluster.sh list-endpoints`.

Method: documentation only; no commands were run.
