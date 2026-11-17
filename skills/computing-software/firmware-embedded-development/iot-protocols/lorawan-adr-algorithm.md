---
id: computing-software.firmware-embedded-development.iot-protocols.lorawan-adr-algorithm
name: lorawan-adr-algorithm
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [lorawan-adr-algorithm, lorawan-adr-airtime, lorawan, adr, adr-ack-limit, snr-margin, iot-protocols]
level: practitioner
status: draft
description: "LoRaWAN adaptive data rate: Tune ADR for static versus mobile devices."
sources:
  - https://lora-alliance.org/resource_hub/lorawan-specification-v1-0-4/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LoRaWAN adaptive data rate

**Goal:** Tune ADR for static versus mobile devices.

## Steps
1. Device sets the ADR bit in the FCtrl field; the server measures SNR of recent uplinks (typically last 20) and sends LinkADRReq with DR, TX power and NbTrans
2. Margin installation: required SNR per SF (SF7 about -7.5 dB, SF12 about -20 dB) plus a device margin of ~10 dB
3. Device ADR_ACK_LIMIT 64 and ADR_ACK_DELAY 32: if no downlink, the device sets ADRACKReq, then lowers DR
4. Use ADR for fixed nodes only
5. Disable it and fix SF for mobile trackers

## Gotcha
ADR on moving devices chases stale SNR and loses packets after the node moves away.

## Verify
- [ ] Fixed node settles on SF7 or SF8
- [ ] ADR off for mobile
- [ ] Uplink ADRACKReq seen on silence
