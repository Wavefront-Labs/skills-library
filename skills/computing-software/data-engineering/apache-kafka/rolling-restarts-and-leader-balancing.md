---
id: computing-software.data-engineering.apache-kafka.rolling-restarts-and-leader-balancing
name: rolling-restarts-and-leader-balancing
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, kafka-operations, rolling-restart-kafka, controlled-shutdown, preferred-leader-election, kafka-leader-election, auto-leader-rebalance, under-replicated-partitions, maintenance]
level: advanced
status: docs-checked
description: "Restart Kafka brokers one at a time without client impact: controlled shutdown, zero under-replicated partitions between brokers, then preferred leader election."
sources:
  - https://kafka.apache.org/40/operations/basic-kafka-operations/
  - https://kafka.apache.org/40/configuration/broker-configs/
  - https://kafka.apache.org/40/operations/kraft/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rolling restarts and leader balancing

**Goal:** apply config changes, OS patches, or upgrades to every broker with no lost writes and no prolonged client errors.

## Preconditions
- All topics RF >= 3 with `min.insync.replicas=2` (otherwise a single broker restart blocks `acks=all` producers or makes partitions unavailable).
- `controlled.shutdown.enable=true` (default): on SIGTERM the broker migrates leadership away before stopping, so clients see only a quick leader change.
- Cluster healthy: `UnderReplicatedPartitions == 0` before starting.

## Procedure (per broker, one at a time)
```bash
# 1. check health
kafka-topics.sh --bootstrap-server $B --describe --under-replicated-partitions    # must print nothing
kafka-topics.sh --bootstrap-server $B --describe --under-min-isr-partitions        # must print nothing
# 2. stop gracefully (SIGTERM, never kill -9); give controlled shutdown enough time to finish
systemctl stop kafka
# 3. apply change, start
systemctl start kafka
# 4. wait until the broker has caught up: URP back to 0
watch -n 10 "kafka-topics.sh --bootstrap-server $B --describe --under-replicated-partitions | wc -l"
# 5. only then move to the next broker
```
Find the active KRaft controller with `kafka-metadata-quorum.sh --bootstrap-server $B describe --status` (`LeaderId`).

Kubernetes operators such as Strimzi and managed services automate this loop; check their docs for how they gate each restart.

## Leader balancing afterwards
After restarts, leadership is concentrated on the brokers that stayed up. Kafka rebalances to **preferred leaders** (first replica in the list) automatically if `auto.leader.rebalance.enable=true` (default; checks every `leader.imbalance.check.interval.seconds`=300 when imbalance > 10%). Force it:
```bash
kafka-leader-election.sh --bootstrap-server $B --election-type preferred --all-topic-partitions
```

## Gotchas
- Unclean shutdown (kill -9, OOM) triggers log recovery on start: can take a long time for many partitions; `num.recovery.threads.per.data.dir` speeds it.
- Restarting the next broker while URP > 0 can drop partitions below min ISR -> producer `NotEnoughReplicas` errors.
- Client `request.timeout.ms`/`delivery.timeout.ms` must tolerate a leader move (defaults do).

## Verify
- [ ] URP and under-min-ISR were 0 before each broker restart.
- [ ] Producer error rate stayed ~0 during the roll (check client metrics `record-error-rate`).
- [ ] After the roll, leaders per broker are balanced (`kafka-topics.sh --describe` leader counts or `LeaderCount` JMX).

## Checked
2026-10-28. Confirmed in the Kafka 3.9/4.0 operations and configuration pages and TopicCommand source (3.9): `controlled.shutdown.enable`, `auto.leader.rebalance.enable`, `leader.imbalance.check.interval.seconds` default 300, `leader.imbalance.per.broker.percentage` default 10, `kafka-leader-election.sh --election-type preferred --all-topic-partitions`, `kafka-topics.sh --describe --under-replicated-partitions` and `--under-min-isr-partitions`, `kafka-metadata-quorum.sh ... describe --status` with `LeaderId`, `NotEnoughReplicas`. Removed: the systemd `TimeoutStopSec` figure, the claim about Strimzi's pre-roll partition check, and the controller-last rationale.
Method: documentation only; no commands were run.
