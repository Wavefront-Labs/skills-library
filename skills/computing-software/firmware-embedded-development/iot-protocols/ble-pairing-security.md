---
id: computing-software.firmware-embedded-development.iot-protocols.ble-pairing-security
name: ble-pairing-security
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [ble-pairing-security, ble-iot, ble, pairing, le-secure-connections, numeric-comparison, iot-protocols]
level: practitioner
status: draft
description: "BLE pairing and security modes: Choose BLE pairing that resists eavesdropping and MITM."
sources:
  - https://www.bluetooth.com/specifications/specs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# BLE pairing and security modes

**Goal:** Choose BLE pairing that resists eavesdropping and MITM.

## Steps
1. LE Secure Connections (ECDH P-256, Bluetooth 4.2+) is the baseline; legacy pairing is weaker
2. Association models: Just Works (no MITM protection), Numeric Comparison, Passkey Entry, Out of Band (NFC or QR)
3. Set IO capabilities accordingly and require bonding for stored keys
4. Security Mode 1 Level 4 means authenticated LE Secure Connections with 128-bit key
5. Use resolvable private addresses for privacy
6. Mark characteristics with permission flags (encrypt, authenticated)

## Gotcha
Just Works on an IoT device with no display gives encryption without MITM protection; use OOB QR with a printed code when possible.

## Verify
- [ ] Connection refuses unauthenticated access
- [ ] Bond persists across reboot
- [ ] Privacy address rotates
