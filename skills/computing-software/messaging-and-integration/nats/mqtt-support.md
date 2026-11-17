---
id: computing-software.messaging-and-integration.nats.mqtt-support
name: mqtt-support
category: computing-software
field: messaging-and-integration
product: nats
tags: [mqtt, mqtt-config, qos1, ack-wait, max-ack-pending, allowed-connection-types]
level: practitioner
status: docs-checked
description: "Enable the MQTT listener in nats-server: mqtt block, server_name requirement, auth modes, ack_wait, max_ack_pending and .sub permissions."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/running-a-nats-service/configuration/mqtt/mqtt_config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let MQTT clients connect to nats-server and interoperate with NATS subjects.

Add an `mqtt` block, for example `mqtt { port: 1883 }` (or `listen`/`host`). It supports a `tls` map (`cert_file`, `key_file`, `ca_file`, `verify`, `timeout`, `verify_and_map`), `no_auth_user` (default user for credential-less clients; overrides the main value for MQTT; not compatible with operator mode), a local `authorization` block (`username`, `password`, `token`, `timeout`), `ack_wait` (QoS 1 redelivery as DUPLICATE if no PUBACK; default 30 seconds; applies to new subscriptions only) and `max_ack_pending` (QoS 1 messages in flight per subscription, range 0 to 65535; session total cannot exceed 65535, otherwise SUBACK returns 0x80; a subscription ending in `#` uses twice the value).

Requirements: MQTT needs a unique `server_name` in the top-level config, and QoS 1 uses JetStream, so JetStream must be enabled.

Auth: in operator (JWT) mode every user needs a JWT; MQTT clients cannot sign a nonce, so mark users as bearer: `nsc edit user --name U --account A --bearer`. In local mode restrict a user to MQTT with `allowed_connection_types: ["MQTT"]` (aliases `connection_types`, `clients`); values are `STANDARD`, `WEBSOCKET`, `LEAFNODE`, `MQTT`; omitted means all.

Gotcha: a QoS 1 subscription creates a JetStream durable with delivery subject `$MQTT.sub.<...>`, so users with permissions must be allowed to subscribe to `$MQTT.sub.>`.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
