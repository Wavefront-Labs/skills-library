---
id: computing-software.messaging-and-integration.mosquitto.bridge-protocol-and-session
name: bridge-protocol-and-session
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [bridge-protocol-version, cleansession, session-expiry, try-private]
level: advanced
status: docs-checked
description: "Tune a bridge session with bridge_protocol_version, cleansession, local_cleansession, v5 session expiry and try_private."
sources:
  - https://mosquitto.org/man/mosquitto-conf-5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: set bridge protocol version and session persistence.

- `bridge_protocol_version mqttv50|mqttv311|mqttv31`, default `mqttv311`.
- `cleansession true|false`: default false keeps all subscriptions on the remote broker if the connection drops. True cleans up subscriptions and messages on drop, and may cause a large amount of retained messages to be sent at every reconnect.
- `local_cleansession` splits the local side from the remote; defaults to the value of cleansession.
- `bridge_session_expiry_interval` (MQTT v5): 0 (default) expires at once when the connection drops, 0xFFFFFFFF means infinite, otherwise seconds.
- `bridge_receive_maximum` (v5): limits in-flight QoS 1/2 messages; 1-65535; defaults to `max_inflight_messages` (20).
- `try_private true` (default) tries to tell the remote broker this is a bridge, so loop detection is better and retained messages propagate; set false if the bridge will not connect to a broker lacking support.
- `bridge_outgoing_retain false` strips the retain bit on outgoing messages for v3.1.1/v3.1 brokers without retained support; default true.

Gotcha: with `cleansession false`, changing the subscribed topics can cause unexpected incoming topics because the remote broker keeps the old subscription. Connect once with `cleansession true`, then reconnect with false.

## Checked

2026-11-03. Claims, option names, defaults and version notes were compared with the Mosquitto manual pages in `sources` (mosquitto(8), mosquitto.conf(5), mosquitto_pub, mosquitto_sub, mosquitto_rr, mosquitto_ctrl, and the Dynamic Security page where relevant). Nothing removed.

Method: documentation only; no commands were run.
