---
id: computing-software.messaging-and-integration.nats.jetstream-consumer-config
name: jetstream-consumer-config
category: computing-software
field: messaging-and-integration
product: nats
tags: [consumers, ack-policy, pull-consumer, durable, max-ack-pending, backoff]
level: practitioner
status: docs-checked
description: "Configure JetStream consumers: pull vs push, durable vs ephemeral, ack policies, AckWait, MaxDeliver, BackOff, MaxAckPending, filters."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/nats-concepts/jetstream/consumers.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick and configure the consumer that tracks delivery and acknowledgement for a stream.

A consumer is a stateful view of a stream giving at-least-once delivery. The docs recommend pull consumers for new projects (scaling, flow control, error handling); push consumers (set `DeliverSubject`, optional `DeliverGroup` queue group, `FlowControl`, `IdleHeartbeat`, `RateLimit`) suit load balancing or per-message acks; ordered consumers are always ephemeral, unacked, single-threaded replay helpers.

Durable means `Durable` is set. `Name` alone or `InactiveThreshold` do not make a consumer durable; InactiveThreshold only cleans up inactive consumers.

Key fields: `AckPolicy` (`AckExplicit` default, `AckNone`, `AckAll`), `AckWait` (ignored when `BackOff` is set), `MaxDeliver` (default -1, forever), `BackOff` (list of delays, length at most MaxDeliver; applies to ack timeouts, not nak), `MaxAckPending` (flow control across all subscriptions; high for throughput, lower with slow external calls plus a tuned AckWait), `DeliverPolicy` (`DeliverAll`, `DeliverLast`, `DeliverNew`, `DeliverByStartSequence`, `DeliverByStartTime`, `DeliverLastPerSubject`), `ReplayPolicy` (`ReplayInstant` default or `ReplayOriginal`), `FilterSubject` or `FilterSubjects` (not both), `Replicas`, `MemoryStorage`, `HeadersOnly`.

Pull-only limits: `MaxWaiting`, `MaxRequestExpires`, `MaxRequestBatch`, `MaxRequestMaxBytes`.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
