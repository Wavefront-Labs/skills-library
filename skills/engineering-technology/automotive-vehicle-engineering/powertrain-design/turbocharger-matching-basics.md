---
id: engineering-technology.automotive-vehicle-engineering.powertrain-design.turbocharger-matching-basics
name: turbocharger-matching-basics
category: engineering-technology
field: automotive-vehicle-engineering
product: powertrain-design
tags: [turbo-matching, turbocharger, compressor-map, turbine, surge, choke, wastegate, boost-pressure]
level: practitioner
status: gated
description: "Match a turbocharger to an engine: compressor flow and pressure ratio requirements, map margins, turbine sizing and wastegate behaviour."
sources:
  - "Watson and Janota, Turbocharging the Internal Combustion Engine"
  - "Heywood, Internal Combustion Engine Fundamentals"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Turbocharger matching basics

1. Airflow requirement at rated power: `mdot_air = P*bsfc*AFR/3600`-style estimate, or from volumetric efficiency: `mdot = eta_v*rho_in*Vd*N/2` (N rev/s, four-stroke).
2. Pressure ratio needed: from target BMEP/intake manifold pressure. Include intercooler and intake pressure drops.
3. Locate working points on the compressor map using **corrected** flow `mdot*sqrt(T01/Tref)/(p01/pref)`; keep points between surge line (with 10-15% margin (gated: unconfirmed, source is paywalled or blocked)) and choke, and near the island of highest compressor efficiency.
4. Low-speed torque: need boost at low rpm; smaller compressor/turbine and lower A/R improve response but choke flow at rated power.
5. Turbine: size by exhaust flow and pressure ratio to deliver compressor power; wastegate or VGT to control boost at high flow.
6. Transient: turbo lag depends on rotor inertia and exhaust energy; consider twin-scroll, e-boost, or two-stage.
7. Validate on a gas stand and engine dyno.

**Gotchas:** over-speed and temperature limits of the turbine; compressor surge during tip-out.

## Verify
- [ ] Rated and low-speed points plotted on the map inside margins.
- [ ] Turbine inlet temperature and shaft speed within supplier limits.
