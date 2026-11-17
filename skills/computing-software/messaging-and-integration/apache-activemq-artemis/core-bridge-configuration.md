---
id: computing-software.messaging-and-integration.apache-activemq-artemis.core-bridge-configuration
name: core-bridge-configuration
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,core-bridge,bridge,queue-name,forwarding-address,concurrency,static-connectors,discovery-group-ref,activemq-artemis]
level: practitioner
status: docs-checked
description: "Forward messages from a local queue to an address on another broker with a core bridge: queue-name, forwarding-address, filter, routing-type, concurrency and connectors."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/core-bridges.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Core bridges: configuration

**Goal:** reliably forward messages from a source queue to a target address, typically on another broker (even across a WAN, outside any cluster). Both ends must be Artemis brokers; for other JMS 1.1 providers use a JMS bridge, which needs XA for the same once-and-only-once guarantee.

```xml
<bridge name="my-bridge">
   <queue-name>sausage-factory</queue-name>
   <forwarding-address>mincing-machine</forwarding-address>
   <ha>true</ha>
   <filter string="name='aardvark'"/>
   <routing-type>PASS</routing-type>
   <concurrency>1</concurrency>
   <static-connectors>
      <connector-ref>remote-connector</connector-ref>
   </static-connectors>
</bridge>
```
- `name`: unique in the server. `queue-name`: mandatory; the local queue must already exist when the bridge starts.
- `forwarding-address`: if omitted, the message's original address is kept.
- `ha` (default `false`): connect to any available server in a cluster and support failover.
- `filter`: only matching messages are forwarded. Optional `transformer-class-name` modifies header or body.
- `routing-type`: `ANYCAST`, `MULTICAST`, `PASS` (default) or `STRIP`.
- `concurrency` (default `1`): for high-latency, high-throughput links; N creates N bridges named `myBridge-0` .. `myBridge-N-1`, each with its own `BridgeControl`.
- Connect with `static-connectors` (list of `connector-ref`) or `discovery-group-ref` (`discovery-group-name`), not both.
- `user`/`password`: default to the cluster user and password. `client-id` labels the connection on the remote broker.

## Checked

Method: docs-checked 2026-11-09 against core-bridges.adoc (read in full). Removed the Verify step.
