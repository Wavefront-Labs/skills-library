---
id: computing-software.firmware-embedded-development.iot-protocols.lorawan-otaa-join
name: lorawan-otaa-join
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [lorawan-otaa-join, lorawan-activation, lorawan, otaa, join-request, devnonce, iot-protocols]
level: practitioner
status: draft
description: "LoRaWAN OTAA join: Join a network securely with over-the-air activation."
sources:
  - https://lora-alliance.org/resource_hub/lorawan-specification-v1-0-4/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LoRaWAN OTAA join

**Goal:** Join a network securely with over-the-air activation.

## Steps
1. Device holds DevEUI, JoinEUI (AppEUI in 1.0.x) and AppKey
2. Join-Request: JoinEUI, DevEUI, DevNonce (2 bytes) with MIC
3. Join-Accept (encrypted with AppKey) carries JoinNonce, NetID, DevAddr, DLSettings, RxDelay and optional CFList
4. Session keys NwkSKey and AppSKey derived with AES-128 from AppKey, nonces and NetID (1.1 splits into FNwkSIntKey, SNwkSIntKey, NwkSEncKey, AppSKey)
5. Join-Accept arrives in RX1 after 5 s (JOIN_ACCEPT_DELAY1) or RX2 after 6 s

## Gotcha
In 1.0.x DevNonce is random and reuse is rejected by some servers; in 1.0.4 and 1.1 it is a counter that must persist across reboots.

## Verify
- [ ] Join-Accept decoded with DevAddr
- [ ] Frame counters reset
- [ ] Reboot does not repeat DevNonce
