---
id: engineering-technology.automotive-vehicle-engineering.crash-safety.crash-model-correlation-and-validation
name: crash-model-correlation-and-validation
category: engineering-technology
field: automotive-vehicle-engineering
product: crash-safety
tags: [crash-correlation, model-validation, cora, iso-ts-18571, correlation, validation, energy-balance, verification, crash-cae, sled-test, component-test]
level: practitioner
status: gated
description: "Correlate a crash model to test: build-up from material to full-vehicle level, signal-comparison metrics such as CORA and ISO/TS 18571, and energy and sanity checks."
sources:
  - "LS-DYNA user manual contents (keyword manual volumes I-III; vendor documentation at https://www.ansys.com)"
  - "Kramer, Passive Safety of Vehicles (chapter list)"
  - "ISO/TS 18571 (objective rating metric for non-ambiguous signals; confirm edition); CORA correlation analysis method (published by the PDB/Partnership for Dummy Technology and Biomechanics)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Crash model correlation and validation

Metric names, ISO/TS 18571 scope and energy thresholds are unconfirmed (gated: unconfirmed, source is paywalled or blocked).

## 1. Build up in levels
1. **Material:** tensile and rate tests reproduced (see material cards).
2. **Joint:** coupon tests reproduced (see joint modelling).
3. **Component:** crush, bending, impact tests of tubes, rails, doors, sills, pillars.
4. **Subsystem:** front end, side structure, seat, restraint sled test.
5. **Full vehicle:** barrier or pole test.
Do not skip levels: errors found at the full vehicle are expensive to attribute.

## 2. Verification (is the model solving correctly)
Total energy conserved (kinetic plus internal plus contact plus hourglass and sliding energies); hourglass energy less than about five percent of internal; added mass small; contact energy small; initial penetrations zero; mass and centre of gravity match.

## 3. Validation (does it match test)
Compare, with filtered signals at the same channel classes as the test:
- Vehicle deceleration pulse (accelerometers at sills or tunnel), and velocity and displacement from integration.
- Barrier forces (load cells).
- Intrusion measurements (toe pan, steering column, door), deformation lengths and fold patterns (photos, 3-D scans).
- Occupant: dummy head, chest, pelvis signals if dummy model included.
Use quantitative metrics, not only visual overlays: CORA (corridor and cross-correlation rating) and ISO/TS 18571 (rating by corridor, phase, magnitude and slope) give a score from 0 to 1; define acceptable scores per signal type up front. Compare peak and timing; the pulse phase matters for restraint tuning.

## 4. Tuning rules
Tune the parameters that are uncertain and physically adjustable (weld failure, material rate sensitivity, friction coefficient, contact stiffness), not mass or geometry. Record each change; avoid "fitting" one test: validate against a second configuration (other speed, overlap, load case).

## 5. Predictive confidence
Run mesh-size and parameter sensitivity; check that the test is repeatable (test-to-test scatter of identical vehicles may be several percent in peak loads). State a model's validated envelope.

## Verify
- [ ] Verification energy checks pass.
- [ ] Metrics and acceptance thresholds agreed in advance.
- [ ] Tuned parameters recorded with justification.
- [ ] Second configuration used for blind validation.
