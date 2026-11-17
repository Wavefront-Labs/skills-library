---
id: engineering-technology.aerospace-engineering.flight-dynamics-control.usaf-datcom-derivative-estimation
name: usaf-datcom-derivative-estimation
category: engineering-technology
field: aerospace-engineering
product: flight-dynamics-control
tags: [flight-dynamics, stability-derivatives, derivative-estimation, datcom, digital-datcom, empirical-methods, aerodynamic-coefficients]
level: practitioner
status: draft
description: "Estimate stability and control derivatives with USAF DATCOM or Digital DATCOM, set up the input namelists, and know its accuracy and limits."
sources:
  - "USAF Stability and Control DATCOM (Hoak et al., AFFDL-TR-79-3032)"
  - "Digital DATCOM user's manual (Williams and Vukelich)"
  - "Nelson, Flight Stability and Automatic Control"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# DATCOM derivative estimation

**Goal:** a first set of aerodynamic coefficients and derivatives from geometry.

## What it is
The USAF Stability and Control DATCOM is a compilation of empirical and semi-empirical methods; Digital DATCOM is a Fortran implementation that reads a namelist input file and writes `CL`, `CD`, `Cm`, and derivatives vs angle of attack and Mach.

## Input outline
- Flight conditions namelist (`FLTCON`): Mach, altitude, angle-of-attack list, Reynolds numbers.
- Synthesis (`SYNTHS`): cg and component positions; body (`BODY`), wing planform (`WGPLNF`), horizontal and vertical tails (`HTPLNF`, `VTPLNF`), airfoil sections, flap and control devices (`SYMFLP`, `ASYFLP`), plus case control cards (`DIM FT`, `DERIV RAD`, `SAVE`, `NEXT CASE`).
- Output: coefficients and static and dynamic derivatives (`CLA`, `CMA`, `CLQ`, `CMQ`, `CYB`, `CLB`, `CNB`, `CLP`, `CNR` ...).

## Practice
1. Build the input from the CAD dimensions with consistent units; define the reference area and chord.
2. Run, check that coefficients behave (lift slope, `Cm_alpha`).
3. Compare with a vortex-lattice or CFD solution and wind-tunnel data where available.
4. Use DATCOM results as starting values; tune with test data.

## Limits
Conventional configurations, empirical accuracy (typically a few to 20% on derivatives, worse at transonic and for unconventional layouts); no propulsion effects; check the method limits listed in the manual.

## Verify
- [ ] Lift slope and neutral point agree with an independent estimate within about 10%.
