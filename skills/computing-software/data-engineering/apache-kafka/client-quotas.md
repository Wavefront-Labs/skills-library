---
id: computing-software.data-engineering.apache-kafka.client-quotas
name: client-quotas
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, kafka-operations, kafka-quotas, producer-byte-rate, consumer-byte-rate, request-percentage, throttle-time, multi-tenant, noisy-neighbour]
level: advanced
status: docs-checked
description: "Protect a shared Kafka cluster with client quotas: produce/fetch byte rates and request percentage per user/client-id, defaults vs overrides, and detecting throttling in clients."
sources:
  - https://kafka.apache.org/documentation/#design_quotas
  - https://kafka.apache.org/documentation/#quotas
  - https://kafka.apache.org/documentation/#monitoring
  - https://github.com/apache/kafka/blob/trunk/docs/operations/basic-kafka-operations.md
  - https://github.com/apache/kafka/blob/trunk/docs/operations/multi-tenancy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Client quotas

**Goal:** one runaway producer or a backfill consumer cannot saturate brokers for everyone else.

## Quota types (enforced per broker)
| Quota | Limits |
|---|---|
| `producer_byte_rate` | Bytes/s produced by the entity on each broker |
| `consumer_byte_rate` | Bytes/s fetched |
| `request_percentage` | Share of broker network and I/O thread time: `n` means n% of one thread, out of a total of `(num.io.threads + num.network.threads) * 100` % |
| `controller_mutation_rate` | Rate of topic and partition creations, deletions and partition additions (KIP-599) |
By default clients have an unlimited quota. A broker that detects a violation does not reject: it returns a response carrying the delay, mutes the client's channel until the delay is over (a throttled fetch response contains no data), and well-behaved clients also pause.

## Entities and precedence
Quotas apply to `(user, client-id)`, `user`, or `client-id`, with defaults at each level, and all connections of a group share its quota. The most specific match wins, in this order: (1) user and client-id, (2) user and default client-id, (3) user, (4) default user and client-id, (5) default user and default client-id, (6) default user, (7) client-id, (8) default client-id. The user is the authenticated principal; client-id is a name chosen by the client application, so prefer user quotas on clusters with SASL or mTLS.

## Commands
```bash
# default for all users
kafka-configs.sh --bootstrap-server $B --alter --entity-type users --entity-default \
  --add-config 'producer_byte_rate=10485760,consumer_byte_rate=20971520,request_percentage=50'
# (user, client-id) pair: --entity-type users --entity-name u --entity-type clients --entity-name c
# override for a heavy pipeline
kafka-configs.sh --bootstrap-server $B --alter --entity-type users --entity-name etl-backfill \
  --add-config 'consumer_byte_rate=104857600'
# inspect
kafka-configs.sh --bootstrap-server $B --describe --entity-type users --entity-name etl-backfill
kafka-configs.sh --bootstrap-server $B --describe --entity-type users --entity-default
```
Quotas are defined per broker (the docs reject a cluster-wide quota because it would need usage shared across brokers): a client group can use the configured rate on each broker. Quota overrides are stored in the metadata log and take effect immediately, with no restart.

## Replication throttles are separate
`leader.replication.throttled.rate` and `follower.replication.throttled.rate` (dynamic broker properties, with `replica.alter.log.dirs.io.max.bytes.per.second`) throttle replication traffic, not client quotas.

## Detecting throttling
- Broker metrics: `kafka.server:type={Produce|Fetch},user=...,client-id=...` with attributes `throttle-time` (ms the client was throttled, ideally 0) and `byte-rate`; `kafka.server:type=Request,user=...,client-id=...` with `throttle-time` and `request-time`. When a per-client-id quota applies, the user is not specified; when a per-user quota applies, the client-id is not.
Expose throttle time in team dashboards so "Kafka is slow" tickets can be answered with "you are hitting your quota".

## Verify
- [ ] A load test as a quota'd user shows throughput capped near the quota on each broker and non-zero throttle time.
- [ ] Other tenants' latency stays flat during the test.
- [ ] Quotas are kept in version control with topics and ACLs.

## Checked

2026-10-25, against Apache Kafka trunk documentation (apache/kafka docs/, commit date 2026-10-24). Confirmed: quota types and their `kafka-configs.sh` syntax including `--entity-default` and the (user, client-id) form, the eight-step precedence order, per-broker enforcement and the delay-and-mute mechanism, the request-percentage definition, `controller_mutation_rate` (multi-tenancy page, KIP-599), the quota metric MBeans and `throttle-time`/`byte-rate`/`request-time` attributes, and the replication throttle property names. Removed: the client-side `produce-throttle-time-*` and `fetch-throttle-time-*` names (not in the monitoring page) and the "6x cluster-wide" arithmetic.

Method: documentation only; no commands were run.
