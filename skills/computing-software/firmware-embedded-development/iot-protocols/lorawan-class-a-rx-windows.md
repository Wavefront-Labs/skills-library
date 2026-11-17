---
id: computing-software.firmware-embedded-development.iot-protocols.lorawan-class-a-rx-windows
name: lorawan-class-a-rx-windows
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [lorawan-class-a-rx-windows, lorawan-classes, lorawan, class-a, rx1, rx2, iot-protocols]
level: practitioner
status: draft
description: "LoRaWAN Class A receive windows: Time downlinks for the lowest-power class."
sources:
  - https://lora-alliance.org/resource_hub/lorawan-specification-v1-0-4/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LoRaWAN Class A receive windows

**Goal:** Time downlinks for the lowest-power class.

## Steps
1. Each uplink opens RX1 at RECEIVE_DELAY1 (default 1 s) and RX2 at RECEIVE_DELAY2 (1 s after RX1, default 2 s total)
2. RX1 uses the uplink channel and DR offset (RX1DROffset); RX2 uses fixed frequency and DR (EU868 869.525 MHz, DR0)
3. Server queues downlinks and sends only in these windows
4. Confirmed uplinks are acked in the next downlink
5. Change delay with RXTimingSetupReq

## Gotcha
Server cannot reach a Class A node between uplinks, so command latency equals the uplink interval.

## Verify
- [ ] Downlink received after uplink
- [ ] RX2 parameters match the network
- [ ] Queue drained on uplink
