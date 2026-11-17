---
id: engineering-technology.aerospace-engineering.flight-dynamics-control.control-law-reversion
name: control-law-reversion
category: engineering-technology
field: aerospace-engineering
product: flight-dynamics-control
tags: [control-law-reversion, degraded-modes, alternate-law, direct-law, fly-by-wire, reconfiguration]
level: practitioner
status: draft
description: "Design and verify fly-by-wire control law reversion to degraded modes, including triggers, bumpless transfer, annunciation and handling in each mode."
sources:
  - "FAA 14 CFR 25.671 and 25.1309"
  - "SAE ARP4754A"
  - "SAE ARP4761"
  - "Stevens and Lewis, Aircraft Control and Simulation"
  - "https://www.law.cornell.edu/cfr/text/14/25.671"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Control law reversion

**Goal:** a controlled, annunciated move from normal to degraded control laws after failures.

## Typical structure
- Normal: full protections and command law.
- Degraded (alternate or secondary): some protections lost; handling retained with stability augmentation.
- Direct: stick commands surfaces mechanically-like, with minimal augmentation.
Names differ by manufacturer; the principle is graceful degradation.

## Triggers
Loss of air-data or inertial sensor sets, hydraulic or electrical power, actuator or computer failures, and disagreement between sensors (see sensor-voting-and-redundancy). Each trigger maps to a mode with a defined set of protections and gains.

## Design checks
1. Define each law and what is lost in each reversion.
2. Make transitions bumpless: initialise integrators and gain states so there is no surface jump (transients bounded for the worst case).
3. Add hysteresis or latching to avoid chattering between modes.
4. Annunciate every reversion and its consequences to the crew, with procedures.
5. Evaluate handling in each law across the envelope, including approach and landing, and in the worst-case failure condition (see cooper-harper-handling-ratings, pilot-induced-oscillation).
6. Safety assessment: failure conditions and their probabilities are handled under the system safety process (14 CFR 25.1309, ARP4761 or its 2023 revision ARP4761A; confirm which the certification basis cites) and development assurance under ARP4754A. The authority and the certification basis define the means of compliance.

## Gotchas
- Simultaneous failures can create reversion paths no one designed; use fault-tree and simulation sweeps.
- Gains tuned for the normal law may be unstable in the degraded law with different sensor lag.

## Verify
- [ ] Every reversion path has a simulation showing bounded transient and stable closed loop.
