---
id: computing-software.data-engineering.apache-kafka.securing-controller-and-inter-broker-listeners
name: securing-controller-and-inter-broker-listeners
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, kafka-security, controller-listener-security, inter-broker-listener, kraft, mtls, listener-security-protocol-map]
level: advanced
status: docs-checked
description: "Lock down KRaft controller and inter-broker listeners: listener maps, mTLS or SASL between nodes, super.users, separate networks, and safe migration from PLAINTEXT."
sources:
  - https://kafka.apache.org/documentation/#listener_configuration
  - https://kafka.apache.org/documentation/#security_rolling_upgrade
  - https://kafka.apache.org/documentation/#kraft
  - https://github.com/apache/kafka/blob/trunk/docs/security/listener-configuration.md
  - https://github.com/apache/kafka/blob/trunk/docs/security/incorporating-security-features-in-a-running-cluster.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Securing controller and inter-broker listeners

Clients are usually secured first; the internal listeners are often left PLAINTEXT, so anyone on the network can impersonate a broker, read replicated data or alter cluster metadata.

## Listener layout (KRaft combined example)
```properties
process.roles=broker,controller
listeners=CLIENT://:9093,REPLICATION://:9094,CONTROLLER://:9095
advertised.listeners=CLIENT://kafka-1.example.com:9093,REPLICATION://kafka-1.internal:9094
listener.security.protocol.map=CLIENT:SASL_SSL,REPLICATION:SSL,CONTROLLER:SSL
inter.broker.listener.name=REPLICATION
controller.listener.names=CONTROLLER
controller.quorum.bootstrap.servers=kafka-1.internal:9095,kafka-2.internal:9095,kafka-3.internal:9095   # older static form: controller.quorum.voters
listener.name.replication.ssl.client.auth=required
listener.name.controller.ssl.client.auth=required
ssl.keystore.location=/etc/kafka/tls/node.p12
ssl.truststore.location=/etc/kafka/tls/internal-ca.p12
ssl.principal.mapping.rules=RULE:^CN=(kafka-node),.*$/$1/,DEFAULT
super.users=User:kafka-node
```
- The **controller listener** must use its own listener name, never the inter-broker one. Brokers send requests to controllers, so a broker-only node must still define the controller listener and its security properties (for example `controller.listener.names=CONTROLLER` and `CONTROLLER:SASL_SSL` in the protocol map) even though it does not put it in `listeners`; a combined node includes it in `listeners`. The host and port in `controller.quorum.bootstrap.servers` must route to the controller listener.
- Node principals need `super.users` (or ClusterAction on the Cluster resource) for replication and controller operations; otherwise those requests fail authorization.
- Consider an internal CA separate from the client-facing one, with automated rotation.
- Isolate the internal listeners at the network level: clients never use the controller listener, so do not expose those ports to client subnets.

## Migrating a running cluster from PLAINTEXT
Kafka documents this as phased incremental bounces; stop each broker cleanly with SIGTERM and wait for restarted replicas to rejoin the ISR before the next node. A PLAINTEXT port must stay open until the last bounce.
1. Open the secured port alongside the existing one (rolling restart), then move clients to it.
2. Set `inter.broker.listener.name` (or `security.inter.broker.protocol`, default PLAINTEXT) to the secure listener (rolling restart).
3. Close the PLAINTEXT port (rolling restart).
4. Controllers accept requests on every listener in `controller.listener.names`, and the first listed is used for outbound requests, so move to a new controller listener with one roll that adds it and a second that removes the old one. Test in staging.

## Verify
- [ ] A TLS connection to the controller listener without a client certificate fails the handshake.
- [ ] A port scan from a client subnet cannot reach the internal ports.
- [ ] Under-replicated partitions stay 0 through each rolling step.

## Checked

2026-10-25, against Apache Kafka trunk documentation (apache/kafka docs/, commit date 2026-10-24). Confirmed: listener, `listener.security.protocol.map`, `inter.broker.listener.name`, `security.inter.broker.protocol` (default PLAINTEXT) and `controller.listener.names` semantics, the broker-only and combined KRaft examples, the rule that the controller listener cannot equal the inter-broker listener, `controller.quorum.bootstrap.servers` replacing `controller.quorum.voters`, the incremental-bounce procedure, and `super.users` plus ClusterAction. Removed: the `sasl.mechanism.controller.protocol` mention, the 3.9 version gate and dynamic-quorum voter advice (not in the documentation read), and the "rogue node" rationale.

Method: documentation only; no commands were run.
