---
id: computing-software.firmware-embedded-development.iot-protocols.last-will
name: last-will
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [last-will, mqtt-qos-reliability, mqtt, lwt, will, iot-protocols]
level: practitioner
status: docs-checked
description: "MQTT last will and testament: Publish an offline marker automatically when a device dies."
sources:
  - https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html
  - https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MQTT last will and testament

**Goal:** Publish an offline marker automatically when a device dies.

## Steps
1. Set will topic, payload, QoS and retain in CONNECT
2. Publish "online" retained on connect, and let the will be retained "offline" on the same topic
3. Will is sent on network failure, keep-alive timeout or protocol error, not on a clean DISCONNECT (v5 allows code 0x04 to send it anyway)
4. v5 Will Delay Interval waits before sending so brief reconnects do not flap

## Gotcha
Broker takes up to 1.5 x keep alive to notice death, so presence is not instant.

## Verify
- [ ] Kill -9 the client and see the offline message
- [ ] Clean disconnect sends no will
- [ ] Delay interval suppresses flapping

## Checked

2026-11-03. Confirmed in the OASIS MQTT 3.1.1 and 5.0 specifications: will fields in CONNECT, Will Retain, situations that publish the will, will discarded on DISCONNECT, v5 DISCONNECT reason 0x04 (Disconnect with Will Message), Will Delay Interval and the rule that a reconnect before it expires suppresses the will, and the 1.5 x keep alive detection time. Nothing removed.
Method: documentation only; no commands were run.
