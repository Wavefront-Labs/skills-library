---
id: computing-software.firmware-embedded-development.iot-protocols.matter-commissioning-flow
name: matter-commissioning-flow
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [matter-commissioning-flow, matter-commissioning, matter, commissioning, pase, case, commissionable, iot-protocols]
level: practitioner
status: draft
description: "Matter commissioning flow: Walk the steps of commissioning a device."
sources:
  - https://csa-iot.org/developer-resource/specifications-download-request/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Matter commissioning flow

**Goal:** Walk the steps of commissioning a device.

## Steps
1. Device advertises (BLE for Wi-Fi/Thread devices, or DNS-SD _matterc._udp when already on network)
2. Commissioner scans the QR or manual code to get the passcode and discriminator
3. PASE session via SPAKE2+
4. Commissioner reads attestation, validates Device Attestation Certificate chain against the CSA PAA/DAC roots
5. Sets regulatory config, Wi-Fi or Thread credentials via Network Commissioning
6. Device joins the network; commissioner finds it by operational DNS-SD
7. CASE session; AddNOC installs certificate; CommissioningComplete

## Gotcha
The commissioning window is time-limited (a few minutes, confirm the limits in the spec) and then closes; reopen via Administrator Commissioning cluster.

## Verify
- [ ] chip-tool pairing code <node> <code> completes
- [ ] Device visible via _matter._tcp
- [ ] Attestation passed or test PAA used in dev
