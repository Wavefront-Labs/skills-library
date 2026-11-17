---
id: computing-software.firmware-embedded-development.iot-protocols.modbus-to-mqtt-gateway
name: modbus-to-mqtt-gateway
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [modbus-to-mqtt-gateway, iot-gateway, modbus, mqtt-gateway, register-map, polling, iot-protocols]
level: practitioner
status: draft
description: "Modbus to MQTT gateway: Expose Modbus devices on MQTT."
sources:
  - https://modbus.org/specs.php
  - https://nodered.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Modbus to MQTT gateway

**Goal:** Expose Modbus devices on MQTT.

## Steps
1. Define a register map: slave ID, function code (03 holding, 04 input), address, count, type (int16, uint32 word order) and scale
2. Poll in groups to reduce requests; keep intervals above device minimum
3. Publish each tag to plant/line/device/tag as JSON with timestamp and quality
4. Subscribe to command topics and write coils or registers via function 05/06/16
5. Handle timeouts and exceptions (codes 01-04)
6. Read-only by default; whitelist writable registers

## Gotcha
Word order mismatch (big versus little endian words) returns plausible but wrong float values; test against a known reading.

## Verify
- [ ] Values match device display
- [ ] Timeout marks quality bad
- [ ] Writes only to whitelisted registers
