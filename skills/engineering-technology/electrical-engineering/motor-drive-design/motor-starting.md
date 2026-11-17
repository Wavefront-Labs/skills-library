---
id: engineering-technology.electrical-engineering.motor-drive-design.motor-starting
name: motor-starting
category: engineering-technology
field: electrical-engineering
product: motor-drive-design
tags: [direct-on-line, dol-star-delta-comparison, electrical-engineering, motor-drive-design, motor-start-voltage-dip, motor-starting, soft-starter, star-delta-starter, starting-voltage-dip]
level: practitioner
status: draft
description: "Compare DOL, star-delta, autotransformer and soft-starter methods and compute the starting voltage dip on the supply."
sources:
  - "https://www.iec.ch/"
  - "https://standards.ieee.org/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Induction motor starting methods

| Method | Start current | Start torque | Notes |
|---|---|---|---|
| DOL | 6 to 8 x FLC | 100 % | simple, hardest on the supply |
| Star-delta | about 1/3 of DOL | about 1/3 | open transition spike; light-load starts only |
| Autotransformer | k^2 of DOL | k^2 | taps 50 to 80 % |
| Soft starter | set by current limit | falls with V^2 | ramp; use bypass contactor after |
| VFD | up to rated | up to rated | best control, harmonic content |

**Voltage dip estimate:** `dV (pu) ~ I_start x Z_source`, or with MVA: `dV ~ S_start / (S_start + S_sc)`. Example: 500 kVA starting load on a 10 MVA short-circuit bus gives about 4.8 percent. Limits are set by the utility or the plant (commonly 10 to 15 percent at the motor terminals so torque stays above the load).

**Torque scales with `V^2`:** a 15 percent dip loses about 28 percent of the starting torque.

**Verify:** run a motor-starting dynamic study (for example in ETAP) or measure inrush with a power analyser.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
