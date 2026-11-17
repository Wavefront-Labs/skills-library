---
id: engineering-technology.aerospace-engineering.spacecraft-systems-design.propellant-mass-from-delta-v
name: propellant-mass-from-delta-v
category: engineering-technology
field: aerospace-engineering
product: spacecraft-systems-design
tags: [spacecraft, propulsion-subsystem, propellant-mass, delta-v-budget, rocket-equation, isp, propellant-margin, residuals]
level: practitioner
status: verified
description: "Convert a spacecraft delta-v budget to propellant mass with the rocket equation, using typical Isp values, residuals and margins by propulsion type."
sources:
  - "Wertz and Larson, Space Mission Analysis and Design"
  - "Sutton and Biblarz, Rocket Propulsion Elements"
  - "Brown, Elements of Spacecraft Design"
  - "NASA Small Spacecraft Technology State of the Art, in-space propulsion chapter (2021): https://www.nasa.gov/wp-content/uploads/2021/10/4.soa_in-space_propulsion_2021.pdf"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Propellant mass from delta-v

**Goal:** propellant to carry for a manoeuvre budget.

## Equation
`m_p = m_0 (1 - exp(-Delta v/(Isp g0)))`, `g0 = 9.80665 m/s^2`. For several burns use the sequential form; do not add propellant fractions.

## Typical specific impulse ranges (vendor data governs)
- NASA small-spacecraft survey (2021): cold and warm gas about 30-110 s; hydrazine monopropellant 200-285 s across surveyed devices (200-235 s for 1 N class or larger); alternative mono- and bipropellants 160-310 s; larger bipropellant engines are higher (confirm vendor data); electric propulsion in the thousands of seconds (see electric propulsion skill).

## Budget items
- Orbit insertion, station-keeping, phasing, attitude control (momentum dumping), collision avoidance reserve, deorbit or disposal burn.
- Margin on `Delta v` (commonly 5-10% or more at early design (gated: unconfirmed, source is paywalled or blocked)), residual and trapped propellant (a few percent of loaded mass, per vendor data), and pressurant.

## Procedure
1. Tabulate `Delta v` per manoeuvre with its margin.
2. Order burns by sequence and compute propellant for each with the evolving mass.
3. Add residuals and uncertainties; compare with tank capacity.
4. Re-run when dry mass changes (iterative).

## Gotchas
- Using wet mass when dry mass is needed (or vice versa).
- Disposal compliance (orbital debris guidelines) must be funded at the start.

## Verify
- [ ] A 100 m/s manoeuvre at Isp 220 s on a 500 kg spacecraft needs 22.6 kg (recomputed: 22.65).
