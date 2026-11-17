---
id: computing-software.firmware-embedded-development.iot-protocols.lorawan-keys-and-mic
name: lorawan-keys-and-mic
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [lorawan-keys-and-mic, lorawan-security, lorawan, nwkskey, appskey, mic, iot-protocols]
level: practitioner
status: draft
description: "LoRaWAN keys and MIC: Understand which key protects what."
sources:
  - https://lora-alliance.org/resource_hub/lorawan-specification-v1-0-4/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LoRaWAN keys and MIC

**Goal:** Understand which key protects what.

## Steps
1. NwkSKey computes the 4-byte MIC (AES-CMAC) and encrypts MAC commands
2. AppSKey encrypts application payload (AES-128 CTR style) end to end to the application server
3. The network server cannot read application data when keys are split
4. AppKey is root key, never sent over the air
5. Use secure element or per-device unique keys; avoid fleet-wide keys
6. In 1.1 a separate NwkKey and AppKey exist, with JoinServer holding roots

## Gotcha
Keys flashed in plain firmware can be extracted from the chip; protect with readout protection or a secure element.

## Verify
- [ ] MIC verified by server
- [ ] Payload opaque to network server
- [ ] Unique keys per device
