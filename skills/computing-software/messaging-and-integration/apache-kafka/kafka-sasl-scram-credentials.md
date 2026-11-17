---
id: computing-software.messaging-and-integration.apache-kafka.kafka-sasl-scram-credentials
name: kafka-sasl-scram-credentials
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, sasl-scram, scram-sha-256, add-scram, scram-sha-512]
level: practitioner
status: docs-checked
description: "Create and manage SCRAM credentials stored in the KRaft metadata log with kafka-storage.sh --add-scram and kafka-configs.sh."
sources:
  - https://kafka.apache.org/42/security/authentication-using-sasl/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: use SASL/SCRAM-SHA-256 or SCRAM-SHA-512 (RFC 5802) with credentials kept in the metadata log.

Inter-broker credentials must exist before brokers start, so format storage with them:
`bin/kafka-storage.sh format -t $(bin/kafka-storage.sh random-uuid) -c config/server.properties --add-scram 'SCRAM-SHA-256=[name="admin",password="admin-secret"]'`

Create or update client credentials dynamically (new connections use the update):
`bin/kafka-configs.sh --bootstrap-server localhost:9092 --alter --add-config 'SCRAM-SHA-256=[iterations=8192,password=alice-secret]' --entity-type users --entity-name alice --command-config client.properties`
List with `--describe`, delete with `--alter --delete-config 'SCRAM-SHA-256'`. The default iteration count is 4096 and a random salt is used if not given.

Broker JAAS: `org.apache.kafka.common.security.scram.ScramLoginModule required username="admin" password="admin-secret";` plus `sasl.mechanism.inter.broker.protocol=SCRAM-SHA-256` and `sasl.enabled.mechanisms=SCRAM-SHA-256` (or SHA-512). Client: `ScramLoginModule` in `sasl.jaas.config`, `security.protocol=SASL_SSL`, `sasl.mechanism=SCRAM-SHA-256`.

Security notes: storing credentials in the metadata log suits installations where KRaft controllers are secure and on a private network. Only SHA-256 and SHA-512 with minimum 4096 iterations are supported. Use SCRAM only with TLS. Override the store with `sasl.server.callback.handler.class` if controllers are not secure.

## Checked

2026-11-04: claims, commands, flags and config names confirmed against the Kafka 4.2 Authentication using SASL page (SCRAM section). Removed: closing paragraph about restarts and client.properties (not on the page).

Method: documentation only; no commands were run.
