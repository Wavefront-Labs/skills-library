---
id: engineering-technology.aerospace-engineering.aerodynamics.pressure-measurement-probes
name: pressure-measurement-probes
category: engineering-technology
field: aerospace-engineering
product: aerodynamics
tags: [aerodynamics, wind-tunnel, aero-testing, pressure-measurement, five-hole-probe, pressure-taps, scanner, transducer-calibration, pitot-static]
level: practitioner
status: draft
description: "Calibrate pitot-static, five-hole and pressure-tap instrumentation for aerodynamic testing and keep transducer and lag errors under control."
sources:
  - "Barlow, Rae and Pope, Low-Speed Wind Tunnel Testing"
  - "Tavoularis, Measurement in Fluid Mechanics"
  - "Manufacturer pressure scanner manuals"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Pressure measurement and probe calibration

**Goal:** trustworthy `Cp` and flow-angle data.

## Pressure taps and scanners
- Tap hole diameter ~0.3-1 mm, perpendicular to the surface, deburred; tube lengths set lag. Compute the settle time from tubing volume and length before sampling.
- Use electronic pressure scanners with periodic on-line calibration (zero and span) and temperature compensation.
- Use `Cp = (p - p_inf) / q_inf` with the reference static and dynamic pressure from the tunnel's reference system at the test section.

## Pitot-static and five-hole probes
- Pitot-static tube: static ports far enough from the nose to avoid acceleration effects; alignment error is small within about 10-15 degrees of yaw.
- Five-hole probes give total, static pressure and two flow angles via non-dimensional coefficients; calibrate in a known flow over a pitch-yaw grid and fit polynomials or look-up tables.

## Calibration practice
1. Calibrate transducers against a deadweight tester or a traceable reference; record the date and uncertainty.
2. Check tubing for leaks with a pressure-hold test.
3. Zero drift check before and after each run.

## Gotchas
- Blocked or leaking tubes give subtle `Cp` errors, find by repeating a known pressure.
- Dynamic pressure from a single reference upstream pitot may differ from the model location; apply the tunnel calibration.

## Verify
- [ ] Repeated polars agree within the uncertainty budget.
- [ ] A calibrated flow (a cylinder or a flat plate) reproduces known `Cp`.
