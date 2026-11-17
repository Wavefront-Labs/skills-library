---
id: computing-software.firmware-embedded-development.iot-protocols.qos-flows
name: qos-flows
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [qos-flows, mqtt-qos-reliability, mqtt, qos, puback, pubrec, iot-protocols]
level: practitioner
status: docs-checked
description: "MQTT QoS 0, 1, 2 flows: Choose the right QoS and know the exact handshake."
sources:
  - https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MQTT QoS 0, 1, 2 flows

**Goal:** Choose the right QoS and know the exact handshake.

## Steps
1. QoS 0: fire and forget, no ack
2. QoS 1: PUBLISH then PUBACK; sender retries with DUP set until acked, so duplicates are possible (at least once)
3. QoS 2: PUBLISH, PUBREC, PUBREL, PUBCOMP; receiver stores the id until PUBREL so it delivers once
4. Effective QoS is min(publisher QoS, subscription QoS)
5. In 3.1.1 re-sending is required only when a client reconnects with CleanSession=0: unacknowledged PUBLISH (QoS above 0) and PUBREL packets are re-sent with their original packet identifiers

## Gotcha
QoS 2 costs four packets and state on both sides; most telemetry should use QoS 1 with idempotent handlers keyed on a message id.

## Verify
- [ ] Duplicate delivery handled without double effect
- [ ] Downgrade by subscriber QoS observed
- [ ] Inflight window limit configured

## Checked

2026-11-03. Confirmed in the OASIS MQTT 3.1.1 specification: QoS 0/1/2 handshakes, DUP on redelivery, receiver holding the identifier until PUBREL, minimum of published and granted QoS, and redelivery only on reconnect with CleanSession=0. Reworded step 5 to the exact rule.
Method: documentation only; no commands were run.
