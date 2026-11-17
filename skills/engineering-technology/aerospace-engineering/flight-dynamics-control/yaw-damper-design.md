---
id: engineering-technology.aerospace-engineering.flight-dynamics-control.yaw-damper-design
name: yaw-damper-design
category: engineering-technology
field: aerospace-engineering
product: flight-dynamics-control
tags: [flight-dynamics, control-laws, sas, yaw-damper, dutch-roll, washout-filter, rudder-feedback, stability-augmentation]
level: practitioner
status: draft
description: "Design a yaw damper with a washout filter and rudder feedback, tune gains to raise Dutch roll damping, and check turn coordination, authority and structural filtering."
sources:
  - "Nelson, Flight Stability and Automatic Control"
  - "Stevens, Lewis and Johnson, Aircraft Control and Simulation"
  - "Etkin and Reid"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Yaw damper design

**Goal:** more Dutch roll damping without opposing steady turns.

## Architecture
Yaw rate `r` (rate gyro) -> washout filter `s/(s + 1/tau_w)` -> gain `K_r` -> rudder command (via actuator). The washout removes the steady-state component so the rudder does not oppose coordinated turns.

## Design steps
1. Linearise the lateral-directional model at the design condition (see MATLAB linearization).
2. Choose `tau_w` of the order of a few seconds (slower than the Dutch roll period, so the filter passes the oscillation).
3. Root locus vs `K_r`: raise Dutch roll damping to the target (for example `zeta >= 0.2-0.4` depending on the criteria) with minimal movement of the spiral and roll modes.
4. Include actuator dynamics and sensor filtering; add structural notch filters if a flexible mode appears in the loop.
5. Limit rudder authority (a few degrees for many transports) and check the response to severe gusts and engine failure.
6. Verify margins (see margin analysis) across the envelope; schedule `K_r` with dynamic pressure if needed.

## Gotchas
- At high speed a gain tuned for low speed can cause rudder activity and fatigue loads.
- Failure of the yaw damper must be tolerable: the aircraft needs acceptable handling without it, as shown by the safety assessment.

## Verify
- [ ] Closed-loop Dutch roll damping meets the target at all scheduled points, and a steady turn entry produces no rudder opposition.
