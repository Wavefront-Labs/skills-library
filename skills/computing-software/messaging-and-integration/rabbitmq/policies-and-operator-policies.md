---
id: computing-software.messaging-and-integration.rabbitmq.policies-and-operator-policies
name: policies-and-operator-policies
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, policies-and-operator-policies, rmq-policies]
level: practitioner
status: docs-checked
description: "Use policies and operator policies for runtime settings with priority and pattern matching."
sources:
  - https://www.rabbitmq.com/docs/policies
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Policies and operator policies

**Goal:** Change queue behaviour without redeploying clients.

## Steps
1. `rabbitmqctl set_policy -p app1 --priority 5 --apply-to queues name "^pattern" '{"max-length":1000}'`. The default priority is 0.
2. At most one policy matches a queue or exchange; the one with the highest priority wins.
3. Operator policies (`rabbitmqctl set_operator_policy`) are merged with the regular policy before being applied. When both set the same key, the more conservative value is used (operator `max-length` 50 beats regular 100, but regular 20 beats operator 50). An operator policy also takes precedence over client-provided arguments. Operator policies are limited to a few arguments listed in the guide.
4. Some arguments cannot be set by policy because they are fixed at declaration time, for example the queue type.

## Failure modes
- Overlapping patterns pick a single winner by priority, not a merge of both.

## Verify
- `rabbitmqctl list_policies`.

## Checked

Date: 2026-11-02. Confirmed on the Policies guide: one matching policy, priority default 0 and highest wins, operator-policy merge and conservative-value rule, override of client arguments, queue type not settable by policy, `set_operator_policy` and `list_policies` in the rabbitmqctl man page. Fixed: "operator policies override or cap user policies" was imprecise. Removed: `list_queues name policy` as a check.

Method: documentation only; no commands were run.
