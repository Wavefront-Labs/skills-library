---
id: computing-software.messaging-and-integration.rabbitmq.mandatory-and-returns
name: mandatory-and-returns
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, mandatory-and-returns]
level: practitioner
status: docs-checked
description: "Publish with the mandatory flag and handle basic.return to detect unroutable messages."
sources:
  - https://www.rabbitmq.com/docs/publishers
  - https://www.rabbitmq.com/docs/confirms
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mandatory flag and returns

**Goal:** Detect when no queue received a message.

## Steps
1. Set mandatory=true on basic.publish.
2. Register a returned-message handler; an unroutable mandatory message is returned to the publisher with `basic.return`.
3. With confirms on, `basic.return` is sent before the `basic.ack`, so a confirm still arrives for the returned message.
4. Combine with confirms for end-to-end publishing safety.

## Failure modes
- The publisher must have a returned-message handler, or returns go unhandled.
- `mandatory` is `false` by default, so unroutable messages are discarded (or sent to an alternate exchange) silently. A message routed via an alternate exchange counts as routed.

## Verify
- Publish to a key with no binding and see the return handler fire.

## Checked

Date: 2026-11-02. Confirmed in the Publishers guide (docs/publishers, unroutable messages), Confirms guide (return before ack) and Alternate Exchanges page. Removed as not stated there: reply code 312 NO_ROUTE.

Method: documentation only; no commands were run.
