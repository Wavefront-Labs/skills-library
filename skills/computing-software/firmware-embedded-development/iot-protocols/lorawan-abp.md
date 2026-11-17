---
id: computing-software.firmware-embedded-development.iot-protocols.lorawan-abp
name: lorawan-abp
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [lorawan-abp, lorawan-activation, lorawan, abp, devaddr, iot-protocols]
level: practitioner
status: draft
description: "LoRaWAN ABP: Decide when static activation is acceptable."
sources:
  - https://lora-alliance.org/resource_hub/lorawan-specification-v1-0-4/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LoRaWAN ABP

**Goal:** Decide when static activation is acceptable.

## Steps
1. ABP pre-loads DevAddr, NwkSKey and AppSKey on the device and network server
2. No join; device transmits immediately
3. Frame counters start at zero and must persist, since the server rejects counters that go backwards
4. Disable counter check only on dev servers
5. Region channel and RX2 defaults are hard-coded, so set them explicitly
6. Prefer OTAA for production because ABP keys cannot be rotated without reflash

## Gotcha
Resetting a device to FCnt 0 after a power loss makes the server drop all uplinks as replays.

## Verify
- [ ] Counters stored in non-volatile memory
- [ ] Uplinks accepted after reboot
- [ ] Plan to move to OTAA
