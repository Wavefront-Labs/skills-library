---
id: computing-software.firmware-embedded-development.iot-protocols.topic-design
name: topic-design
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [topic-design, mqtt-topics, mqtt, topic-tree, namespace, iot-protocols]
level: practitioner
status: docs-checked
description: "MQTT topic design: Design a topic tree that scales and is securable."
sources:
  - https://www.hivemq.com/blog/mqtt-essentials-part-5-mqtt-topics-best-practices/
  - https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MQTT topic design

**Goal:** Design a topic tree that scales and is securable.

## Steps
1. Order levels general to specific: org/site/device-type/device-id/signal
2. Put the client id or another unique device id in its own level so broker authorization can limit each client to its own topics (the HiveMQ example: client1 may publish to client1/status but not client2/status)
3. Avoid spaces, non-ASCII characters and a leading slash (a leading slash adds an empty first level)
4. Use specific topics per data stream, e.g. myhome/livingroom/temperature rather than one myhome/livingroom topic; this also lets retained messages work per stream
5. Keep topics short, since the topic is sent in every message
6. Leave room to grow so new devices and signals fit without restructuring; include version information where appropriate

## Gotcha
Subscribing to # to collect everything overwhelms most clients; HiveMQ recommends a broker extension for persisting all messages.

## Verify
- [ ] One ACL line covers all devices
- [ ] Fleet-wide subscribe is one filter
- [ ] Topic count bounded

## Checked

2026-11-03. Confirmed in the HiveMQ MQTT Essentials part 5 article and the OASIS MQTT 3.1.1 specification: general-to-specific levels, unique id or client id in the topic for authorization, no spaces or non-ASCII, no leading slash, short topics, specific topics, room for growth, avoid subscribing to #. Removed: Mosquitto %c/%u patterns, the up/down direction split, the payload-in-topic rule and the timestamp memory-growth claim (not in the sources).
Method: documentation only; no commands were run.
