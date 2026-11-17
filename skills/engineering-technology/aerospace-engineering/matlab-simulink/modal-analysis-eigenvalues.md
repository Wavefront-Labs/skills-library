---
id: engineering-technology.aerospace-engineering.matlab-simulink.modal-analysis-eigenvalues
name: modal-analysis-eigenvalues
category: engineering-technology
field: aerospace-engineering
product: matlab-simulink
tags: [matlab, simulink, trim-linearization, modal-analysis, eig, damp, short-period, phugoid, dutch-roll, eigenvectors]
level: practitioner
status: docs-checked
description: "Interpret flight-dynamic modes from eigenvalues and eigenvectors of A, compute frequency and damping with damp, and identify which states participate."
sources:
  - "https://www.mathworks.com/help/control/ref/dynamicsystem.damp.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Modal analysis with eig and damp

**Goal:** identify flight modes and judge them against criteria.

## Commands
```matlab
[wn, zeta, p] = damp(sys);      % natural frequency, damping ratio, poles (same order, ascending wn)
[V, D] = eig(sys.A);            % eigenvectors and eigenvalues
```
For each complex pair `lambda = -zeta*wn +/- j*wn*sqrt(1-zeta^2)`.

## Identification
- Longitudinal: a fast pair is the short period (states alpha and q dominate); a slow lightly damped pair is the phugoid (V and theta).
- Lateral: dutch roll (oscillatory, sideslip and yaw rate), roll subsidence (real, fast), spiral (real, slow, can be unstable).
- Use `abs(V(:,k))` normalised to see participation of each state in each mode.

## Practice
1. Normalise eigenvectors to compare state participation.
2. Plot `pzmap(sys)` (listed beside `eig` on the damp page) and compare against handling-quality limits (see handling-qualities skills).
3. Compare modes across trim points to see trends with speed and altitude.

## Gotchas
- Poorly scaled states (m/s vs rad) hide participation: scale before reading eigenvectors.
- Modes of actuators and sensors mix with airframe modes in a full model.

## Verify
- [ ] The short-period frequency agrees with a hand estimate from the aircraft's pitch derivatives.

## Checked
2026-11-01. Confirmed on the MathWorks damp page: `[wn,zeta,p] = damp(sys)`, outputs and their ordering, eig and pzmap listed under See Also. Removed: the textbook source and the typical frequency and period figures (not on the page read). The eigenvalue formula follows from the second-order pole definition.
Method: documentation only; no commands were run.
