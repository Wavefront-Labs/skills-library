---
id: computing-software.messaging-and-integration.apache-kafka.kafka-client-quotas
name: kafka-client-quotas
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, quotas, producer-byte-rate, consumer-byte-rate, request-percentage]
level: practitioner
status: docs-checked
description: "Set per-user and per-client-id quotas with kafka-configs.sh using producer_byte_rate, consumer_byte_rate and request_percentage."
sources:
  - https://kafka.apache.org/42/operations/basic-kafka-operations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: throttle clients per (user, client-id), user, or client-id. By default clients get an unlimited quota.

Quota keys: `producer_byte_rate`, `consumer_byte_rate`, `request_percentage`.

Set for user1 and client clientA:
`bin/kafka-configs.sh --bootstrap-server localhost:9092 --alter --add-config 'producer_byte_rate=1024,consumer_byte_rate=2048,request_percentage=200' --entity-type users --entity-name user1 --entity-type clients --entity-name clientA`

Other levels use the same --add-config with:
- user only: `--entity-type users --entity-name user1`
- client only: `--entity-type clients --entity-name clientA`

Defaults use `--entity-default` instead of `--entity-name`, for example `--entity-type users --entity-default`, or `--entity-type users --entity-name user1 --entity-type clients --entity-default` for a default client-id under user1.

Describe with `--describe` and the same entity flags. Omitting the entity name describes all entities of that type, for example `--describe --entity-type users`.

## Checked

2026-11-04: claims, commands, flags and config names confirmed against the Kafka 4.2 Basic Kafka operations page (Quotas section). Removed: closing paragraph on precedence and describe-to-confirm (not stated there; precedence is on the Design page).

Method: documentation only; no commands were run.
