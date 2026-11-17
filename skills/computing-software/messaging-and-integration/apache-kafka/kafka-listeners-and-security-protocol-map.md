---
id: computing-software.messaging-and-integration.apache-kafka.kafka-listeners-and-security-protocol-map
name: kafka-listeners-and-security-protocol-map
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, listeners, listener-security-protocol-map, inter-broker-listener-name, controller-listener-names]
level: practitioner
status: docs-checked
description: "Configure listeners, listener.security.protocol.map, inter.broker.listener.name and the KRaft controller listener."
sources:
  - https://kafka.apache.org/42/security/listener-configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: define each port a Kafka server accepts connections on and its security protocol.

`listeners` is a comma-separated list of `{LISTENER_NAME}://{hostname}:{port}`; at least one is required per server. Protocols are mapped separately: `listener.security.protocol.map=CLIENT:SSL,BROKER:PLAINTEXT`. Valid protocols (case-insensitive): PLAINTEXT, SSL, SASL_PLAINTEXT, SASL_SSL. If each listener uses a different protocol you may name listeners by protocol (`listeners=SSL://localhost:9092,PLAINTEXT://localhost:9093`), but explicit names are recommended.

Inter-broker traffic (mainly replication) uses `inter.broker.listener.name`; if unset it follows `security.inter.broker.protocol`, default PLAINTEXT.

KRaft: controllers must use a separate listener named in `controller.listener.names`, which cannot equal the inter-broker listener. Even a broker-only node must define the controller listener and its security properties, though it is not added to `listeners`:
```
process.roles=broker
listeners=BROKER://localhost:9092
inter.broker.listener.name=BROKER
controller.quorum.bootstrap.servers=localhost:9093
controller.listener.names=CONTROLLER
listener.security.protocol.map=BROKER:SASL_SSL,CONTROLLER:SASL_SSL
```
For `process.roles=broker,controller` add CONTROLLER to `listeners`. The host and port in `controller.quorum.bootstrap.servers` must route to the exposed controller listener. With multiple controller listeners, the first is used for outbound requests; this allows migrating listeners over two rolls.

## Checked

Method: 2026-11-08 docs-only read of the cited Kafka 4.2 listener-configuration page. All claims matched; no content changes. No hands-on run.
