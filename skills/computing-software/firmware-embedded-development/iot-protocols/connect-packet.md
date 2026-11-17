---
id: computing-software.firmware-embedded-development.iot-protocols.connect-packet
name: connect-packet
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [connect-packet, mqtt-packets, mqtt, connect, clientid, iot-protocols]
level: practitioner
status: docs-checked
description: "MQTT CONNECT packet: Build and read an MQTT CONNECT/CONNACK exchange correctly for 3.1.1 and 5."
sources:
  - https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html
  - https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MQTT CONNECT packet

**Goal:** Build and read an MQTT CONNECT/CONNACK exchange correctly for 3.1.1 and 5.

## Steps
1. Variable header is protocol name "MQTT", level (4 = 3.1.1, 5 = v5), connect flags, keep alive (seconds)
2. Flags byte bits: username 7, password 6, will retain 5, will QoS 4-3, will flag 2, clean start 1
3. Payload order: ClientId, will topic/message, username, password
4. A server may accept a zero-byte ClientId and assign one. In 3.1.1 the client must then set CleanSession=1 (otherwise CONNACK 0x02 Identifier rejected); in v5 the server returns the Assigned Client Identifier in CONNACK
5. CONNACK carries session-present bit and return/reason code (3.1.1 code 5 = not authorised; v5 0x87)

## Gotcha
A server must disconnect an existing client when a new connection uses the same ClientId, so two devices sharing an id keep displacing each other; make ids unique per device, e.g. from the hardware serial.

## Verify
- [ ] A packet capture or client debug log shows the expected CONNECT flags
- [ ] CONNACK code 0
- [ ] second client with same id disconnects the first

## Checked

2026-11-03. Confirmed in the OASIS MQTT 3.1.1 and 5.0 specifications: protocol level 4 and 5, connect flag bit positions, payload order, zero-byte ClientId rules, Assigned Client Identifier, CONNACK return code 5 (3.1.1), reason code 0x87 (v5), and disconnect of an existing client with the same ClientId. Removed: the mosquitto_sub -d check and the v5 clean-start requirement for an empty ClientId (3.1.1 only).
Method: documentation only; no commands were run.
