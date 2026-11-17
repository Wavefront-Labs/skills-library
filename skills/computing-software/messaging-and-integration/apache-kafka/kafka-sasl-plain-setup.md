---
id: computing-software.messaging-and-integration.apache-kafka.kafka-sasl-plain-setup
name: kafka-sasl-plain-setup
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, sasl-plain, plain-login-module, jaas-config, user-credentials]
level: practitioner
status: docs-checked
description: "Configure SASL/PLAIN with PlainLoginModule users in the broker JAAS file and client sasl.jaas.config, and use it only over TLS."
sources:
  - https://kafka.apache.org/42/security/authentication-using-sasl/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: simple username/password authentication.

Broker JAAS (`KafkaServer` section):
```
org.apache.kafka.common.security.plain.PlainLoginModule required
    username="admin"
    password="admin-secret"
    user_admin="admin-secret"
    user_alice="alice-secret";
```
`username`/`password` are what the broker uses to connect to other brokers (admin is the inter-broker user). The `user_<name>` properties define every acceptable client password, including inter-broker connections. Pass the file with `-Djava.security.auth.login.config=/path/to/kafka_server_jaas.conf`.

server.properties:
```
listeners=SASL_SSL://host.name:port
security.inter.broker.protocol=SASL_SSL
sasl.mechanism.inter.broker.protocol=PLAIN
sasl.enabled.mechanisms=PLAIN
```
Client:
```
sasl.jaas.config=org.apache.kafka.common.security.plain.PlainLoginModule required username="alice" password="alice-secret";
security.protocol=SASL_SSL
sasl.mechanism=PLAIN
```
With the default principal.builder.class, the username is the principal used for ACLs.

Production: use PLAIN only with SSL as the transport so clear passwords are never sent unencrypted. To avoid clear passwords on disk (2.0 onwards) provide your own callback handlers via `sasl.server.callback.handler.class` and `sasl.client.callback.handler.class`, which can also verify passwords against an external server.

## Checked

Method: docs-checked 2026-11-09 against the kafka.apache.org 4.2 Authentication using SASL page (JAAS configuration and SASL/PLAIN sections). An unsupported closing paragraph on restarts was removed.
