---
id: computing-software.firmware-embedded-development.iot-protocols.zigbee-network-formation
name: zigbee-network-formation
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [zigbee-network-formation, zigbee-stack, zigbee, coordinator, pan-id, permit-join, iot-protocols]
level: practitioner
status: draft
description: "Zigbee network formation and joining: Form a Zigbee 3.0 network and add devices."
sources:
  - https://csa-iot.org/all-solutions/zigbee/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Zigbee network formation and joining

**Goal:** Form a Zigbee 3.0 network and add devices.

## Steps
1. Roles: Coordinator (forms network, Trust Center), Router, End Device
2. Coordinator scans channels 11-26 (2.4 GHz) and picks a low-energy one; channels 15, 20, 25 avoid most Wi-Fi 1/6/11 overlap
3. Chooses PAN ID (16-bit) and Extended PAN ID (64-bit)
4. Enable joining with permit-join for 60-254 s
5. Device does beacon request, association, receives a 16-bit network address
6. Routers use AODV mesh routing; end devices poll their parent
7. Zigbee 3.0 uses install codes or the well-known link key for joining

## Gotcha
Zigbee on channel 11 beside busy Wi-Fi gives poor range; and permit-join left open permanently allows unwanted joins.

## Verify
- [ ] Device joins and gets short address
- [ ] Route discovery works across two hops
- [ ] Permit-join closed after the timer
