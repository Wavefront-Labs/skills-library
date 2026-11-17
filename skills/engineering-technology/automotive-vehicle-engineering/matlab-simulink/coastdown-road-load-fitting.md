---
id: engineering-technology.automotive-vehicle-engineering.matlab-simulink.coastdown-road-load-fitting
name: coastdown-road-load-fitting
category: engineering-technology
field: automotive-vehicle-engineering
product: matlab-simulink
tags: [coastdown-fitting, coastdown, road-load, road-load-coefficients, polyfit, simulink-parameters]
level: practitioner
status: gated
description: "Fit A, B, C road-load coefficients from coastdown speed traces and load them into a Simulink vehicle model with a residual check."
sources:
  - "Gillespie, Fundamentals of Vehicle Dynamics (SAE)"
  - "SAE J2263 listing (https://saemobilus.sae.org/content/J2263_202005)"
  - "ISO 10521-1:2006 (https://www.iso.org/standard/37533.html)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Fit road-load coefficients from coastdown data

**Goal:** get F(v) = A + B*v + C*v^2 (N, v in m/s) that reproduces measured deceleration, for use in the plant model.

1. Use a flat, dry, low-wind track, runs in both directions, tyres warmed, gearbox in neutral. Log speed at >= 10 Hz with GPS/wheel speed; the governing standards define wind, grade and repeat limits: SAE J2263 (Road Load Measurement Using Onboard Anemometry and Coastdown Techniques; covers 115 to 15 km/h; May 2020 revision per the SAE listing), ISO 10521-1 (Road vehicles, Road load, Part 1: determination under reference atmospheric conditions; title and scope (gated: unconfirmed, source is paywalled or blocked)) and the regulation procedure you certify to. Confirm the edition you must follow.
2. Smooth speed, differentiate, and form force: `F = -(m + m_rot)*dvdt` where `m_rot` is the rotating-inertia equivalent mass (wheels, driveline; commonly a few percent of mass (gated: unconfirmed, source is paywalled or blocked); take it from measured/CAD inertias).
3. Fit with `p = polyfit(v, F, 2)`; then `C=p(1); B=p(2); A=p(3)`. Average opposite-direction runs to cancel grade and wind.
4. Sanity-check: A is usually positive (rolling), C ~ 0.5*rho*CdA (ρ=1.2 kg/m^3 gives CdA); a negative B or A signals wind/grade error or too narrow a speed range.
5. In Simulink, feed A, B, C as `Simulink.Parameter` objects so the same model runs for different vehicles.

**Gotchas:** fitting over a narrow speed band makes A/B/C collinear, so quote force at reference speeds rather than trusting individual coefficients; drivetrain drag in neutral differs from drive-in-gear drag.

## Verify
- [ ] Simulated coastdown over the test range (SAE J2263 uses 115 to 15 km/h) matches measured time within a stated tolerance.
- [ ] Residual vs speed shows no systematic curve; both directions agree.
