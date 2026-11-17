---
id: computing-software.firmware-embedded-development.iot-protocols.connectedhomeip-sdk
name: connectedhomeip-sdk
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [connectedhomeip-sdk, matter-development, matter, connectedhomeip, chip-tool, zap, iot-protocols]
level: practitioner
status: draft
description: "connectedhomeip SDK: Build and run Matter examples."
sources:
  - https://github.com/project-chip/connectedhomeip
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# connectedhomeip SDK

**Goal:** Build and run Matter examples.

## Steps
1. Clone project-chip/connectedhomeip and run source scripts/bootstrap.sh and source scripts/activate.sh
2. Build host example: scripts/examples/gn_build_example.sh examples/lighting-app/linux out/light
3. Build controller: examples/chip-tool
4. Edit clusters with ZAP (zap-cli) which generates the .zap file and code
5. Platform ports: ESP-IDF esp-matter, nRF Connect, Silicon Labs, Telink
6. Run with --wifi or on-network, and chip-tool pairing onnetwork 1 20202021 for default dev passcode

## Gotcha
Developers often use the test PAA and DAC; production devices need real attestation certificates and CSA certification.

## Verify
- [ ] lighting-app starts and advertises
- [ ] chip-tool onoff toggle works
- [ ] ZAP regenerates without errors
