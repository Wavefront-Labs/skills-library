---
id: engineering-technology.automotive-vehicle-engineering.crash-safety.airbag-sizing-and-venting
name: airbag-sizing-and-venting
category: engineering-technology
field: automotive-vehicle-engineering
product: crash-safety
tags: [airbag-design, airbag, inflator, vent-area, bag-volume, tether, tank-test]
level: practitioner
status: gated
description: "Size an airbag module: bag volume and geometry, inflator output via tank test, vent area, tethers and fold, validated by sled and out-of-position tests."
sources:
  - "Kramer, Passive Safety of Vehicles"
  - "airbag supplier technical papers; FMVSS 208 out-of-position provisions"
  - "https://www.law.cornell.edu/cfr/text/49/571.208"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Airbag sizing and venting

Practice guidance only: airbag modules are pyrotechnic devices; development and handling follow the supplier's and the employer's safety procedures. The inflator composition is not in scope here.

0. Bag volume figures below are unconfirmed (gated: unconfirmed, source is paywalled or blocked); FMVSS 208 contains out-of-position provisions (checked in 49 CFR 571.208).
1. Starting point: bag volume driven by the position and the gap to be filled; driver bags are tens of litres and passenger bags typically greater than a hundred litres (use your vehicle data).
2. Inflator characterisation: run tank tests (inflator into a rigid tank at set conditions) to measure pressure-time curves; match mass flow and temperature to the bag requirement; dual-stage or adaptive inflators change output by crash severity or occupant presence.
3. Vent area: fixed vents or controlled vents determine how quickly the bag deflates when the occupant loads it; larger vents lower chest loads but allow bottoming out; tune with sled tests for 50th male and small female.
4. Tethers and geometry: tethers shape the bag, and affect early inflation reach and the force on the occupant's head; fold pattern controls the unfolding path and out-of-position injury risk.
5. Timing: the time-to-fire (from the sensing algorithm) and bag fill time determine the contact moment with the occupant; the bag should be mostly full before the head arrives.
6. Out-of-position tests (child and small adult near the module) are part of FMVSS 208 provisions and consumer ratings; confirm the tests.
7. Materials: nylon fabric, silicone coating, seam strength tested; ageing and temperature conditioning (cold and hot deployments).

**Gotchas:** high inflator aggressiveness gives injuries in out-of-position cases; always test.

## Verify
- [ ] Head and chest results across dummy sizes and positions within criteria.
- [ ] Hot and cold deployments show consistent timing and pressure.
