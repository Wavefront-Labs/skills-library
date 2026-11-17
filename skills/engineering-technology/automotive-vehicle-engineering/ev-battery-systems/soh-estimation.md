---
id: engineering-technology.automotive-vehicle-engineering.ev-battery-systems.soh-estimation
name: soh-estimation
category: engineering-technology
field: automotive-vehicle-engineering
product: ev-battery-systems
tags: [soh-estimation, state-of-health, capacity-fade, resistance-growth, ageing-indicator, capacity-estimation]
level: practitioner
status: verified
description: "Estimate state of health from capacity fade and resistance growth using full-charge, partial-charge and pulse methods, with filtering and warranty reporting."
sources:
  - "Plett, Battery Management Systems Vol. 2"
  - "Birkl et al., diagnostic ageing literature (J. Power Sources)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# State of health estimation

1. Definitions: capacity SOH = `Q_now/Q_new` (energy-based variants exist); resistance SOH = `R_new/R_now`. Define which one the vehicle reports.
2. Capacity estimation: between two SOC points with accurate references: `Q = integral(I dt)/(SOC2 - SOC1)`; use rest-OCV points before and after a charge segment.
3. Resistance: from current-step voltage response at set SOC and temperature during normal driving or charging, normalised to temperature.
4. Filtering: SOH changes slowly; average many estimates, reject outliers, use recursive least squares or a dual Kalman filter.
5. Compensate for temperature and C-rate because both change apparent capacity.
6. Reporting: display and diagnostic (UDS) values; regulatory in some markets (not confirmed here, verify with the regulator): durability and battery-state-of-health reporting (check regional rules).
7. Validate on aged packs against lab capacity tests.

**Gotchas:** measuring when cold gives low apparent capacity; do not report a drop caused by temperature.

## Verify
- [ ] Estimated SOH within a few percent of bench capacity on aged packs.
- [ ] Estimate monotonic enough over time (no jumps) after filtering.
