---
id: computing-software.firmware-embedded-development.iot-protocols.matter-onboarding-payload
name: matter-onboarding-payload
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [matter-onboarding-payload, matter-commissioning, matter, qr-code, manual-pairing-code, discriminator, iot-protocols]
level: practitioner
status: draft
description: "Matter onboarding payload and QR code: Generate valid onboarding codes."
sources:
  - https://csa-iot.org/developer-resource/specifications-download-request/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Matter onboarding payload and QR code

**Goal:** Generate valid onboarding codes.

## Steps
1. QR payload starts with "MT:" followed by Base38 text
2. Fields: version (3 bits), vendor ID (16), product ID (16), commissioning flow (2), discovery capabilities (8: BLE, on-network, soft AP), discriminator (12), passcode (27)
3. Manual code is 11 or 21 digits with a check digit
4. Invalid passcodes: 00000000, 11111111, 22222222 etc. and 12345678 or 87654321
5. Passcode 8 digits, derived with SPAKE2+ verifier stored on device
6. Tools: chip-tool payload generate-qrcode (confirm exact syntax in current SDK)

## Gotcha
Printing the same passcode on every unit means anyone with one label can commission all; generate unique passcodes and salts per device.

## Verify
- [ ] Parse the QR with the SDK payload tool
- [ ] Round-trip manual code
- [ ] Unique per unit
