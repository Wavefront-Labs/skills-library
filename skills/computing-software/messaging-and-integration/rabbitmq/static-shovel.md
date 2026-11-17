---
id: computing-software.messaging-and-integration.rabbitmq.static-shovel
name: static-shovel
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, static-shovel]
level: advanced
status: docs-checked
description: "Define shovels in the configuration file for fixed topologies; changes need a restart."
sources:
  - https://www.rabbitmq.com/docs/shovel-static
  - https://www.rabbitmq.com/docs/shovel
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Static shovel

**Goal:** Keep a permanent shovel as code.

## Steps
1. Define shovels in the advanced configuration file under the `rabbitmq_shovel` application's `shovels` clause (Erlang terms); each element is a named static shovel and names must be distinct.
2. Common keys include `reconnect-delay` and `ack-mode`, plus protocol-specific source and destination sections.
3. Static shovels start on node boot; changing one requires a node restart. The docs recommend dynamic shovels for most users.

## Failure modes
- Any change needs a restart, which makes static shovels inflexible.

## Verify
- `rabbitmqctl shovel_status`.

## Checked

2026-11-02. Confirmed in docs/shovel and docs/shovel-static: advanced.config location, shovels clause, distinct names, reconnect-delay and ack-mode keys, restart requirement, preference for dynamic shovels; rabbitmqctl shovel_status in docs/shovel. Removed: "declarative config in newer versions" and "syntax errors stop plugin startup" (not in pages).
Method: documentation only; no commands were run.
