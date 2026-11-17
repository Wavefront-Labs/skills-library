---
id: computing-software.messaging-and-integration.nats.queue-groups
name: queue-groups
category: computing-software
field: messaging-and-integration
product: nats
tags: [queue-groups, load-balancing, work-queue, geo-affinity]
level: practitioner
status: docs-checked
description: "Use NATS queue subscriptions to load balance work: one random member per message, naming rules, no-responder, and stream-as-queue."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/nats-concepts/core-nats/queue-groups/queue.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: spread messages across competing consumers with no server configuration.

Subscribers that register under the same queue name form a queue group. A message on the subject is delivered to every ordinary subscriber, but to only one randomly chosen member of each queue group. Queue groups are defined purely by the subscribing applications, not by server config, so adding another instance scales out and terminating one (after a drain on a signal) scales in without duplicates.

Rules and details:
- Queue group names follow subject naming rules: case sensitive, no whitespace. A hierarchy with `.` is allowed, and some server features such as queue permissions can match them with wildcards.
- If a request targets a service where the server knows no queue member subscribes, the server returns a no-responders protocol message so blocking calls break immediately.
- Streams as queues: with JetStream, set the stream retention to `WorkQueuePolicy` and use pull consumers for horizontal scaling, or an explicit-ack push consumer with a queue group of subscribers.
- In a super-cluster, queue service requests go to another cluster only when no local listener can handle them, giving automatic geo-affinity.

Gotcha: core queue groups are at-most-once; use JetStream when messages must survive consumer absence.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
