---
id: engineering-technology.aerospace-engineering.flight-dynamics-control.takeoff-field-length
name: takeoff-field-length
category: engineering-technology
field: aerospace-engineering
product: flight-dynamics-control
tags: [flight-dynamics, aircraft-performance, flight-performance, takeoff-field-length, balanced-field-length, v1, vr, v2, accelerate-stop]
level: practitioner
status: gated
description: "Estimate takeoff ground roll and total field length, and understand V1, VR, V2 and balanced field length for transport category aircraft."
sources:
  - "14 CFR Part 25 sections 25.107, 25.109, 25.113"
  - "Raymer, Aircraft Design"
  - "Roskam, Airplane Design Part VII"
  - "https://www.law.cornell.edu/cfr/text/14/25.107"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Takeoff field length

**Goal:** takeoff distance for sizing and operations planning.

## Ground roll (simple)
`s_g ~ V_LOF^2 / (2 a_avg)` where `V_LOF` is lift-off speed and `a_avg` the acceleration evaluated at about 0.7 `V_LOF` (gated: unconfirmed, source is paywalled or blocked): `a = g [ T/W - mu - (D - mu L)/W ]` with rolling friction `mu` (0.02-0.04 for dry concrete (gated: unconfirmed, source is paywalled or blocked)). The acceleration form matches the standard force balance T - D - mu (W - L) divided by mass (checked algebraically). Add rotation time (1-3 s at `V_R`) and the air distance to 35 ft.

## Transport category definitions (read the current rule text)
- `V_1`: decision speed; `V_R`: rotation speed; `V_2`: takeoff safety speed attained by 35 ft.
- Takeoff distance (14 CFR 25.113(a), dry runway, eCFR text read) is the greater of (a) the distance along the 25.111 takeoff path to 35 ft above the surface (the critical-engine-failure path; 25.111 text not read this session) and (b) 115% of the all-engines-operating distance to 35 ft. On a wet runway 25.113(b) adds a distance to 15 ft consistent with reaching V2 before 35 ft. Without a clearway, takeoff run equals takeoff distance (25.113(c)).
- Accelerate-stop distance (25.109) is the greater of the engine-failure-at-V_EF case and the all-engines case, each with a stop and a distance equal to 2 seconds at V1. Wheel brakes are the baseline; other means must be safe, reliable and need no exceptional skill (25.109(e)); reverse thrust is not credited on a dry runway and may be on a wet one.
- Balanced field length: `V_1` chosen so that the accelerate-stop distance equals the continued takeoff distance.

## Procedure
1. Compute `V_S` from `CL_max` for the takeoff flap setting; set `V_R` and `V_2` per margins.
2. Integrate acceleration over speed (numerically) with thrust lapse, drag, ground effect and runway slope/wind/temperature.
3. Compute continued and rejected takeoff cases; find the balanced field length.
4. Apply runway surface, wind and slope corrections per the operational requirements.

## Gotchas
- Hot-and-high conditions size the engines; corrections for density altitude are large.
- Obstacle clearance (net flight path) limits payload on some runways.

## Verify
- [ ] Hand ground-roll estimate lies within about 15% of a numerical integration.
