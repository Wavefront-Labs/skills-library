---
id: engineering-technology.automotive-vehicle-engineering.crash-safety.seatbelt-pretensioner-and-load-limiter
name: seatbelt-pretensioner-and-load-limiter
category: engineering-technology
field: automotive-vehicle-engineering
product: crash-safety
tags: [belt-load-limiter, seatbelt, pretensioner, load-limiter, retractor, belt-force, seat-belt-reminder]
level: practitioner
status: gated
description: "Tune seatbelts for frontal crashes: pretensioner slack removal, load limiter force level, torsion bar and dual-stage limiting, and the chest-versus-excursion trade-off."
sources:
  - "Kramer, Passive Safety of Vehicles"
  - "belt system supplier technical papers"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Pretensioner and load limiter

1. **Pretensioner:** a pyrotechnic or electric actuator pulls the belt to remove slack within milliseconds of the sensing decision, coupling the occupant to the vehicle early to use stroke; some systems use buckle or retractor pretensioners, or both; reversible electric pretensioners act in pre-crash events.
2. **Load limiter:** a torsion bar in the retractor yields at a set belt force to limit chest loading; typical force levels of around 4-6 kN for adults in the front (gated: unconfirmed, source is paywalled or blocked) (varies by size, vehicle and airbag; check programme data). FMVSS 209 (49 CFR 571.209, eCFR) sets no load-limiter force band; its S4.5(a) only exempts belts with a load limiter from the elongation requirements, and it requires webbing breaking strength of 26,689 N (Type 1), 22,241 N (Type 2 pelvic) and 17,793 N (Type 2 upper torso).
3. Trade-off: lower limiter force reduces chest deflection but increases forward excursion (head-to-steering-wheel/dashboard distance); airbag provides the second restraint; tune together with sled tests.
4. Dual-stage or progressive limiters (variable torsion bar, dual stage) provide a higher initial force then reduce; they adapt to occupant size and crash severity.
5. Belt webbing: elongation properties (polyester) affect timing; routing, D-ring height, and buckle position determine shoulder belt path on the dummy.
6. Child and small-occupant considerations: 5th female dummy test, lower force limit settings for small occupants with adaptive systems.
7. Verify with sled test matrix: speeds, dummy sizes, belt force sensors, chest deflection and head excursion.
8. Reminder systems (belt reminder) are covered separately by regulation and consumer schemes.

**Gotchas:** limiter set too low causes the head to hit hard parts; too high gives chest deflection.

## Verify
- [ ] Sled tests show chest deflection below the limit and excursion within allowed clearance for all dummy sizes.
- [ ] Pretensioner fire timing and stroke verified on a rig.
