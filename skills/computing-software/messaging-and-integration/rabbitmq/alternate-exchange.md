---
id: computing-software.messaging-and-integration.rabbitmq.alternate-exchange
name: alternate-exchange
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, alternate-exchange]
level: practitioner
status: docs-checked
description: "Catch unroutable messages with an alternate-exchange policy bound to a fanout exchange feeding a parking queue."
sources:
  - https://www.rabbitmq.com/docs/ae
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Alternate exchange

**Goal:** Capture messages that no binding matches instead of dropping them.

## Steps
1. Create a fanout exchange `unroutable` and a durable queue `unroutable.q` bound to it.
2. Set the policy: `rabbitmqctl set_policy ae "^orders$" '{"alternate-exchange":"unroutable"}' --apply-to exchanges`.
3. Alert on the depth of unroutable.q.

## Failure modes
- Defining the alternate exchange through declare arguments is discouraged; use a policy. If both are set, the argument overrules the policy, and the user needs `read` on the exchange and `write` on the alternate exchange.
- If the alternate exchange cannot route the message, it tries its own alternate exchange, if any; the chain ends when the message is routed, the chain runs out or an exchange repeats. A missing alternate exchange only logs a warning.
- A message routed through an alternate exchange still counts as routed for the `mandatory` flag.

## Verify
- Publish a message with no matching key and confirm it lands in unroutable.q.

## Checked

Date: 2026-11-02. Confirmed in the Alternate Exchanges page (docs/ae): the policy command form, argument precedence and permissions, chaining, mandatory interaction. Corrected: an AE that cannot route passes the message to its own AE rather than dropping it.

Method: documentation only; no commands were run.
