---
id: engineering-technology.automotive-vehicle-engineering.nvh.loss-of-engine-masking-in-evs
name: loss-of-engine-masking-in-evs
category: engineering-technology
field: automotive-vehicle-engineering
product: nvh
tags: [masking, engine-masking, ev-refinement, wind-noise-audibility, tonal-noise, auditory-masking]
level: practitioner
status: draft
description: "Manage the loss of engine masking in EVs: newly audible wind, road, HVAC, accessory and trim noises, target levels and the debug approach."
sources:
  - "Harrison, Vehicle Refinement"
  - "Zwicker and Fastl, Psychoacoustics"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Loss of engine masking in EVs

1. Effect: broadband engine noise masks many sounds in a combustion car; in an EV the masking noise drops, so noise from wind, tyres, HVAC blowers, pumps, relays, squeaks and rattles, and the electric drive becomes audible.
2. Principle: auditory masking depends on spectral overlap; low-level tonal sounds become prominent in quiet backgrounds; psychoacoustic metrics (tonality, sharpness) matter more than A-weighted level.
3. Priorities: set lower targets for tonal and impulsive noises (clicks, pumps, coolant flow, thermal expansion ticks); require higher quality of seals and trim; add acoustic insulation (e.g. dash, door seals).
4. Typical sources to check: HVAC blower (tonal fans), cooling pumps, brake system actuator, steering EPS motor, seat motors, charging port actuators, relays and contactors, motor and gear whine, power inverter, high-frequency wind noise at the A-pillar and mirrors.
5. Debug: record in a quiet environment (low-noise road, stationary), check noise at several speeds, isolate by switching systems; use a microphone array or acoustic camera.
6. Sound design: some designers add background or sound signature cues; keep within comfort expectations and regulations.

**Gotchas:** squeaks and rattles are more audible; run buzz, squeak and rattle (BSR) testing.

## Verify
- [ ] Quiet-condition cabin spectrum shows no tonal components above the audibility threshold.
- [ ] BSR test results documented on rough roads.
