---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.remote-telemetry-and-pivot-monitoring
name: remote-telemetry-and-pivot-monitoring
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, irrigation-telemetry, pivot-monitoring, remote-irrigation-control, center-pivot-control, scada, cellular-telemetry]
level: practitioner
status: gated
description: "Plan remote telemetry for irrigation: pivot position and status, pressure and flow sensing, communications options, alarms, security and power."
sources:
  - "ASABE Standards, Engineering Practices and Data (https://www.asabe.org)"
  - "Keller & Bliesner, Sprinkle and Trickle Irrigation"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Remote telemetry and pivot monitoring

**Goal:** know what each pump and pivot is doing, and be able to start, stop or change them from a phone or office.

## What to monitor
- Pivot: GPS position or angle, direction, speed percent, on or off, end gun state, pressure at the pivot point, safety trip status and wet or dry.
- Pumps: run state, discharge pressure, flow, power or current, and tank level.
- Field: soil moisture, weather (`et-based-and-sensor-based-automatic-scheduling`).

## Communications
- Cellular modems where coverage exists; long-range radio or LoRaWAN for remote sites (`lorawan-coverage-planning-for-farms`); satellite for no coverage.
- Check the network type (some old cellular data standards are being retired, so confirm the carrier's plans before buying hardware).

## Design
- Power: mains, solar and battery for sensors (`solar-and-battery-power-budgeting-for-field-nodes`).
- Alarms: loss of pressure, stopped pivot, fault, high or low flow, and communication failure with escalation rules.
- Safety: remote start must not start a machine when people may be near. Use local indicators, audible warnings or interlocks as the maker specifies.
- Security: strong passwords, no default accounts, two-factor where offered, updated firmware, restricted access.

## Verify
- [ ] Alarm test by deliberately tripping a pivot safety.
- [ ] Data logged for pressure and position over a week.
- Vendor features and the cellular standards still in service in your region: confirm with the carrier and vendor (gated: unconfirmed, source is paywalled or blocked).
