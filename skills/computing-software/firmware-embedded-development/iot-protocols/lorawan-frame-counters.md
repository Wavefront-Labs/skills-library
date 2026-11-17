---
id: computing-software.firmware-embedded-development.iot-protocols.lorawan-frame-counters
name: lorawan-frame-counters
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [lorawan-frame-counters, lorawan-security, lorawan, fcnt, replay-protection, iot-protocols]
level: practitioner
status: draft
description: "LoRaWAN frame counters: Keep counters monotonic to resist replay."
sources:
  - https://lora-alliance.org/resource_hub/lorawan-specification-v1-0-4/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LoRaWAN frame counters

**Goal:** Keep counters monotonic to resist replay.

## Steps
1. Uplink FCntUp and downlink FCntDown are 32-bit in each direction; only the lower 16 bits are sent in the frame
2. Server infers the upper 16 bits
3. Counter rollover after 65535 requires the 32-bit option to be supported (most modern servers)
4. A new join resets counters and rotates keys
5. Servers reject counters not above the last accepted one
6. 1.1 separates NFCntDown and AFCntDown

## Gotcha
Restoring a backup image that rewinds the stored counter locks the device out until rejoin.

## Verify
- [ ] Counter persisted every N frames or at power fail
- [ ] Replay of an old frame rejected
- [ ] Rejoin recovers
