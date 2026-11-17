---
id: engineering-technology.aerospace-engineering.spacecraft-systems-design.propellant-tank-sizing
name: propellant-tank-sizing
category: engineering-technology
field: aerospace-engineering
product: spacecraft-systems-design
tags: [tank-sizing, propellant-tank, pressure-vessel, tank-mass, residuals, propulsion-subsystem]
level: practitioner
status: gated
description: "Size propellant tanks from required propellant, residuals, ullage and maximum expected operating pressure, with wall thickness and proof and burst factors."
sources:
  - "AIAA S-080 and S-081 (space pressure vessels)"
  - "Sutton and Biblarz, Rocket Propulsion Elements"
  - "Wertz and Larson, Space Mission Analysis and Design"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Tank sizing

**Goal:** tank volume, wall thickness and mass.

## Volume
1. Propellant mass `m_p` from the rocket equation (see propellant-mass-from-delta-v).
2. Add residuals (unusable, trapped, loading tolerance, margin): often a few percent; use your programme's rule.
3. Volume `V_prop = m_total / rho_prop`; density at the loaded temperature.
4. Add ullage (gas volume): for blowdown from the relation in blowdown-pressurisation; for regulated systems, a few percent.
5. Tank volume `V_T = V_prop + V_ullage`.

## Wall thickness
- Thin-walled sphere: `t = P r / (2 sigma_allow)`; cylinder hoop stress `t = P r / sigma_allow` (standard thin-wall results, valid for t much less than r).
- `P` = maximum expected operating pressure (MEOP) times the required factors; space pressure vessel standards (AIAA S-080 for metallic, S-081 for composite overwrapped vessels) define proof and burst factors and verification; check the current text. Vendor sheets for AIAA S-080 qualified vessels quote proof 1.25 and burst 1.5 times MEOP (L3Harris ARDE spec sheets), but the standard's own factors are paywalled (gated: unconfirmed, source is paywalled or blocked); also the applicable standard and the launch site range safety rules govern.
- `sigma_allow` from material properties (titanium alloys and aluminium are common) with temperature.

## Mass
- Metallic sphere mass `m = 4 pi r^2 t rho_mat`.
- Pressure-vessel performance factor `P V / (m g)`; composite overwrapped tanks achieve higher.
- Add bosses, ports, propellant management devices (vanes, diaphragms, sponges).

## Gotchas
- Propellant management in zero-g matters for restart; tank internals affect slosh and acquisition.
- Compatibility of materials with the propellant, and cleanliness.
- Regulated-system tanks must handle regulator failure (overpressure relief).

## Verify
- [ ] The tank volume holds the loaded propellant plus ullage at the highest loading temperature.
