---
id: engineering-technology.aerospace-engineering.computational-fluid-dynamics.cfd-verification-and-validation
name: cfd-verification-and-validation
category: engineering-technology
field: aerospace-engineering
product: computational-fluid-dynamics
tags: [cfd, verification, validation, v-and-v, mesh-independence, grid-convergence, gci, richardson-extrapolation, observed-order, y-plus, iterative-convergence, residuals, turbulence-modelling, rans, spalart-allmaras, k-omega-sst, asme-v-and-v-20, aiaa-g-077, nasa-tmr, drag-prediction-workshop, uncertainty-quantification, mesh-quality, fluent, openfoam, star-ccm]
level: advanced
status: draft
description: "Make CFD results trustworthy: mesh-independence via Richardson extrapolation and GCI, y+ checks, convergence criteria, model choice and validation vs test."
sources:
  - "Roache, Verification and Validation in Computational Science and Engineering"
  - "Celik et al., Procedure for Estimation and Reporting of Uncertainty Due to Discretization in CFD Applications, ASME Journal of Fluids Engineering (2008)"
  - "ASME V&V 20, Standard for Verification and Validation in Computational Fluid Dynamics and Heat Transfer"
  - "AIAA G-077-1998, Guide for the Verification and Validation of Computational Fluid Dynamics Simulations"
  - "Oberkampf and Roy, Verification and Validation in Scientific Computing"
  - "NASA Langley Turbulence Modeling Resource; AIAA CFD Drag Prediction Workshop series"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# CFD verification and validation — putting an error bar on the number

**Goal:** for every quantity you report (CL, CD, a pressure, a heat flux), state the
numerical uncertainty and how well the model agrees with data, instead of "the mesh
looked fine".

Verification asks *are we solving the equations right* (code and numerics). Validation
asks *are we solving the right equations* (physics vs measurement). Do them in that
order; validating an unconverged solution measures nothing.

## 1. Iterative convergence
- Residuals down at least 3–4 orders from their start (normalised residual levels mean
  different things in different codes, so the drop matters more than the absolute value).
- Every reported quantity flat: change < ~0.1% over the last several hundred iterations.
- Global conservation: mass imbalance < ~0.1% of throughput; energy similar.
- Iterative error should be under a tenth of the discretisation error you will estimate
  next. If a steady run limit-cycles, the physics may be unsteady: run transient and
  average over enough periods, then check the averages converged too.

## 2. Mesh quality and near-wall resolution
- Code-specific metrics: e.g. Fluent minimum orthogonal quality > 0.1, max skewness
  < 0.95; growth ratio ≤ 1.2 in boundary layers.
- **y+ by approach:** wall-resolved low-Re models need y+ ≈ 1; wall functions need the
  first cell in roughly 30–300. Avoid first cells in the buffer layer (5–30) unless the
  code has an explicitly y+-insensitive wall treatment, and say which one you used.

## 3. Grid convergence study (Richardson + GCI)
Build three systematically refined grids (same topology, refine everywhere, including
boundary-layer spacing). Grid refinement ratio `r = h_coarse/h_fine ≥ 1.3`; in 3D,
`h = (V/N)^(1/3)`.
```python
import math
def gci(f1, f2, f3, r21, r32, Fs=1.25):
    """f1 = fine, f3 = coarse. Returns observed order p, extrapolated value, GCI_fine."""
    e32, e21 = f3 - f2, f2 - f1
    s = math.copysign(1, e32 / e21)
    p = abs(math.log(abs(e32 / e21))) / math.log(r21)       # first guess
    for _ in range(50):                                     # fixed-point for unequal r
        q = math.log((r21**p - s) / (r32**p - s))
        p = abs(math.log(abs(e32 / e21)) + q) / math.log(r21)
    f_ext = (r21**p * f1 - f2) / (r21**p - 1)
    gci_fine = Fs * abs((f1 - f2) / f1) / (r21**p - 1)
    return p, f_ext, gci_fine
```
- Compare observed p to the scheme's formal order (~2 for second-order). p far above or
  below means you are **not in the asymptotic range**: refine further, do not report the GCI
  as if it were valid.
- **Oscillatory convergence** (sign of e32/e21 negative) breaks the method; report the
  oscillation band as the uncertainty instead.
- Typical aim: GCI on CD of a few percent; drag converges slower than lift. Drag counts
  (1 count = 0.0001) are the usual currency in external aero, and DPW-style studies show
  spreads of tens of counts between codes and grids, so do not over-claim.

## 4. Model-form judgement (before blaming the mesh)
- Attached external flow: SA or SST both fine; SA often slightly better for attached
  wings, SST for adverse pressure gradient and onset of separation.
- Laminar runs/low Re (< ~1e6): fully turbulent RANS overpredicts drag; use a transition
  model or fixed transition matching the test.
- Massive separation, bluff bodies, high-lift near CLmax: RANS is unreliable; consider
  hybrid RANS-LES (DES/DDES) and expect larger uncertainty.
- Check your implementation against a standard case first: NASA TMR flat plate and
  NACA 0012 cases have published reference results for SA and SST.

## 5. Validation against data
- Match the test conditions, not the nominal ones: tunnel Re, Mach, transition trips,
  wall interference/blockage corrections, support/sting, measured alpha.
- ASME V&V 20 style: comparison error `E = S − D`; validation uncertainty
  `u_val = sqrt(u_num² + u_input² + u_D²)`. If `|E| < u_val`, the model error is within the
  noise of the comparison; if `|E| >> u_val`, the model has a real deficiency of about E.
- Compare distributions (Cp, Cf, velocity profiles), not just integrated forces; right
  force from wrong distribution is luck.

## Gotchas
- Refining only the surface mesh and not the boundary layer or wake is not a grid study.
- Changing turbulence model, domain size and mesh at the same time hides which one moved
  the answer. Change one thing.
- Domain size is its own convergence study for lifting cases.

## Verify
- [ ] Iterative convergence criteria met and reported for every quantity of interest.
- [ ] y+ distribution consistent with the chosen wall treatment.
- [ ] Three-grid study shows observed order near formal order; GCI reported.
- [ ] Turbulence/transition model choice justified for this flow regime.
- [ ] Code and model checked on a standard benchmark case.
- [ ] Validation comparison includes uncertainty on both simulation and data.
