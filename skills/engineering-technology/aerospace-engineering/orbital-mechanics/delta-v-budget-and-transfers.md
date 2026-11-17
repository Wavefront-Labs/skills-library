---
id: engineering-technology.aerospace-engineering.orbital-mechanics.delta-v-budget-and-transfers
name: delta-v-budget-and-transfers
category: engineering-technology
field: aerospace-engineering
product: orbital-mechanics
tags: [orbital-mechanics, astrodynamics, mission-design, delta-v, delta-v-budget, hohmann-transfer, bi-elliptic, plane-change, gto, geo, leo, rocket-equation, tsiolkovsky, specific-impulse, isp, station-keeping, deorbit, disposal, edelbaum, low-thrust, propellant-budget, gmat, stk, orekit, smad]
level: practitioner
status: gated
description: "Build a mission delta-v budget: Hohmann and bi-elliptic transfers, plane changes, rocket equation, launch, station-keeping, deorbit and margin policy."
sources:
  - "Curtis, Orbital Mechanics for Engineering Students"
  - "Vallado, Fundamentals of Astrodynamics and Applications"
  - "Wertz and Larson (eds.), Space Mission Analysis and Design (SMAD); Wertz et al., Space Mission Engineering: The New SMAD"
  - "Bate, Mueller and White, Fundamentals of Astrodynamics"
  - "IADC Space Debris Mitigation Guidelines"
  - "eCFR 47 CFR 25.114, https://www.ecfr.gov/current/title-47/part-25/section-25.114"
  - "Recomputed in Python (Hohmann, Edelbaum, plane change, deorbit, graveyard)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Delta-v budget and impulsive transfers — from orbit plan to propellant mass

**Goal:** a line-itemised delta-v budget with margins for every phase of a mission, turned
into propellant mass via the rocket equation, good enough for Phase A sizing.

## 1. Constants and core relations
- Earth `μ = 398600.4418 km³/s²`, `R_E = 6378.137 km`, `g0 = 9.80665 m/s²`.
- Vis-viva: `v = sqrt(μ (2/r − 1/a))`. Circular: `v_c = sqrt(μ/r)`.
- Hohmann between circular r1 → r2:
  `Δv1 = sqrt(μ/r1) (sqrt(2 r2/(r1+r2)) − 1)`, `Δv2 = sqrt(μ/r2) (1 − sqrt(2 r1/(r1+r2)))`,
  transfer time = half the transfer-ellipse period.
- Pure plane change: `Δv = 2 v sin(Δi/2)`. Do it where v is smallest (apoapsis) and
  combine it with an in-plane burn there: `Δv = sqrt(v1² + v2² − 2 v1 v2 cos Δi)`.
- Bi-elliptic beats Hohmann only for `r2/r1 > ~11.94` (for every `rb` above ~15.58), and takes much
  longer; rarely worth it for Earth missions.
- Rocket equation: `Δv = Isp g0 ln(m0/mf)` → `m_prop = m0 (1 − exp(−Δv/(Isp g0)))`.

```python
import math
mu = 398600.4418
def hohmann(r1, r2):
    a = (r1 + r2) / 2
    dv1 = math.sqrt(mu/r1) * (math.sqrt(2*r2/(r1+r2)) - 1)
    dv2 = math.sqrt(mu/r2) * (1 - math.sqrt(2*r1/(r1+r2)))
    return dv1, dv2, math.pi * math.sqrt(a**3/mu) / 3600   # km/s, km/s, hours
print(hohmann(6378.137+300, 42164.0))   # ~2.43, ~1.46 km/s, ~5.3 h
def prop_mass(m0, dv_kms, isp):
    return m0 * (1 - math.exp(-dv_kms*1000/(isp*9.80665)))
```

## 2. Reference numbers (use to sanity-check, not to replace analysis)
- Surface to LEO (gated: unconfirmed, source is paywalled or blocked): ~9.3–9.8 km/s including ~1.5–2 km/s of gravity and drag losses
  (vehicle-dependent; launcher performance is normally taken from the user's guide as
  mass-to-orbit, not as delta-v).
- LEO (300 km) → GEO coplanar Hohmann ≈ 3.9 km/s. From a 28.5° launch site, GTO
  perigee burn ~2.4–2.5 km/s and apogee burn with plane change ~1.8 km/s.
- Low-thrust circle-to-circle (Edelbaum): `Δv = sqrt(v0² + v1² − 2 v0 v1 cos(π Δi / 2))`;
  LEO→GEO is ~4.7 km/s coplanar and ~5.95 km/s with 28.5° (computed from a 300 km start). Low thrust always costs more
  delta-v than impulsive, but far less propellant thanks to Isp.
- GEO station-keeping (gated: unconfirmed, source is paywalled or blocked): north–south ~45–50 m/s per year, east–west a few m/s per year.
- LEO drag make-up varies by an order of magnitude with altitude and the solar cycle;
  compute it with an atmosphere model (e.g. NRLMSISE-00) at the solar-activity level you
  must design to.
- Deorbit from 500 km circular to a ~50 km perigee: roughly 130 m/s (computed: 129.8 m/s).
- Disposal policy: IADC guideline historically 25 years in LEO (gated: unconfirmed, source is paywalled or blocked); the US FCC rule in 47 CFR 25.114(d)(14)(vii)(D)(1) requires atmospheric re-entry as soon as practicable and no later than five years after mission end for NGSO stations in LEO below 2,000 km (eCFR). Confirm which rule applies
  to your licence. GEO graveyard: raise ≥ ~235 km above GEO plus a solar-pressure term
  (IADC formula (gated: unconfirmed, source is paywalled or blocked)); two-burn cost computed as 9-11 m/s for 250-310 km.

## 3. Typical Isp (vacuum, indicative (gated: unconfirmed, source is paywalled or blocked))
Cold gas 50–75 s · hydrazine monoprop 220–235 s · green monoprop (AF-M315E/LMP-103S)
~230–255 s · MMH/NTO biprop apogee engines ~310–325 s · Hall thrusters ~1,500–2,000 s ·
gridded ion ~2,500–3,500 s. Use the specific thruster datasheet value and its
steady-state vs pulsed Isp; pulsed ADCS firings can be far below steady state.

## 4. Building the budget
1. List phases: launcher dispersion correction, orbit raising, phasing, plane change,
   station-keeping per year × life, collision avoidance allowance, momentum management
   (if thrusters unload wheels), end-of-life disposal.
2. For each item: nominal Δv, source (analysis or rule of thumb), and margin.
3. Apply margins by maturity: deterministic manoeuvres computed analytically commonly get
   ~5%; stochastic items (dispersions, collision avoidance) are sized at 3-sigma or 99%.
   Many agencies also add a system-level margin; follow your programme's margin policy.
4. Convert to propellant **sequentially**, burn by burn, from the wet mass at each burn;
   add residuals and unusable propellant (~2–3%) and pressurant.
5. Finite-burn (gravity) losses: small for high-thrust short burns; add a few percent for
   long low-T/W burns or model them in GMAT/STK/Orekit.

## Gotchas
- Using the total Δv once in the rocket equation with mixed engines (biprop then
  monoprop) is wrong; split by propulsion system.
- Plane changes in LEO are ruinously expensive (~133 m/s per degree at 7.6 km/s); pick the
  launch inclination and RAAN (launch window) to avoid them.
- Sun-synchronous orbits need inclination maintenance only from third-body effects;
  budget it but it is small. Check SSO inclination from the J2 relation, not memory.

## Verify
- [ ] Hohmann LEO→GEO script reproduces ~3.9 km/s and ~5.3 h transfer time.
- [ ] Every Δv line has a source, a margin and the propulsion system it uses.
- [ ] Propellant computed burn-by-burn with the correct Isp and mass at each burn.
- [ ] Disposal meets the regulation that applies to the mission.
- [ ] Budget cross-checked against a numerical propagation (GMAT, STK or Orekit).
