---
id: computing-software.firmware-embedded-development.iot-protocols.lwm2m-device-management
name: lwm2m-device-management
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [lwm2m-device-management, lwm2m-operations, lwm2m, read, write, observe, notify, iot-protocols]
level: practitioner
status: draft
description: "LwM2M read write execute and observe: Manage a fleet using LwM2M interfaces."
sources:
  - https://www.openmobilealliance.org/lwm2m/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LwM2M read write execute and observe

**Goal:** Manage a fleet using LwM2M interfaces.

## Steps
1. Device Management interface: Read (GET), Write (PUT/POST), Execute (POST), Create, Delete, Write-Attributes
2. Information Reporting: Observe (CoAP Observe) with attributes pmin, pmax, gt, lt, st to throttle notifications
3. Notify rates should respect pmin to avoid chatter
4. Composite operations (v1.1) read many paths in one request
5. Send operation (1.1) lets the client push data
6. Anjay, Wakaama and Leshan are common client and server stacks

## Gotcha
Setting pmin 0 and no pmax on a noisy sensor floods a cellular link.

## Verify
- [ ] Observe sends only when threshold crossed
- [ ] Composite read returns all paths
