---
id: engineering-technology.aerospace-engineering.propulsion-engineering.rocket-equation-and-staging
name: rocket-equation-and-staging
category: engineering-technology
field: aerospace-engineering
product: propulsion-engineering
tags: [propulsion, rocket-performance, rocket-equation, tsiolkovsky, staging-optimisation, mass-ratio, structural-coefficient, payload-fraction]
level: practitioner
status: verified
description: "Use the Tsiolkovsky rocket equation and staging relations to size launch vehicle mass ratios, structural fractions and payload fraction for civil launchers."
sources:
  - "Sutton and Biblarz, Rocket Propulsion Elements"
  - "Wertz and Larson, Space Mission Analysis and Design"
  - "Curtis, Orbital Mechanics for Engineering Students"
  - "Delta-v budget (Earth surface to LEO 9.3-10 km/s): https://en.wikipedia.org/wiki/Delta-v_budget"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Rocket equation and staging

**Goal:** vehicle mass budget for a delta-v requirement.

## Rocket equation
`Delta v = V_e ln(m0/mf) = Isp g0 ln(m0/mf)` with `g0 = 9.80665 m/s^2`.
Example: `Isp = 350 s`, mass ratio 5 gives `Delta v = 350 x 9.80665 x ln 5 = 5.5 km/s`.

## Staging
- Stage structural coefficient `epsilon = m_s/(m_s + m_p)`; mass ratio `m0/mf = (1 + lambda)/(epsilon + lambda)` where `lambda` is payload ratio for the stage.
- Total `Delta v = sum_i Isp_i g0 ln(m0_i/mf_i)`.
- For identical `Isp` and `epsilon`, equal splitting of `Delta v` is optimal; with different values use Lagrange-multiplier optimisation to maximise payload.
- Orbit insertion `Delta v` budget: orbital velocity plus gravity and drag losses, minus Earth rotation benefit (see ascent losses); the total is typically about 9.3-10 km/s to low Earth orbit (orbital speed 7.8 km/s plus 1.5-2 km/s of drag and gravity losses, per the Wikipedia delta-v budget table).

## Procedure
1. Choose total `Delta v` with losses.
2. Select `Isp` and `epsilon` per stage (from comparable vehicles).
3. Optimise stage `Delta v` split for payload.
4. Check thrust-to-weight at liftoff (above about 1.2-1.5 (gated: unconfirmed, source is paywalled or blocked)) and at each stage.

## Gotchas
- Structural coefficient estimates must come from comparable vehicles; optimistic `epsilon` makes any design look feasible.
- Vacuum vs sea level `Isp` for the first stage.

## Verify
- [ ] Example above gives about 5.5 km/s (recomputed: 5.52 km/s); an equal-split scan of a two-stage case (Isp 300 s, epsilon 0.1, 9 km/s) peaks at 4.5 km/s per stage; payload fraction trends fall with higher `epsilon`.
