---
id: computing-software.systems-network-administration.zigbee2mqtt.zigbee2mqtt-mqtt-connection-and-output
name: zigbee2mqtt-mqtt-connection-and-output
category: computing-software
field: systems-network-administration
product: zigbee2mqtt
tags: [zigbee2mqtt, mqtt, base-topic, tls, secret-yaml, cache-state, last-seen, retain, mqtt-v5]
level: practitioner
status: docs-checked
description: "Set up the Zigbee2MQTT mqtt section: server URL, credentials, TLS client certs, secret.yaml references, base topic, payload output format, cached state and last_seen."
sources: ["https://www.zigbee2mqtt.io/guide/configuration/mqtt.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Zigbee2MQTT MQTT connection and message behaviour

```yaml
mqtt:
    server: 'mqtt://localhost:1883'   # mqtts:// for TLS
    base_topic: zigbee2mqtt
    user: my_user
    password: my_password
    ca: '/etc/ssl/mqtt-ca.crt'        # optional TLS
    key: '/etc/ssl/mqtt-client.key'
    cert: '/etc/ssl/mqtt-client.crt'
    reject_unauthorized: true
    keepalive: 60
    version: 4
```

Notes from the reference:
- `client_id`, `server_name` (TLS SNI override when the certificate name differs from the host in `server`), `include_device_information`, and `maximum_packet_size` (default 1048576 bytes the broker may send) are optional.
- `version: 5` is needed for the per-device `retention` (MQTT message expiry) option.
- `force_disable_retain: true` is only for brokers that do not support retained messages (AWS IoT core, Azure IoT Hub and similar); it breaks the Home Assistant integration.
- `reject_unauthorized: false` disables TLS certificate validation; the securing page calls it dangerous in production.
- Home Assistant Mosquitto add-on hostname example: `core-mosquitto`.

Keep secrets out of the main file. Quote the reference:

```yaml
mqtt:
    server: '!secret.yaml server'
    user: '!secret.yaml user'
    password: '!secret.yaml password'
```
with a `secret.yaml` containing `server:`, `user:`, `password:`. The quotes are mandatory.

Behaviour under `advanced`: `cache_state` (default true; payloads contain all attributes, required for Home Assistant), `cache_state_persistent`, `cache_state_send_on_startup`, `last_seen` (disable, ISO_8601, ISO_8601_local, epoch), `elapsed` (ms since previous message), and `output`: `json` (default, one topic per device), `attribute` (one topic per attribute, e.g. `zigbee2mqtt/my_bulb/state` = `ON`) or `attribute_and_json`.

## Checked

2026-11-03. Confirmed against the MQTT configuration page: server, base_topic, TLS keys, reject_unauthorized, client_id, server_name, include_device_information, keepalive, version 4/5, force_disable_retain, maximum_packet_size 1048576, secret.yaml syntax, cache_state, last_seen values, elapsed, output values. Removed: the unverified mosquitto_sub verify line and the placement claim for secret.yaml; the reject_unauthorized warning now cites the securing page.
Method: documentation only; no commands were run.
