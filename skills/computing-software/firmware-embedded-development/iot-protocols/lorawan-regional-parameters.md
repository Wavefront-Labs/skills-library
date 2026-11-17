---
id: computing-software.firmware-embedded-development.iot-protocols.lorawan-regional-parameters
name: lorawan-regional-parameters
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [lorawan-regional-parameters, lorawan-regional, lorawan, eu868, us915, data-rate, iot-protocols]
level: practitioner
status: draft
description: "LoRaWAN regional parameters: Configure the right channel plan and data rates per region."
sources:
  - https://lora-alliance.org/resource_hub/rp2-1-0-4-regional-parameters/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LoRaWAN regional parameters

**Goal:** Configure the right channel plan and data rates per region.

## Steps
1. EU868 default channels 868.1, 868.3, 868.5 MHz; RX2 869.525 MHz at DR0 (SF12/125 kHz)
2. US915 uses 64 x 125 kHz uplink channels (902.3 + 0.2n) plus 8 x 500 kHz; gateways usually listen on 8-channel sub-bands
3. AU915, AS923, IN865, KR920 differ in plans
4. DR0-DR5 map to SF12-SF7 at 125 kHz in EU868; DR6 SF7/250 kHz
5. Max payload size depends on DR and region (confirm table in the RP2 document for your version)
6. Use the matching LoRaWAN regional parameters revision (RP002-1.0.x)

## Gotcha
A US915 device configured for the wrong sub-band joins nothing; align device and gateway sub-band (e.g. channels 8-15).

## Verify
- [ ] Join accepted on right channel plan
- [ ] Payload limit respected at lowest DR
- [ ] Regional parameter revision matches network server
