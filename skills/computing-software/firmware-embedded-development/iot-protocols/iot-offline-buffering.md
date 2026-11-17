---
id: computing-software.firmware-embedded-development.iot-protocols.iot-offline-buffering
name: iot-offline-buffering
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [iot-offline-buffering, iot-operations, store-and-forward, offline-buffer, flash-ringbuffer, backfill, iot-protocols]
level: practitioner
status: draft
description: "Offline buffering and store-and-forward: Avoid data loss during connectivity gaps."
sources:
  - https://docs.aws.amazon.com/wellarchitected/latest/iot-lens/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Offline buffering and store-and-forward

**Goal:** Avoid data loss during connectivity gaps.

## Steps
1. Buffer readings in a flash ring buffer with sequence numbers and timestamps
2. Wear-level by using a log-structured store (LittleFS, NVS)
3. On reconnect, send oldest first at a capped rate, or newest first for live dashboards
4. Mark backfilled records so consumers do not treat them as live
5. Drop policy when full: oldest low-priority first
6. Use QoS 1 and ack-based deletion

## Gotcha
Deleting buffered data on publish rather than on ack loses records if the link drops mid-send.

## Verify
- [ ] Disconnect test: no loss after reconnect
- [ ] Backfill rate does not starve live data
- [ ] Flash writes within endurance budget
