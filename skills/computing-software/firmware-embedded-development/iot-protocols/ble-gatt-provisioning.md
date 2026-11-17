---
id: computing-software.firmware-embedded-development.iot-protocols.ble-gatt-provisioning
name: ble-gatt-provisioning
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [ble-gatt-provisioning, ble-iot, ble, gatt, provisioning, characteristic, iot-protocols]
level: practitioner
status: draft
description: "BLE GATT provisioning service: Design a BLE provisioning flow for Wi-Fi credentials."
sources:
  - https://www.bluetooth.com/specifications/specs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# BLE GATT provisioning service

**Goal:** Design a BLE provisioning flow for Wi-Fi credentials.

## Steps
1. Advertise a service with 128-bit UUID and device name
2. Define a primary service with characteristics: write-only SSID/password (or one structured write), notify for status, read for device info
3. Use Write with response and a length-prefixed protocol across MTU (default 23, ATT payload 20 bytes; negotiate MTU up to 247)
4. Encrypt link with LE Secure Connections pairing, or encrypt the payload at app level
5. Time out and stop advertising after provisioning
6. Reject writes after success

## Gotcha
Writing plain credentials over an unencrypted, unpaired link exposes them to nearby sniffers.

## Verify
- [ ] App provisions Wi-Fi and device joins
- [ ] Advertising stops after success
- [ ] Large payload chunking works
