---
id: computing-software.firmware-embedded-development.iot-protocols.zigbee-security-keys
name: zigbee-security-keys
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [zigbee-security-keys, zigbee-ops, zigbee, network-key, link-key, install-code, trust-center, iot-protocols]
level: practitioner
status: draft
description: "Zigbee security keys: Understand Zigbee key hierarchy."
sources:
  - https://csa-iot.org/developer-resource/specifications-download-request/
  - https://www.zigbee2mqtt.io/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Zigbee security keys

**Goal:** Understand Zigbee key hierarchy.

## Steps
1. 128-bit network key encrypts and authenticates all NWK frames (AES-CCM*)
2. Trust Center link key protects delivery of the network key to a joiner
3. Default Global Trust Center Link Key ("ZigBeeAlliance09") is public and used by legacy HA devices; Zigbee 3.0 prefers unique install codes (key from 6-byte code plus CRC16, hashed)
4. Network key can be rotated by the Trust Center with key switch
5. Frame counters must stay increasing across restarts
6. Disable use of the default link key where devices allow

## Gotcha
Joining with the well-known key in open mode lets sniffers capture the network key during join; keep permit-join windows short.

## Verify
- [ ] Install code provisioned and joins
- [ ] Key rotation completes
- [ ] Frame counter persisted
