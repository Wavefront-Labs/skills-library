---
id: engineering-technology.automotive-vehicle-engineering.chassis-suspension-design.brake-force-distribution
name: brake-force-distribution
category: engineering-technology
field: automotive-vehicle-engineering
product: chassis-suspension-design
tags: [brake-balance, brake-force-distribution, ideal-brake-distribution, adhesion-utilisation, ebd, proportioning-valve]
level: practitioner
status: verified
description: "Compute ideal front/rear brake distribution, choose the fixed split and proportioning, and check adhesion utilisation against regulatory expectations."
sources:
  - "Limpert, Brake Design and Safety"
  - "UN Regulation 13-H adhesion utilisation requirements; confirm current edition"
  - "https://www.ecfr.gov/current/title-49/part-571/section-571.135"
  - "https://www.mlit.go.jp/jidosha/un/UN_R013H.pdf"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Brake force distribution

1. Dynamic axle loads at deceleration z (in g; lf and lr are the CG distances to the front and rear axle, L = lf + lr, h = CG height): `Fz_f = m*g*(lr + z*h)/L`, `Fz_r = m*g*(lf - z*h)/L`.
2. **Ideal distribution:** front and rear brake forces proportional to dynamic axle loads, so both axles reach friction limit together: `Fxf/Fxr = (lr + z*h)/(lf - z*h)`. The ideal curve bends toward the front as z grows.
3. **Fixed split:** `beta = Fxf/(Fxf + Fxr)` is a straight line; choose beta so the real line lies below the ideal curve for the usual load range (front locks first) up to a typical deceleration level; then limit rear force at higher z with proportioning valves or EBD.
4. **EBD (electronic brake-force distribution)** in the ABS/ESC unit approximates the ideal curve by modulating rear pressure.
5. Check **adhesion utilisation** curves for both axles across friction coefficients and load states (laden/unladen); UN R13-H Annex 6 requires, for all load states, that the rear-axle adhesion utilisation curve not lie above the front-axle curve for braking rates between 0.15 and 0.8; FMVSS 135 (S7.4.5) requires each rear-axle curve to lie below z = 0.9k for braking ratios 0.15 to 0.80, plus a wheel-lockup sequence check (front lockup before or with the rear) for vehicles without ABS. Confirm the current text and conditions (k range, load states) before design sign-off.
6. Check with regen present: regen on the driven axle shifts the effective distribution.
7. Verify by test: braking from speed on high-mu with logging of axle pressure.

**Gotchas:** forgetting payload/trailer variants; wear and temperature effects on pad friction.

## Verify
- [ ] Adhesion utilisation plot shows front-first lock across load states.
- [ ] Measured brake pressure ratio matches the design beta.
