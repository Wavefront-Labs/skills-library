---
id: computing-software.firmware-embedded-development.iot-protocols.lorawan-mac-commands
name: lorawan-mac-commands
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [lorawan-mac-commands, lorawan-regional, lorawan, mac-command, linkadrreq, devstatusreq, iot-protocols]
level: practitioner
status: draft
description: "LoRaWAN MAC commands: Read the MAC layer commands in FOpts or the FPort 0 payload."
sources:
  - https://lora-alliance.org/resource_hub/lorawan-specification-v1-0-4/
  - https://lora-alliance.org/resource_hub/rp2-1-0-4-regional-parameters/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LoRaWAN MAC commands

**Goal:** Read the MAC layer commands in FOpts or the FPort 0 payload.

## Steps
1. Commands paired as Req/Ans: LinkCheckReq (0x02), LinkADRReq (0x03), DutyCycleReq (0x04), RXParamSetupReq (0x05), DevStatusReq (0x06), NewChannelReq (0x07), RXTimingSetupReq (0x08)
2. Up to 15 bytes fit in FOpts, otherwise use FPort 0 encrypted with NwkSKey
3. Device answers in next uplink; the network repeats until acked
4. DevStatusAns gives battery (1-254, 255 unknown) and SNR margin
5. Class B and C add commands such as PingSlotInfoReq (class B)

## Gotcha
Ignored answers loop the request; ensure the device returns an Ans for each Req in the same uplink.

## Verify
- [ ] Packet decoder shows Req/Ans pairs
- [ ] LinkADR applied and acked
- [ ] FOpts length at most 15
