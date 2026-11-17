---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.pump-and-system-curve-duty-point
name: pump-and-system-curve-duty-point
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, system-curve, irrigation-pumping, pump-selection, duty-point, pump-curve, best-efficiency-point, centrifugal-pump]
level: practitioner
status: gated
description: "Plot a pump curve against the system curve to find the duty point, check best-efficiency range, and handle changing static head and friction through the season."
sources:
  - "USDA NRCS National Engineering Handbook, Part 623 Irrigation (https://www.nrcs.usda.gov)"
  - "Keller & Bliesner, Sprinkle and Trickle Irrigation"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pump and system curve duty point

**Goal:** a pump that runs near its best efficiency point (BEP) across the real range of operating conditions.

## System curve
`H_sys(Q) = H_static + K Q^2`, with static head = lift + elevation + required pressure head (at the operating nozzle or emitter) and K representing friction and minor losses (friction goes roughly as Q^1.85-2). Plot for the highest and lowest static heads (e.g. low water level in the well or a dirty filter), and for each zone.

## Pump curve
Obtain the manufacturer's curve of head, efficiency and power versus flow, plus NPSH required. The duty point is the intersection of pump head curve and system curve.

## Check
1. The duty point lies within roughly 70-120 percent of BEP flow for continuous duty (the preferred operating region of ANSI/HI 9.6.3; the exact range depends on pump type and edition (gated: unconfirmed, source is paywalled or blocked)); operation far from BEP raises vibration, recirculation and wear.
2. Check the power at the end of the curve for motor sizing (non-overloading curves are preferable).
3. Check each operating zone, not just the worst one; if the range is wide, use a VFD, multiple pumps, or bypass strategy.
4. Parallel pumps: add flows at the same head; series: add heads at the same flow; check for reverse flow with check valves.

## Gotchas
- Using the pump nominal flow without the system curve gives the wrong flow.
- Wear in the pump moves the curve down over years.

## Verify
- [ ] Measured flow (meter) and pressure at the pump match the predicted duty point within 5-10 percent.
