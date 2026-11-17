---
id: computing-software.messaging-and-integration.apache-activemq-artemis.clustered-message-grouping
name: clustered-message-grouping
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,clustered-grouping,grouping-handler,local-handler,remote-handler,group-timeout,activemq-artemis]
level: sme
status: docs-checked
description: "Configure LOCAL and REMOTE grouping-handler elements for message groups across a cluster, and understand its single point of failure and best practices."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/message-grouping.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Clustered message grouping

The manual says clustered grouping is not recommended: ordered consumption is serial, which defeats horizontal scaling. If you still need it, each node needs to know which group ids are bound to which queue on which node, solved by grouping handlers in `broker.xml`.

```xml
<grouping-handler name="my-grouping-handler">
   <type>LOCAL</type>
   <address>jms</address>
   <timeout>5000</timeout>
</grouping-handler>
<grouping-handler name="my-grouping-handler">
   <type>REMOTE</type>
   <address>jms</address>
   <timeout>5000</timeout>
</grouping-handler>
```
- `type`: pick one node per cluster with a `LOCAL` handler; all others use `REMOTE` and talk to it. The LOCAL handler makes the routing decision.
- `address`: refers to the cluster connection and the address it uses.
- `timeout`: how long to wait for a decision; the send throws an exception when reached, preserving strict ordering.

The receiving node proposes a route (round-robin among queues, local first, queue with a consumer); once accepted every node routes that group to that queue and normal single-server grouping pins the consumer.

## Single point of failure
If the node with the LOCAL handler crashes, no decisions are made and sends fail. Replicate it: create a backup configured with the same LOCAL handler.

## Best practices
Distribute consumers evenly and avoid closing them (a queue left with no consumers keeps receiving its group). Prefer durable queues. Always replicate the LOCAL handler node. If you use group timeouts, the remote node should have a smaller group-timeout, at least half the value on the main coordinator.

## Checked
2026-11-03. Confirmed against the Artemis user manual page message-grouping, section Clustered Grouping: grouping-handler XML, type, address, timeout, routing proposal, single point of failure and best practices. Removed: the Verify step.
Method: documentation only; no commands were run.
