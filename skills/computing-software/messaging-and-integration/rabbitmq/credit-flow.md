---
id: computing-software.messaging-and-integration.rabbitmq.credit-flow
name: credit-flow
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, credit-flow, rmq-flow-control]
level: advanced
status: docs-checked
description: "Understand credit-based internal flow control that throttles fast publishers when queues lag."
sources:
  - https://www.rabbitmq.com/docs/flow-control
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Credit flow

**Goal:** Interpret throttled publishers.

## Steps
1. Flow control throttles publishing connections that send faster than the broker can process.
2. A flow-controlled connection shows state `flow` in `rabbitmqctl` and the management UI.
3. Brief `flow` states are normal; investigate if a connection stays in `flow`.

## Failure modes
- A `flow` state is back-pressure, not a bug in itself.

## Verify
- `rabbitmqctl list_connections name state` shows flow.

## Checked

Date: 2026-11-02. Confirmed in the Flow Control page (docs/flow-control): the `flow` state in rabbitmqctl and the management UI. Removed as not checked: the credit-passing mechanism and the advice on where to fix the bottleneck.

Method: documentation only; no commands were run.
