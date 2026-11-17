---
id: engineering-technology.aerospace-engineering.aircraft-structures.fe-model-test-correlation
name: fe-model-test-correlation
category: engineering-technology
field: aerospace-engineering
product: aircraft-structures
tags: [test-correlation, model-correlation, modal-assurance-criterion, cross-orthogonality, model-updating, structural-fem]
level: practitioner
status: draft
description: "Correlate a finite element model with test data using frequency error, MAC and cross-orthogonality, then update stiffness and mass with documented limits."
sources:
  - "Ewins, Modal Testing: Theory, Practice and Application"
  - "NASA GEVS (GSFC-STD-7000)"
  - "Niu, Airframe Structural Design"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Test correlation of FE models

**Goal:** show the model predicts measured modes and static behaviour well enough for its use.

## Metrics
- Frequency error per mode: `(f_fem - f_test) / f_test`.
- Modal Assurance Criterion: `MAC_ij = |phi_test_i . phi_fem_j|^2 / ((phi_test_i . phi_test_i)(phi_fem_j . phi_fem_j))`; 1 means identical shape. A diagonal value above about 0.9 is a common correlation target.
- Cross-orthogonality (test modes against model mass matrix) uses mass weighting: diagonals near 1 and off-diagonals small; spaceflight programmes often quote diagonals at least 0.9 and off-diagonals at most 0.1, but check what your programme or customer document requires.

## Procedure
1. Choose test sensor locations from a pre-test analysis so important modes are observable and distinct.
2. Reduce the FE model to test degrees of freedom (Guyan or SEREP) for the comparison.
3. Pair modes by MAC, not by order number.
4. Review the largest frequency errors; adjust uncertain parameters (joint stiffness, boundary stiffness, non-structural mass, material modulus) within physically plausible ranges.
5. Re-run; stop when criteria are met without physically absurd parameters.
6. Document the final model, the adjusted parameters and the remaining discrepancy.

## Gotchas
- Fitting frequencies by changing the wrong parameter hides a modelling error.
- Test boundary conditions (suspension, fixture) must be in the model.
- Updating on a few modes does not guarantee higher modes.

## Verify
- [ ] The updated model reproduces a test case not used in the update.
