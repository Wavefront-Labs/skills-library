---
id: computing-software.firmware-embedded-development.iot-protocols.ttn-the-things-stack
name: ttn-the-things-stack
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [ttn-the-things-stack, lorawan-network-servers, ttn, the-things-stack, application-server, webhook, iot-protocols]
level: practitioner
status: draft
description: "The Things Stack (TTN): Register a gateway and device on The Things Stack community network."
sources:
  - https://www.thethingsindustries.com/docs/
  - https://www.chirpstack.io/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# The Things Stack (TTN)

**Goal:** Register a gateway and device on The Things Stack community network.

## Steps
1. Create application and register end device with frequency plan, LoRaWAN version and the DevEUI, JoinEUI, AppKey
2. Gateway connects over Basic Station, or the legacy Semtech UDP packet forwarder at the regional cluster address
3. Receive data via MQTT (application ID@tenant username with API key), webhooks or storage integration
4. Payload formatter runs JavaScript on the server
5. Fair use policy applies on community network
6. Pick the cluster (eu1, nam1, au1)

## Gotcha
Wrong frequency plan on the device registration leads to joins silently ignored.

## Verify
- [ ] Live data shows join
- [ ] Webhook receives uplink JSON
- [ ] Formatter output present
