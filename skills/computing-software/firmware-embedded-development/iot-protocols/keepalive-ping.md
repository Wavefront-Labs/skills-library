---
id: computing-software.firmware-embedded-development.iot-protocols.keepalive-ping
name: keepalive-ping
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [keepalive-ping, mqtt-packets, mqtt, keepalive, pingreq, iot-protocols]
level: practitioner
status: docs-checked
description: "MQTT keep alive and PINGREQ: Set a keep alive and understand PINGREQ, the 1.5x broker timeout and v5 Server Keep Alive."
sources:
  - https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html
  - https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MQTT keep alive and PINGREQ

**Goal:** Set a keep alive and understand PINGREQ, the 1.5x broker timeout and v5 Server Keep Alive.

## Steps
1. Client sends PINGREQ if no packet was sent within keep alive; broker replies PINGRESP
2. Broker closes the connection after 1.5 x keep alive of silence
3. Keep alive 0 disables the mechanism
4. The spec gives no recommended value; choose the interval from your network's idle timeout and your power budget
5. v5 broker may override with Server Keep Alive in CONNACK

## Gotcha
A long keep alive saves power but a dead connection stays undetected longer; the broker only closes it after 1.5 x keep alive of silence.

## Verify
- [ ] Packet capture shows ping at the interval
- [ ] Unplugging the network closes the connection on the broker at 1.5 x
- [ ] v5 Server Keep Alive honoured

## Checked

2026-11-03. Confirmed in the OASIS MQTT 3.1.1 and 5.0 specifications: PINGREQ rule, PINGRESP, one-and-a-half-times disconnect, keep alive 0 disables, v5 Server Keep Alive in CONNACK. Removed: the cellular NAT 30-120 s figure and the 60 s suggestion (not in the specification).
Method: documentation only; no commands were run.
