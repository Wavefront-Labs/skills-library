---
id: computing-software.data-engineering.apache-kafka.partition-reassignment-and-cluster-expansion
name: partition-reassignment-and-cluster-expansion
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, kafka-operations, partition-reassignment, kafka-reassign-partitions, cluster-expansion, replication-throttle, increase-replication-factor, cruise-control, broker-decommission]
level: sme
status: docs-checked
description: "Move Kafka partitions safely: rebalance new brokers with kafka-reassign-partitions, throttle replication, raise replication factor, decommission brokers, Cruise Control."
sources:
  - https://kafka.apache.org/documentation/#basic_ops_cluster_expansion
  - https://kafka.apache.org/documentation/#basic_ops_increase_replication_factor
  - https://kafka.apache.org/documentation/#rep-throttle
  - https://github.com/apache/kafka/blob/trunk/docs/operations/basic-kafka-operations.md
  - https://github.com/apache/kafka/blob/trunk/tools/src/main/java/org/apache/kafka/tools/reassign/ReassignPartitionsCommandOptions.java
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Partition reassignment and cluster expansion

**Goal:** add or remove brokers, rebalance load, or raise replication factor without saturating the network or losing availability.

New brokers receive **no existing partitions** automatically: only new topics land on them. You must reassign.

## 1. Generate a plan
```bash
cat > topics.json <<'EOF'
{"version":1,"topics":[{"topic":"orders.checkout.order-placed.v1"},{"topic":"crm.customer.state.v2"}]}
EOF
kafka-reassign-partitions.sh --bootstrap-server $B --topics-to-move-json-file topics.json \
  --broker-list "1,2,3,4,5,6" --generate > plan.txt
# plan.txt contains "Current partition replica assignment" (SAVE for rollback) and "Proposed ..." JSON
```
`--generate` moves all partitions of the listed topics onto the given broker list (replication factor unchanged) and does not study load: you decide which topics move, or hand-edit the proposal. The tool offers three mutually exclusive modes: `--generate`, `--execute` and `--verify`.

## 2. Execute with a throttle
```bash
kafka-reassign-partitions.sh --bootstrap-server $B --reassignment-json-file proposed.json \
  --execute --throttle 50000000 --replica-alter-log-dirs-throttle 100000000   # 50 MB/s between brokers, 100 MB/s between disks
kafka-reassign-partitions.sh --bootstrap-server $B --reassignment-json-file proposed.json --verify
```
- Without a throttle, reassignment copies at full speed and can starve client traffic.
- `--verify` reports progress and **removes the throttle** when the reassignment is complete ("Clearing broker-level throttles ..."): run it until it reports completion, or regular replication stays throttled.
- Change the throttle mid-flight by re-running `--execute` with `--additional`, the same plan file and a new `--throttle`.
- Throttle settings are the dynamic broker properties `leader.replication.throttled.rate`, `follower.replication.throttled.rate` and `replica.alter.log.dirs.io.max.bytes.per.second`, plus the per-topic `leader.replication.throttled.replicas` and `follower.replication.throttled.replicas`; the tool sets all five.
- `--cancel` cancels an active reassignment and `--list` lists active ones.
- Moving in smaller batches limits the load of each run.

## Increase replication factor
Reassign with a longer replica list per partition:
```json
{"version":1,"partitions":[{"topic":"t","partition":0,"replicas":[1,2,3]},{"topic":"t","partition":1,"replicas":[2,3,4]}]}
```
Check the result with `kafka-topics.sh --describe` (ReplicationFactor and Isr). Review `min.insync.replicas` for the new replication factor.

## Decommission a broker
1. Cordon it: `kafka-configs.sh --bootstrap-server $B --alter --add-config cordoned.log.dirs="*" --entity-type brokers --entity-name <id>`.
2. Reassign all its partitions to other brokers; the tool cannot generate a decommissioning plan automatically, so build it from the remaining broker list.
3. Once reassignment is done, shut the broker down and unregister it: `kafka-cluster.sh unregister --bootstrap-server $B --id <id>`.

## Gotchas
- Restore leadership to preferred replicas with `kafka-leader-election.sh --election-type preferred --all-topic-partitions`, or let `auto.leader.rebalance.enable=true` do it.
- Rack awareness: set `broker.rack` on every broker; `--generate` fails if only some brokers have a rack unless `--disable-rack-aware` is used.
- Under-replicated partitions during reassignment are expected, but watch `kafka.server:type=ReplicaManager,name=UnderMinIsrPartitionCount` (ISR below min(`min.insync.replicas`, replica count)), which should stay 0.

## Verify
- [ ] `--verify` reports all reassignments complete and throttles removed.
- [ ] Per-broker disk usage and bytes-in are even after rebalancing.
- [ ] `UnderMinIsrPartitionCount` stayed 0 throughout.

## Checked

2026-10-25, against Apache Kafka trunk documentation (apache/kafka docs/, commit date 2026-10-24). Confirmed (basic operations docs and ReassignPartitionsCommand source): new brokers get no existing partitions, the three tool modes, `--generate` with `--topics-to-move-json-file` and `--broker-list`, `--throttle`, `--replica-alter-log-dirs-throttle`, `--additional`, `--cancel`, `--list`, `--verify` clearing throttles, the five throttle properties, the replication-factor-increase procedure, cordoning and `kafka-cluster.sh unregister` for decommissioning, preferred leader election and `auto.leader.rebalance.enable`, and the `UnderMinIsrPartitionCount` definition. Removed: Cruise Control and managed-service remarks (and the Cruise Control source link), the `--cancel` version gate, the 10% batch and balance figures, and the unsupported `min.insync.replicas=2` advice.

Method: documentation only; no commands were run.
