---
id: engineering-technology.aerospace-engineering.aircraft-structures.ground-vibration-testing
name: ground-vibration-testing
category: engineering-technology
field: aerospace-engineering
product: aircraft-structures
tags: [ground-vibration-test, gvt, modal-testing, flutter-clearance, experimental-modal-analysis, structural-fem]
level: practitioner
status: draft
description: "Plan and run an aircraft ground vibration test to measure modes, damping and generalised mass for flutter model validation, with suspension and excitation choices."
sources:
  - "Ewins, Modal Testing: Theory, Practice and Application"
  - "FAA 14 CFR 25.629"
  - "EASA CS-25"
  - "https://www.law.cornell.edu/cfr/text/14/25.629"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Ground vibration testing

**Goal:** measured modal frequencies, shapes, damping and generalised masses of the full aircraft to validate the structural dynamic model used for flutter.

## Set-up
1. Support the aircraft on soft supports (air springs, bungees) so rigid-body modes lie well below the lowest elastic mode. A ratio of several to one is the usual aim; state your criterion.
2. Configure mass cases: fuel and payload states that are critical for flutter, and structural modifications.
3. Instrument with accelerometers on a grid that distinguishes control surfaces, engines, tips and fuselage; plan sensors from the pre-test model.

## Excitation
- Electrodynamic shakers at wing, tail and fuselage, with multiple-input random, stepped-sine or burst-random signals; use phase-resonance (normal mode tuning) or phase-separation methods.
- Impact hammers for quick surveys.
- Check linearity: repeat at different force levels, because friction and free-play in control systems change frequency and damping.

## Outputs
- Natural frequencies, mode shapes, damping ratios and generalised mass for each mode.
- Control-surface free-play and actuator stiffness measured separately.
- Results feed the correlation of the flutter model (see fe-model-test-correlation).

## Gotchas
- Control-surface rotation modes depend strongly on actuator impedance; test with the system in the flight-representative condition.
- Closely spaced modes need good spatial resolution to separate them.
- The regulation (14 CFR 25.629, CS-25) sets what flutter substantiation is required; GVT is one input.

## Verify
- [ ] Reciprocity checks pass (response at B from force at A equals the opposite).
