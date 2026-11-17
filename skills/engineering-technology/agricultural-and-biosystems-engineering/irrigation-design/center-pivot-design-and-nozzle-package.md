---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.center-pivot-design-and-nozzle-package
name: center-pivot-design-and-nozzle-package
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, center-pivot-design, sprinkler-design, sprinkler-irrigation-design, nozzle-package, end-gun, pivot-speed, pressure-regulator]
level: practitioner
status: gated
description: "Size a center pivot: flow from area and depth, pivot-point pressure, graduated nozzle package along the span, end gun, speed and timer settings."
sources:
  - "Keller & Bliesner, Sprinkle and Trickle Irrigation"
  - "USDA NRCS National Engineering Handbook, Part 623 Irrigation (https://www.nrcs.usda.gov)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Center pivot design and nozzle package

**Goal:** uniform depth over a circle with the lowest pumping pressure for the application rate.

## Capacity
`Q (m3/h) = 10 x A (ha) x d_g (mm/day) / T (h/day)` with A the irrigated area including end gun if used, d_g gross depth per day and T operating hours. The flow in the pivot pipe at radius r is the flow of the area beyond r.

## Nozzle package
- Discharge per unit length must be proportional to the radius (area per unit length grows with r). Nozzle sizes therefore increase toward the end of the lateral, with the manufacturer's software computing sizes and spacings for a chosen pressure profile.
- **Pressure regulators** at each drop keep nozzle pressure constant against elevation changes; use them on sloped fields.
- **Low-pressure spray**: drop tubes with spray plates reduce pumping energy (often 70-140 kPa at the nozzle (gated: unconfirmed, source is paywalled or blocked)) but raise the application rate and runoff risk.
- **End gun / corner arm**: boosts coverage beyond the last tower; needs booster pump if at low pressure.

## Speed and depth
The last tower speed sets the revolution time; depth per revolution (mm) = 1000 x Q (m3/h) x revolution time (h) / area (m2), so slowing the pivot (percent timer) increases depth. Typical revolution times range from about 12 h to several days (gated: unconfirmed, source is paywalled or blocked).

## Pressure at pivot point
`P = nozzle pressure + friction loss along the pivot pipe + elevation difference + losses in valves, pivot base and (if used) the end gun`.

## Gotchas
- Wheel tracks rutting with high application rate on soft soils.
- Nozzle wear increases flow; check packages every few years (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] Catch-can test (ASABE S436) shows Heermann-Hein CU of about 85-90 percent or better (gated: unconfirmed, source is paywalled or blocked).
