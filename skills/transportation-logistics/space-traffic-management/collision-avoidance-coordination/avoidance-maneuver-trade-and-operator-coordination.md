---
id: transportation-logistics.space-traffic-management.collision-avoidance-coordination.avoidance-maneuver-trade-and-operator-coordination
name: avoidance-maneuver-trade-and-operator-coordination
category: transportation-logistics
field: space-traffic-management
product: collision-avoidance-coordination
tags: [collision-avoidance, cola, avoidance-maneuver, debris-avoidance, operator-coordination, owner-operator, space-track, cdm, post-maneuver-screening, delta-v, in-track-maneuver, radial-maneuver, maneuver-timing, conjunction, satellite-operations, space-traffic-management, constellation, emergency-contact]
level: advanced
status: draft
description: "Designing an avoidance burn (direction, size, timing), screening the new trajectory, and coordinating with the other operator so two satellites don't both dodge into each other."
sources: ["NASA Spacecraft Conjunction Assessment and Collision Avoidance Best Practices Handbook (2023)", "Space Safety Coalition, Best Practices for the Sustainability of Space Operations"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Avoidance-manoeuvre trades and operator coordination

**Goal:** when a conjunction crosses your manoeuvre threshold, act in a way that
actually lowers risk — without creating a new conjunction, wasting propellant, or
colliding with an operator who also moved.

## 1. Before designing anything: who else can move?
- Check the secondary's type. Debris and rocket bodies can't manoeuvre; a payload
  might.
- If it's an active payload, **contact the operator immediately** — via the
  Space-Track operator contact listing, a constellation operator's published
  coordination channel, or your screening provider. Agree in writing **who moves**.
  Rule of thumb: the operator with more capability, more margin, or the more
  convenient timing moves; the other holds its planned trajectory and *shares its
  ephemeris*.
- Record the agreement with times (UTC) and both parties' contacts.

## 2. Trade the manoeuvre
| Option | Effect | When |
|---|---|---|
| In-track (along-velocity) burn, ~0.5–1 orbit before TCA or earlier | Shifts arrival time; tiny Δv buys large in-track separation | Default in LEO — cheapest per metre of separation |
| Radial-separation via in-track burn half an orbit earlier | Changes altitude at TCA | When in-track uncertainty dominates and radial miss is small |
| Cross-track (out-of-plane) burn | Direct sideways offset | Costly; rarely the best choice except short notice |
Design steps:
1. Generate 3–5 candidate burns (direction, Δv, execution time).
2. For each, propagate and **re-screen against the full catalogue** for 7 days — not
   just the original secondary.
3. Pick the candidate that brings Pc below your green threshold (e.g. < 1e-6 or two
   orders below the action threshold) with least Δv and no new yellow/red events.
4. Plan the **return** burn (restore altitude/phasing, station-keeping box, ground
   track) and screen that too.

## 3. Execute
- Upload the candidate ephemeris (CCSDS OEM, marked as the manoeuvre plan) to your
  screening provider *before* execution, and get a screening result back.
- Hold a Go/No-Go at a fixed lead time; latest data in, decision made, burn uploaded
  with margin for a missed ground pass.
- Keep a **waive-off point**: if new CDMs drop Pc below threshold before the commit
  time, cancel — not every planned burn needs to fly.
- After the burn: run OD from tracking, upload the as-flown ephemeris, confirm the
  post-manoeuvre screening is clean, notify the other operator.

## Gotchas
- Two operators both dodging without talking is the nightmare case; silence is not
  agreement.
- Autonomous collision-avoidance systems on large constellations may manoeuvre on
  their own — ask the operator how their system handles your shared ephemeris.
- Burns executed with thruster error (e.g. ±5 % magnitude) change separation; screen
  a dispersed case too for close calls.
- Electric-propulsion spacecraft need hours to days of thrusting — decide earlier.
- Clock/time-system errors in commanded burn times shift the result along track.
- *Exact green-target Pc and lead times vary by operator; numbers above are typical.*

## Verify
- [ ] Who-moves agreement recorded with the other operator (or secondary confirmed non-manoeuvrable).
- [ ] Chosen burn re-screened against the full catalogue: no new yellow/red events.
- [ ] Return/restore manoeuvre planned and screened.
- [ ] As-flown ephemeris uploaded and post-manoeuvre CDMs reviewed.
- [ ] Decision log contains data versions, Pc values, Go/No-Go time and the decision-maker.
