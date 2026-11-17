---
id: engineering-technology.aerospace-engineering.orbital-mechanics.patched-conic-interplanetary-design
name: patched-conic-interplanetary-design
category: engineering-technology
field: aerospace-engineering
product: orbital-mechanics
tags: [orbital-mechanics, interplanetary, patched-conics, sphere-of-influence, hyperbolic-excess, c3, departure-burn, arrival-burn]
level: practitioner
status: verified
description: "Design interplanetary transfers with patched conics: heliocentric transfer, sphere of influence, hyperbolic excess speed, departure and arrival burns."
sources:
  - "Curtis, Orbital Mechanics for Engineering Students"
  - "Vallado, Fundamentals of Astrodynamics and Applications"
  - "Wertz and Larson, SMAD"
  - "NASA Sun, Mars and Moon fact sheets, https://nssdc.gsfc.nasa.gov/planetary/factsheet/"
  - "Recomputed in Python"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Patched-conic interplanetary design

**Goal:** first estimate of delta-v and timing for planetary transfers.

## Steps
1. **Heliocentric leg:** Hohmann or Lambert transfer between planet positions; get heliocentric velocities at departure and arrival.
2. **Hyperbolic excess:** `v_inf = |v_spacecraft - v_planet|` at each end; `C3 = v_inf^2`.
3. **Sphere of influence (SOI):** `r_SOI = a (m_planet/M_sun)^(2/5)` (computed with NASA masses and orbit sizes: Earth 9.25e5 km, Moon about 6.6e4 km around Earth); inside it use the planet-centred two-body problem.
4. **Departure burn from a circular parking orbit at radius `r_p`:** `Delta v = sqrt(v_inf^2 + 2 mu/r_p) - sqrt(mu/r_p)`.
5. **Arrival burn to capture into an orbit of periapsis `r_p`, eccentricity `e`:** `Delta v = sqrt(v_inf^2 + 2 mu/r_p) - sqrt(mu (1+e)/r_p)`.
6. Earth-Mars Hohmann: `v_inf` at Earth about 2.9 km/s (`C3` about 8.7 km^2/s^2), transfer time about 259 days (computed: `v_inf` 2.945 km/s, `C3` 8.67 km^2/s^2, 258.9 days with Sun GM 132,712e6 km^3/s^2, a = 149.598e6 and 227.956e6 km; departure from a 300 km circular Earth orbit costs 3.59 km/s).

## Practice
- Use Lambert solutions over launch and arrival dates for the real geometry (see porkchop plot practice).
- Include declination of the departure asymptote and launch vehicle capability (`C3` vs payload mass curves).

## Gotchas
- Patched conics ignores multi-body effects; refine with numerical integration for mission design.
- Ephemeris source and epoch matter for dates.

## Verify
- [ ] Earth-Mars Hohmann example reproduces `v_inf` of about 2.9 km/s at Earth.
