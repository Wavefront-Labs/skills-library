---
id: computing-software.messaging-and-integration.rabbitmq.routing-slip-and-process-manager
name: routing-slip-and-process-manager
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, routing-slip-and-process-manager]
level: advanced
status: docs-checked
description: "Carry the itinerary in a header so each step forwards to the next."
sources:
  - https://www.enterpriseintegrationpatterns.com/patterns/messaging/
  - https://www.rabbitmq.com/docs/dlx
  - https://www.rabbitmq.com/docs/exchanges
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Routing slip

**Goal:** Dynamic multi-step routing.

## Steps
1. Put the remaining steps in a message header (AMQP 0-9-1 headers are a key/value table, so a list or a delimited string both work).
2. Each processor removes its own step, then publishes to the exchange of the next step, for example the default exchange or a direct exchange bound per step.
3. Configure a dead letter exchange on each step queue (see the dead-letter-channel skill) so failed or rejected slips are kept.
4. Where the flow needs central state and branching rather than a fixed list, use a process manager instead; it is a separate component keeping per-instance state, not a RabbitMQ feature.

## Failure modes
- Skipping a step on a bad slip; validate the slip at the first step.

## Verify
- Follow a message through all steps.

## Checked
2026-11-09. Routing Slip and Process Manager confirmed as named patterns on the Enterprise Integration Patterns messaging index. Dead lettering of rejected messages confirmed on the RabbitMQ Dead Letter Exchanges page; exchange types confirmed on the Exchanges page. The pattern content is design advice with no RabbitMQ figures or flags to verify. Removed: the specific header example `slip=a,b,c`, which is illustrative only, and the version note.
Method: documentation only; no commands were run.
