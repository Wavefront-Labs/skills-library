---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.mainline-sizing-and-economic-velocity
name: mainline-sizing-and-economic-velocity
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, mainline-sizing, economic-velocity, pipe-friction, hazen-williams, darcy-weisbach, pipe-selection, pipeline-design]
level: advanced
status: gated
description: "Size an irrigation mainline: friction loss with Hazen-Williams or Darcy-Weisbach, velocity limits, economic pipe diameter, pressure class and pump energy trade-off."
sources:
  - "USDA NRCS National Engineering Handbook, Part 623 Irrigation (https://www.nrcs.usda.gov)"
  - "Keller & Bliesner, Sprinkle and Trickle Irrigation"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Mainline sizing and economic velocity

**Goal:** the pipe size and class that minimise lifetime cost (pipe plus pumping energy) while meeting pressure and velocity limits.

## Friction loss
- Hazen-Williams: hf proportional to L x Q^1.852 / (C^1.852 x D^4.87); C is about 150 for new PVC and polyethylene (gated: unconfirmed, source is paywalled or blocked) and lower for aged steel; SI and US constants differ, so use consistent units.
- Darcy-Weisbach with the Colebrook equation is more general, essential for unusual fluids or temperatures.
- Add minor losses (fittings, valves, filters) explicitly.

## Velocity limits
Commonly 1.5 m/s (5 ft/s = 1.524 m/s, computed) is used as a screening maximum (gated: unconfirmed, source is paywalled or blocked) for mainlines to limit surge; many agencies set lower limits for pipes with quick-closing valves. Very low velocity (under 0.6 m/s (gated: unconfirmed, source is paywalled or blocked)) may settle solids.

## Economics
Larger pipe lowers friction and pumping energy but costs more. Compute annualised pipe capital plus annual pumping energy cost for each candidate diameter and choose the minimum (the "economic diameter"); results depend on energy price and hours.

## Pressure class
Select pipe pressure class above maximum working pressure plus surge allowance (`water-hammer-and-surge-protection`). For PVC, class ratings account for temperature derating; follow the pipe maker's guide.

## Verify
- [ ] Hydraulic grade line plotted along the profile; check minimum pressures at high points.
- [ ] Velocity table at design flows.
- Local standards and C values: use the pipe supplier's data and the governing agency standard.
