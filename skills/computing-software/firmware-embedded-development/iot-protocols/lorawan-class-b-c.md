---
id: computing-software.firmware-embedded-development.iot-protocols.lorawan-class-b-c
name: lorawan-class-b-c
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [lorawan-class-b-c, lorawan-classes, lorawan, class-b, class-c, ping-slot, iot-protocols]
level: practitioner
status: draft
description: "LoRaWAN Class B and C: Choose the class by latency versus power."
sources:
  - https://lora-alliance.org/resource_hub/lorawan-specification-v1-0-4/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LoRaWAN Class B and C

**Goal:** Choose the class by latency versus power.

## Steps
1. Class B: gateways broadcast beacons every 128 s; device opens ping slots at negotiated periodicity (PingSlotInfoReq, 2^n up to 128 s)
2. Beacon loss moves it back to Class A
3. Class C: receive window open continuously except when transmitting, using RX2 parameters
4. Class C is mains-powered, with fast downlink
5. Class switching is by DeviceModeInd in 1.0.x/1.1 (confirm in your server)

## Gotcha
Class C on battery empties it in days; Class B demands GPS-synced gateways with beacons.

## Verify
- [ ] Ping slot downlink latency measured
- [ ] Class C receives right after TX
- [ ] Fallback to A on beacon loss
