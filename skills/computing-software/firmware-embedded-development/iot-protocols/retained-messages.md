---
id: computing-software.firmware-embedded-development.iot-protocols.retained-messages
name: retained-messages
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [retained-messages, mqtt-qos-reliability, mqtt, retain, retained, iot-protocols]
level: practitioner
status: docs-checked
description: "MQTT retained messages: Use retained messages for last-known state."
sources:
  - https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html
  - https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MQTT retained messages

**Goal:** Use retained messages for last-known state.

## Steps
1. Publish with RETAIN=1; the broker stores one message per topic and sends it on new matching subscriptions
2. Clear it by publishing a zero-length payload with retain
3. Messages delivered to existing subscribers have RETAIN=0 in 3.1.1
4. v5 Retain Handling subscribe option: 0 send, 1 send only for new subscription, 2 never

## Gotcha
Retaining high-rate telemetry makes every new subscriber receive stale data; retain only status/config topics and prune dead devices.

## Verify
- [ ] New subscriber instantly receives state
- [ ] Zero-byte publish deletes it
- [ ] Broker restart behaviour matches your broker's persistence setting

## Checked

2026-11-03. Confirmed in the OASIS MQTT 3.1.1 and 5.0 specifications: last retained message per topic, zero-byte retained publish removes it, RETAIN=0 for established subscriptions, v5 Retain Handling 0/1/2. Removed: the Mosquitto persistence claim (page not read).
Method: documentation only; no commands were run.
