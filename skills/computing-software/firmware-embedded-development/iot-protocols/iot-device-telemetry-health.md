---
id: computing-software.firmware-embedded-development.iot-protocols.iot-device-telemetry-health
name: iot-device-telemetry-health
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [iot-device-telemetry-health, iot-operations, telemetry, heartbeat, health-metrics, fleet-monitoring, iot-protocols]
level: practitioner
status: draft
description: "Device health telemetry: Monitor a fleet cheaply."
sources:
  - https://docs.aws.amazon.com/wellarchitected/latest/iot-lens/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Device health telemetry

**Goal:** Monitor a fleet cheaply.

## Steps
1. Report a compact health message: firmware version, uptime, reset reason, battery voltage, RSSI/SNR, free heap, error counters
2. Send on boot, then at intervals with jitter
3. Use retained or shadow for the latest state
4. Set alerts on missing heartbeats (2-3 intervals) using last-will or server timers
5. Log tags with firmware version for cohort analysis
6. Rate limit logs and keep an on-device ring buffer for crash info

## Gotcha
All devices reporting at the top of the hour overloads the backend; add random jitter.

## Verify
- [ ] Dashboard shows last-seen
- [ ] Alert fires for silent device
- [ ] Version cohorts visible
