---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.consensus-based-queues-and-messaging
name: consensus-based-queues-and-messaging
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [replicated-queue, consensus-based-messaging, distributed-consensus, work-queue, leases, atomic-broadcast]
level: advanced
status: docs-checked
description: "Build reliable distributed work queues on consensus: lease-based task claiming, queues as replicated state machines, atomic broadcast, and latency expectations."
sources: ["https://sre.google/sre-book/managing-critical-state/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Consensus-based queues and messaging

All points are from the SRE Book chapter Managing Critical State, section Reliable Distributed Queuing and
Messaging.

## Work queues
- Queues commonly distribute tasks among worker processes, and tolerate the loss of workers fairly easily.
- The system must still ensure claimed tasks are processed. The book recommends a **lease** system instead of
  outright removing a task from the queue when claimed, so a task held by a dead worker becomes claimable
  again.
- The downside: losing the queue stops the whole system. Implementing the queue as a **replicated state
  machine** (an RSM running the same operations in the same order on several processes) minimises that risk.
- Using the queue as a load-balancing device is point-to-point messaging.

## Messaging
- **Atomic broadcast**: messages are received reliably and in the same order by all participants. Chandra and
  Toueg showed it is equivalent to consensus. Not every pub-sub infrastructure provides atomic guarantees.
- Publish-subscribe queues deliver to many subscribers and keep messages as a persistent ordered list; they can
  also implement coherent distributed caches.

## Performance expectation
Queuing and messaging systems often need excellent throughput but not extremely low latency, since they are
seldom directly user-facing. Very high latency can still hurt if claiming time becomes a large share of each
task's processing time.

## Practical notes
Make tasks safe to run twice: a lease can expire while a slow worker is still running. Check your chosen
queue's own documentation for how it provides leases or visibility timeouts and delivery guarantees; this
skill does not cover vendor settings.

## Checked
2026-11-01. Confirmed against the SRE Book chapter Managing Critical State (queuing, atomic broadcast,
pub-sub, throughput versus latency). Removed: the etcd key layout and transaction recipe, all Kafka and KRaft
settings (the Kafka documentation pages returned no text), exactly-once claims and verify targets, which the
chapter does not state.
Method: documentation only; no commands were run.
