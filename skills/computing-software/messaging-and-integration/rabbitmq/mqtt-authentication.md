---
id: computing-software.messaging-and-integration.rabbitmq.mqtt-authentication
name: mqtt-authentication
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, mqtt-authentication]
level: practitioner
status: docs-checked
description: "Authenticate MQTT clients with RabbitMQ users, per-vhost mapping and TLS client certificates."
sources:
  - https://www.rabbitmq.com/docs/mqtt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MQTT authentication

**Goal:** Lock down device access.

## Steps
1. Choose the vhost via a port mapping (`mqtt_port_to_vhost_mapping` global parameter), a `vhost:user` username, or the `mqtt.vhost` default; the username form takes precedence over the port mapping.
2. Disable anonymous access: `mqtt.allow_anonymous = false` (and `anonymous_login_user = none`).
3. Set permissions so clients can only subscribe to their own session queues; topic permissions alone are not enough.
4. For certificate identity set `mqtt.ssl_cert_login = true` (and `ssl_cert_login_from = common_name` if needed), with TLS `verify_peer` and `fail_if_no_peer_cert = true`.

## Failure modes
- Anonymous connections use default credentials; the guide strongly discourages them.
- Usernames cannot contain a colon.

## Verify
- Connect with a bad password and expect refusal.

## Checked

Date: 2026-11-02. Confirmed on the MQTT guide (vhost mapping, anonymous connections, TLS certificate authentication, permissions note). Removed: the log-based verification.

Method: documentation only; no commands were run.
