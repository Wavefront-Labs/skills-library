---
id: engineering-technology.aerospace-engineering.orbital-mechanics.atmospheric-drag-and-orbit-decay
name: atmospheric-drag-and-orbit-decay
category: engineering-technology
field: aerospace-engineering
product: orbital-mechanics
tags: [drag-decay, orbit-decay, ballistic-coefficient, atmospheric-drag, orbital-lifetime, orbital-perturbations]
level: practitioner
status: gated
description: "Estimate orbit decay and lifetime from atmospheric drag using ballistic coefficient, density models and solar activity, and plan disposal compliance."
sources:
  - "Vallado, Fundamentals of Astrodynamics and Applications"
  - "Wertz and Larson, Space Mission Analysis and Design"
  - "Montenbruck and Gill, Satellite Orbits"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Drag and decay

**Goal:** lifetime and altitude loss for a LEO spacecraft.

## Equations
- Drag acceleration `a_d = -0.5 * rho * (Cd A / m) * v_rel^2` along the relative velocity. Ballistic coefficient `B = m/(Cd A)`.
- For a near-circular orbit the semi-major axis loss per revolution `da = -2 pi * (Cd A/m) * rho * a^2`. The altitude decay rate is `da/dt = -(Cd A/m) rho sqrt(mu a)`.
- Density falls roughly exponentially with altitude with a scale height of several tens of kilometres at 300 to 600 km, and varies by an order of magnitude with solar activity (gated: unconfirmed, source is paywalled or blocked).

## Procedure
1. Choose `Cd` (about 2.0 to 2.2 for compact satellites, a modelling assumption), area (tumbling average or attitude-dependent) and mass.
2. Get density from an atmosphere model (for example NRLMSISE-00 or JB2008) with forecast `F10.7` and `Ap`.
3. Integrate `da/dt` forward by quadrature or numerically propagate (see numerical-orbit-propagation).
4. Run the lifetime at low, nominal and high solar-activity scenarios.
5. Compare with disposal requirements: the international debris guideline of 25 years after end of mission (gated: unconfirmed, source is paywalled or blocked), and shorter post-mission requirements adopted by some regulators (for example the FCC 5-year rule: 47 CFR 25.114(d)(14)(vii)(D)(1) requires re-entry no later than five years after mission completion for space stations in or passing through LEO below 2,000 km, confirmed on eCFR text; check its applicability date). Check current regulatory text.

## Gotchas
- Lifetime is steeply dependent on altitude and solar cycle; give it as a range.
- Tumbling objects have a different mean area from the attitude-stabilised case.
- Decay accelerates near the end, and re-entry time is uncertain by days to months in the last revolutions.

## Verify
- [ ] The decay-rate and per-revolution formulas follow from the drag acceleration (da/dt = 2a^2 v/mu * a_d with v = sqrt(mu/a), derived this session). The decay-rate formula matches a numerical propagation within a few percent for a circular orbit with constant density.
