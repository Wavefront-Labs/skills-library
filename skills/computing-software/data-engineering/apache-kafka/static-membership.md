---
id: computing-software.data-engineering.apache-kafka.static-membership
name: static-membership
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, kafka-consumer, consumer-groups, static-membership, group-instance-id, session-timeout-ms, rolling-deploy, rebalancing, kubernetes-statefulset, kip-345]
level: advanced
status: docs-checked
description: "Stop rebalance storms on deploys with Kafka static membership: stable group.instance.id per pod, session.timeout.ms sizing, StatefulSet naming, and duplicate-id fencing errors."
sources:
  - https://cwiki.apache.org/confluence/display/KAFKA/KIP-345%3A+Introduce+static+membership+protocol+to+reduce+consumer+rebalances
  - https://kafka.apache.org/39/configuration/consumer-configs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Static consumer group membership

**Goal:** restarting a consumer (rolling deploy, pod reschedule) does not trigger a group-wide rebalance, so partitions and local state stay put.

## How it works (KIP-345)
With `group.instance.id` set, the broker remembers which partitions belong to that instance. When it leaves (without sending LeaveGroup) and returns within `session.timeout.ms`, it gets the same assignment back with no rebalance. Dynamic members (no id) trigger a rebalance on every leave and every join.

## Configure
```properties
group.id=billing-projector
group.instance.id=${POD_NAME}          # unique AND stable across restarts
session.timeout.ms=120000              # longer than a typical restart; must be within the broker's group.min/max.session.timeout.ms
heartbeat.interval.ms=3000             # lower than session.timeout.ms, typically no higher than 1/3 of it
partition.assignment.strategy=org.apache.kafka.clients.consumer.CooperativeStickyAssignor
```
Kubernetes: run consumers as a **StatefulSet** so pod names (`billing-0`, `billing-1`) are stable, and inject via the downward API:
```yaml
env:
  - name: POD_NAME
    valueFrom: {fieldRef: {fieldPath: metadata.name}}
```
A StatefulSet names Pods `$(statefulset name)-$(ordinal)` (Kubernetes StatefulSet docs); a Deployment does not give that stable identity.

## Trade-offs
- A crashed instance's partitions are not reassigned until `session.timeout.ms` expires: lag builds for that long. Choose the timeout as the longest expected restart time plus margin.
- Scaling down: the removed instance id keeps its partitions until `session.timeout.ms` expires.
- Two live processes with the same `group.instance.id` fence each other; seeing fencing errors in logs usually means duplicate ids (copy-pasted config, two pods with the same env).

## Kafka Streams
Streams passes consumer configs through to its consumers; combined with persistent state stores on a persistent volume, a stable instance id avoids state restoration after restarts (see the Streams configuration docs).

## Checked
2026-10-28. Confirmed against the Kafka 3.9 consumer configuration page and KIP-345: `group.instance.id` behaviour (a static member that shuts down keeps its partitions until `session.timeout.ms` expires), `session.timeout.ms` bounded by `group.min.session.timeout.ms` and `group.max.session.timeout.ms`, `heartbeat.interval.ms` guidance (below session timeout, typically at most 1/3). Removed: version numbers, `FencedInstanceIdException` name, `removeMembersFromConsumerGroup`, KIP-848 paragraph and the default broker maximum.
Method: documentation only; no commands were run.

## Verify
- [ ] `kafka-consumer-groups.sh --describe --group billing-projector --members --verbose` shows `GROUP-INSTANCE-ID` per member.
- [ ] A rolling restart does not trigger a rebalance for the other members.
- [ ] Killing a pod permanently moves its partitions after `session.timeout.ms`.
