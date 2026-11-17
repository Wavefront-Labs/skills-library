---
id: computing-software.firmware-embedded-development.iot-protocols.matter-device-types
name: matter-device-types
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [matter-device-types, matter-development, matter, device-type, bridge, aggregator, iot-protocols]
level: practitioner
status: draft
description: "Matter device types: Pick the right device type and compose endpoints."
sources:
  - https://csa-iot.org/developer-resource/specifications-download-request/
  - https://github.com/project-chip/connectedhomeip
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Matter device types

**Goal:** Pick the right device type and compose endpoints.

## Steps
1. Device Type Library defines required clusters: On/Off Light 0x0100, Dimmable Light 0x0101, Door Lock 0x000A, Thermostat 0x0301, Temperature Sensor 0x0302, Contact Sensor 0x0015
2. Root Node 0x0016 on endpoint 0
3. Bridge uses Aggregator device type 0x000E with Bridged Node endpoints and Bridged Device Basic Information cluster
4. Composed devices use parts lists
5. Newer types (robot vacuum, energy) arrive in later spec releases (confirm version)

## Gotcha
Missing a mandatory cluster fails certification tests even if the device works with one app.

## Verify
- [ ] Required clusters present
- [ ] Bridge shows bridged devices
- [ ] Certification test plan passes
