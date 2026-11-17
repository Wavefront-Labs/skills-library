---
id: engineering-technology.automotive-vehicle-engineering.powertrain-design.road-load-from-vehicle-parameters
name: road-load-from-vehicle-parameters
category: engineering-technology
field: automotive-vehicle-engineering
product: powertrain-design
tags: [road-load-derivation, road-load, aerodynamic-drag, rolling-resistance, rotational-inertia, equivalent-mass]
level: practitioner
status: gated
description: "Derive road-load force from CdA, rolling coefficient, mass and rotating inertias, and convert to the A, B, C form used by regulations and simulation."
sources:
  - "Gillespie, Fundamentals of Vehicle Dynamics"
  - "Guzzella and Sciarretta, Vehicle Propulsion Systems"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Derive road load from vehicle parameters

- Aero: `Fa = 0.5*rho*CdA*v^2`, rho = 1.2 kg/m^3 at about 20 C and sea level. CdA = Cd x frontal area, so compute it per vehicle (e.g. Cd 0.30 x 2.2 m^2 = 0.66 m^2; Cd 0.35 x 2.8 m^2 = 0.98 m^2 for a larger SUV, illustrative values).
- Rolling: `Fr = fr*m*g*cos(theta)`, with fr of roughly 0.007-0.012 for modern low-rolling-resistance tyres on asphalt (gated: unconfirmed, source is paywalled or blocked); add a speed-dependent term `fr = f0 + f1*v^2` for high-speed accuracy.
- Grade: `Fg = m*g*sin(theta)`.
- Inertia: `F_i = (m + m_r)*a` where `m_r = (sum of wheel inertia + (Jm + Jt)*(i_total)^2)/Re^2`. Per gear, rotational mass is larger in low gears and with a high-speed motor behind a high gear ratio (evaluate m_r per gear; the typical 3-30% of vehicle mass is unconfirmed (gated: unconfirmed, source is paywalled or blocked)).
- Map to coefficients: `A = fr0*m*g`, `B ~ driveline/bearing drag`, `C = 0.5*rho*CdA`. In regulatory testing the coefficients come from coastdown, not calculation.
- Use temperature and altitude corrections for rho.

**Gotchas:** forgetting driveline spin losses at the wheel; using rolling resistance of the wrong tyre.

## Verify
- [ ] Calculated power at 100 km/h within about 10% of coastdown-based value.
- [ ] Equivalent mass per gear listed with the inertia inputs.
