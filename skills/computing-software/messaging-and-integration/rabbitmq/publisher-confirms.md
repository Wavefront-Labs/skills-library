---
id: computing-software.messaging-and-integration.rabbitmq.publisher-confirms
name: publisher-confirms
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, publisher-confirms, rmq-publishers]
level: practitioner
status: docs-checked
description: "Use publisher confirms to learn when the broker has accepted responsibility for a message, and handle nacks."
sources:
  - https://www.rabbitmq.com/docs/confirms
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Publisher confirms

**Goal:** Never lose a published message silently.

## Steps
1. Enable with confirm.select on the channel.
2. Track outstanding sequence numbers (the `delivery-tag` of `basic.ack`/`basic.nack`). For routable messages the ack is sent once all queues accepted the message: persisted to disk for persistent messages on durable queues, and accepted by a quorum of replicas for quorum queues.
3. Process confirms asynchronously, or publish batches and wait for outstanding confirms; ack latency under load can reach a few hundred milliseconds.
4. A `basic.nack` is sent only on an internal error in the process responsible for a queue; the client may republish. No message is both confirmed and nacked, and ack order can differ from publish order.

## Failure modes
- A channel in confirm mode cannot be made transactional and vice versa; transactions are unnecessarily heavyweight.
- A confirm means queues accepted the message, not that a consumer processed it.

## Verify
- Kill a node mid-publish in a test and confirm every message is confirmed or retried.

## Checked

Date: 2026-11-02. Confirmed in the Consumer Acknowledgements and Publisher Confirms guide (docs/confirms): `confirm.select`, when acks are sent, nack conditions, latency, ordering, transactions. Removed: the "slow" label for transactions (the guide says heavyweight).

Method: documentation only; no commands were run.
