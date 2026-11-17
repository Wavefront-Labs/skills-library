---
id: engineering-technology.agricultural-and-biosystems-engineering.controlled-environment-systems.envelope-heat-loss-and-u-values
name: envelope-heat-loss-and-u-values
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: controlled-environment-systems
tags: [agricultural-and-biosystems-engineering, controlled-environment-systems, envelope-heat-loss, enclosure-heat-balance, ce-psychrometrics, u-value, heat-loss, design-heating-load, greenhouse-heating]
level: practitioner
status: verified
description: "Calculate heat loss through greenhouse or building envelopes with U-values for glazing, film, polycarbonate, perimeter and screens, and compute the design heating load."
sources:
  - "Arizona CEAC greenhouse heating handout (https://ceac.arizona.edu/sites/default/files/giacomelli%20heating.pdf)"
  - "Manitoba Agriculture, greenhouse heating and venting (https://www.gov.mb.ca/agriculture/crops/crop-management/heating-and-venting.html)"
  - "University of Wisconsin Extension greenhouse energy (https://fyi.extension.wisc.edu/energy/files/2016/09/GreenhouseEC_SAREApril2010_narrative.pdf)"
  - "ASHRAE Handbook (Fundamentals) (https://www.ashrae.org)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Envelope heat loss and U-values

**Goal:** the design heating load at the design outdoor temperature.

## Method
`Q = U A (T_in - T_out)` for each surface type, summed, plus infiltration (next skill) and perimeter losses. Use the design outdoor temperature from climate data (for instance a 99 percent heating design temperature) and the minimum indoor set point.

## Indicative U-values (W/m2 K, whole-structure, for orientation only; use maker or handbook data)
- Single glass about 6 (Wisconsin Extension: single pane about 1.1 Btu/h ft2 F = 6.2 W/m2 K); double glass about 3-3.5 (not confirmed from a free source).
- Single polyethylene film about 6-7 (Arizona handout: glass 1.2 and double PE 0.8 Btu/h ft2 F, about 6.8 and 4.5 W/m2 K); double inflated film about 4-5 (a 1981 glazing comparison gives 4.0; Ontario Publication 65 via Manitoba gives 5.0 for double polyethylene and 4.65 for acrylic).
- Twin-wall polycarbonate or acrylic, depending on thickness, about 3-4.
- Thermal screens reduce loss by a third or more depending on material and sealing.
Wind increases the outside film coefficient; a heating load is calculated with a design wind speed.

## Perimeter and floor
Heat loss through the soil at the perimeter and foundation can be treated with a perimeter loss coefficient per metre (handbook values); insulation at foundations reduces it.

## Heating load procedure
1. Compute envelope area by surface type, including gables and end walls.
2. Apply U-values and the design temperature difference.
3. Add the infiltration load.
4. Multiply the total by a safety factor and size heating with reserve (the factor is a designer's choice; check the method you follow).
5. Compare with the greenhouse standard method (for instance ASAE EP406.4, Heating, Ventilating and Cooling Greenhouses).

## Gotchas
- Using nominal glazing U-value ignores frames, gutters and curtains.
- Cold-sky radiation losses from film can lower the cover temperature below air temperature: condensation drip.

## Verify
- [ ] Measured fuel use in cold weather is within about 20 percent of the load estimate.
