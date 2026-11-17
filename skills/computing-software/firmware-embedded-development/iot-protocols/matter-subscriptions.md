---
id: computing-software.firmware-embedded-development.iot-protocols.matter-subscriptions
name: matter-subscriptions
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [matter-subscriptions, matter-interaction, matter, subscription, min-interval, max-interval, iot-protocols]
level: practitioner
status: draft
description: "Matter subscriptions: Get state changes pushed to a controller."
sources:
  - https://csa-iot.org/developer-resource/specifications-download-request/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Matter subscriptions

**Goal:** Get state changes pushed to a controller.

## Steps
1. Subscribe request has MinIntervalFloor and MaxIntervalCeiling seconds
2. Server reports changes no faster than min and sends keepalive reports by max
3. Server may pick a smaller max
4. Controllers resubscribe after expiry or reboot
5. Sleepy devices (SIT, LIT in ICD cluster) negotiate longer intervals
6. Use KeepSubscriptions to retain existing ones on new subscribe

## Gotcha
Many subscriptions to one constrained device overload it; limit to a hub subscription and fan out in the cloud.

## Verify
- [ ] Report on change within the floor
- [ ] Heartbeat by ceiling
- [ ] Resubscribe after power cycle
