---
id: computing-software.firmware-embedded-development.iot-protocols.mqtt-sn
name: mqtt-sn
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [mqtt-sn, iot-low-power-links, gateway, topic-id, sleeping-client, iot-protocols]
level: practitioner
status: draft
description: "MQTT-SN for constrained networks: Use MQTT-SN over UDP or non-IP links."
sources:
  - https://www.oasis-open.org/committees/tc_home.php?wg_abbrev=mqtt
  - https://www.gsma.com/solutions-and-impact/technologies/internet-of-things/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MQTT-SN for constrained networks

**Goal:** Use MQTT-SN over UDP or non-IP links.

## Steps
1. MQTT-SN v1.2 uses a gateway (transparent or aggregating) between clients and a broker
2. Short packets: CONNECT, REGISTER (topic name to 2-byte topic ID), PUBLISH with topic ID, SUBSCRIBE
3. Predefined topic IDs and short topic names need no registration
4. Sleeping clients: DISCONNECT with duration, gateway buffers messages and delivers on wake PINGREQ
5. Gateway discovery via ADVERTISE and SEARCHGW
6. Common gateways are Eclipse Paho MQTT-SN gateway and Mosquitto-based bridges (confirm availability)

## Gotcha
Topic ID mappings are per-client; after reconnect a clean session needs re-registering.

## Verify
- [ ] Sleeping client receives buffered messages on wake
- [ ] Predefined ID publishes work
- [ ] Gateway translates to MQTT
