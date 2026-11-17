---
id: engineering-technology.electrical-engineering.protection-coordination.breaker-failure-and-reclosing
name: breaker-failure-and-reclosing
category: engineering-technology
field: electrical-engineering
product: protection-coordination
tags: [50bf, 79, auto-reclose, breaker-failure, breaker-failure-and-reclosing, breaker-failure-timing, electrical-engineering, protection-coordination, reclose-dead-time]
level: practitioner
status: draft
description: "Set breaker failure timers and auto-reclosing dead times and lockout logic."
sources:
  - "https://standards.ieee.org/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Breaker failure (50BF) and auto-reclosing (79)

- **Breaker failure timer:** `T_bf = breaker clearing time + relay reset time + safety margin (about 1 to 2 cycles)`; initiated by a protection trip and a current detector; trips adjacent breakers via a lockout relay. Include retrip option.
- **Current detector** set below the minimum fault current but above load (check for CT remanence and slow decay of DC offset).
- **Reclosing:** overhead lines have mostly transient faults; dead time must exceed the arc deionisation time (increases with voltage) and the breaker reset time; single-pole tripping with 1 s dead time is common on EHV, high-speed three-phase reclose on HV with synchronism check; distribution reclosers use a sequence like 2 fast + 2 delayed operations before lockout.
- Block reclose on cable sections, transformer faults, breaker failure and busbar protection operation.
- Coordinate recloser fast curves with fuses (fuse-saving or fuse-blowing).

**Verify:** simulate the sequence in a relay test with a transient fault, and verify lockout after a persistent fault.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
