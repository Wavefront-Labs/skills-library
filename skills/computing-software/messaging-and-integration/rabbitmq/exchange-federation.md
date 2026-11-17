---
id: computing-software.messaging-and-integration.rabbitmq.exchange-federation
name: exchange-federation
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, exchange-federation, rmq-federation]
level: advanced
status: docs-checked
description: "Replicate messages from an upstream exchange to a downstream exchange across clusters using the federation plugin."
sources:
  - https://www.rabbitmq.com/docs/federation
  - https://www.rabbitmq.com/docs/federation-reference
  - https://www.rabbitmq.com/docs/federated-exchanges
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exchange federation

**Goal:** Share events between clusters over WAN safely.

## Steps
1. `rabbitmq-plugins enable rabbitmq_federation rabbitmq_federation_management`.
2. Define an upstream: `rabbitmqctl set_parameter federation-upstream up1 '{"uri":"amqps://user:PASS@host"}'`.
3. Policy: `rabbitmqctl set_policy fed "^fed\." '{"federation-upstream-set":"all"}' --apply-to exchanges`.
4. Use TLS and least-privilege users on the link; `localhost`-restricted users such as `guest` will not work remotely.

## Failure modes
- Federation is asynchronous and tolerates unreliable connections.
- Loops: `max-hops` (default 1) limits how many links a message crosses; with more than one route, messages may still be duplicated.
- Mixing exchange types across a federation gives confusing routing.

## Verify
- Management UI Admin > Federation Status > Running Links shows the link running.

## Checked

Date: 2026-11-02. Confirmed on the Federation, Federation Reference and Federated Exchanges pages. Removed: "ordering across links is not guaranteed" for exchanges; "set max-hops" as a loop fix without the default and duplication caveat.

Method: documentation only; no commands were run.
