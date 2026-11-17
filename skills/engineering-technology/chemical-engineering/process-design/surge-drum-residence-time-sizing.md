---
id: engineering-technology.chemical-engineering.process-design.surge-drum-residence-time-sizing
name: surge-drum-residence-time-sizing
category: engineering-technology
field: chemical-engineering
product: process-design
tags: [chemical-engineering, process-design, pd-equipment-sizing, surge-drum-residence-time-sizing, surge-drum, reflux-drum, residence-time, hold-up-time, level-control, horizontal-drum, vessel-sizing, low-level-high-level]
level: practitioner
status: docs-checked
description: "Size a surge or reflux drum from residence time, level setpoints and control needs, then check diameter and orientation with L/D guidance."
sources:
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Surge drum and residence-time sizing

**Goal:** a drum volume that decouples upstream and downstream units and gives the operator time to react.

## Steps
1. **Choose hold-up time** between the normal level and the low-low (or high-high) trip, based on what the drum protects: use your company standard.
2. **Volumetric flow** at the maximum liquid rate (design margin included): V_liquid = Q x t.
3. **Level setpoints**: low-low, low, normal, high, high-high, with an instrument range; leave minimum liquid height above the outlet for NPSH and vortex breakers.
4. **Geometry**: choose horizontal for larger liquid volumes or vertical for small drums; compute the volume from the level segments, including the head volumes (a 2:1 elliptical head holds pi/24 D^3, about 0.131 D^3, so two heads add about 0.262 D^3).
5. **Vapour space** (if two-phase): see the knockout drum skill; the drum must satisfy both.
6. **Check** with the dynamic behaviour: the level controller tuning (see `engineering-technology.chemical-engineering.process-control.level-loop-averaging-control`).

## Gotchas
- A large drum delays response to disturbances and increases inventory (hazard); balance.
- Trip levels measured by the same transmitter as control reduce safety margin; separate instruments for trips.
- Total volume must include dead volume below the low-low level and above the high-high.

## Verify
- [ ] Volume recomputed from the final dimensions equals the holdup required.
- [ ] Level instrument range covers all setpoints.

## Checked
2026-11-01. Corrected the head volume: a 2:1 elliptical head is pi/24 D^3 (0.131 D^3) each, so two heads are 0.262 D^3, not 0.13 D^3. Removed typical hold-up times and the L/D range (no readable source; use the company standard).
Method: documentation only; no commands were run.
