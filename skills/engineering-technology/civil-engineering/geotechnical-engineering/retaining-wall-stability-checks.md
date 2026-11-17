---
id: engineering-technology.civil-engineering.geotechnical-engineering.retaining-wall-stability-checks
name: retaining-wall-stability-checks
category: engineering-technology
field: civil-engineering
product: geotechnical-engineering
tags: [retaining-wall, earth-pressure, rankine, coulomb, active-pressure, at-rest, sliding, overturning, bearing, cantilever-wall, gravity-wall]
level: practitioner
status: draft
description: "Check a gravity or cantilever retaining wall: Rankine/Coulomb pressures, surcharge and water, sliding, overturning, bearing, global stability, drainage and typical factors."
sources: ["Das, Principles of Foundation Engineering", "Coduto, Foundation Design", "AASHTO LRFD Bridge Design Specifications (walls and abutments)", "US Navy NAVFAC DM 7.02"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Retaining wall stability checks

**Goal:** external stability of a gravity or cantilever wall: sliding, overturning, bearing and global stability, plus drainage.

## Earth pressure
- Rankine active coefficient (level backfill, vertical smooth wall): Ka = (1 - sin phi')/(1 + sin phi') = tan^2(45 - phi'/2). At-rest K0 about 1 - sin phi' (normally consolidated). Passive Kp = 1/Ka.
- Coulomb includes wall friction and sloping backfill; use for inclined backs.
- Use active pressure only if the wall can yield; for restrained walls (basements, integral abutments) use at-rest.
- Add surcharge as Ka*q uniform pressure; water as hydrostatic unless drained; compaction-induced pressure where relevant.
- Ignore passive resistance in frost depth and in soil that may later be excavated.

## Checks (typical textbook working-stress values; confirm against the governing code)
| Check | Typical minimum FS |
|---|---|
| Overturning about toe | about 2.0 |
| Sliding (base friction + passive) | about 1.5 |
| Bearing | about 3 on ultimate, or LRFD resistance factor |
| Global stability | about 1.3 to 1.5 |
The resultant should lie in the middle third of the base (e <= B/6) on soil. LRFD codes use load and resistance factors instead of these.

## Drainage
Weep holes or perforated drain behind the wall, free-draining backfill, filter fabric. Most wall failures involve water.

## Verify
Sum forces and moments on a free body; toe/heel pressures q = (V/B)(1 +/- 6e/B); run a global slip circle past the heel.

> Professional guidance only. Design, sign-off and site decisions belong to a licensed/chartered engineer applying the codes adopted in the project jurisdiction; check edition and local amendments.
