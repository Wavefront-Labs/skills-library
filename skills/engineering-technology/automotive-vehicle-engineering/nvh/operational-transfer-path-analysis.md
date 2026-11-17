---
id: engineering-technology.automotive-vehicle-engineering.nvh.operational-transfer-path-analysis
name: operational-transfer-path-analysis
category: engineering-technology
field: automotive-vehicle-engineering
product: nvh
tags: [operational-tpa, otpa, matrix-inversion, indicator-sensors, svd, transfer-path-analysis-fast]
level: practitioner
status: gated
description: "Use operational TPA with matrix inversion: reference sensors, FRF measurement, conditioning with SVD truncation and over-determination, with its accuracy limits."
sources:
  - "de Klerk and Ossipov, Operational transfer path analysis: theory, guidelines and tire noise application, Mechanical Systems and Signal Processing 24 (2010), doi:10.1016/j.ymssp.2010.05.009"
  - "Harrison, Vehicle Refinement"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Operational TPA

1. Idea: instead of measuring mount stiffness, estimate path forces from vibration measured at indicator sensors near each interface, using the inverse of the FRF matrix: `F = H^+ * a_indicators`.
2. Measurements: operational runs (rpm run-up, road), plus a roving hammer or shaker FRF measurement from path points to indicator sensors (and target).
3. Indicator sensors: choose a number larger than the number of paths (typically 1.5-3 times, to over-determine (gated: unconfirmed, source is paywalled or blocked)) at locations around the body-side of each interface.
4. Inversion and conditioning: use SVD with truncation or regularisation (Tikhonov) to avoid noise amplification; check singular values and condition number.
5. Contributions: forces times the path-to-target FRFs, summed; compare to the measured target for validation.
6. Strengths: faster, no need to disconnect or measure mount stiffness; good for noise-source ranking in whole vehicle.
7. Limits: cross-coupling between nearby paths, less accurate absolute values; use classical TPA for design targets when accuracy matters.
8. Check with coherence and with a path-blocking test or vehicle change.

**Gotchas:** ill-conditioned matrices; insufficient indicators.

## Verify
- [ ] Reconstructed response from indicators matches the measured within a few dB.
- [ ] Condition number and truncation recorded.
