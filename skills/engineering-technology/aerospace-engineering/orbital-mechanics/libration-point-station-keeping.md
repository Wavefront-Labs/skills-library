---
id: engineering-technology.aerospace-engineering.orbital-mechanics.libration-point-station-keeping
name: libration-point-station-keeping
category: engineering-technology
field: aerospace-engineering
product: orbital-mechanics
tags: [libration-station-keeping, station-keeping, l2, halo-orbit-control, three-body-dynamics]
level: practitioner
status: gated
description: "Plan station keeping for L1 and L2 orbits: instability time scale, manoeuvre cadence, targeting strategies and delta-v budget."
sources:
  - "Koon, Lo, Marsden and Ross, Dynamical Systems, the Three-Body Problem and Space Mission Design"
  - "Vallado, Fundamentals of Astrodynamics and Applications"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Libration point station keeping

**Goal:** hold the spacecraft near the reference orbit with minimum propellant.

## Why it is needed
Collinear libration point orbits are unstable: small deviations grow exponentially with an e-folding time on the order of weeks for Sun-Earth L1 and L2 (linearised CR3BP about the L1 point gives an unstable eigenvalue 2.53 per unit time, an e-folding time of about 23 days, computed) (the unstable eigenvalue of the monodromy matrix sets it; compute it for your orbit). Errors from orbit determination, manoeuvre execution and unmodelled forces (SRP) grow and must be corrected.

## Strategies
- **Target to a reference**: periodic small corrections to return to the nominal orbit.
- **Manifold-based (Floquet) control**: remove the unstable-eigenvector component of the deviation, which leaves the stable and centre motion alone.
- **Cadence**: small burns every few weeks; for Sun-Earth L2 observatories the typical cadence is reported as roughly every three weeks with annual delta-v budgets of metres per second (confirm for any particular mission (gated: unconfirmed, source is paywalled or blocked)).

## Procedure
1. Determine the orbit with tracking data and a covariance.
2. Compute the unstable component of the deviation by projecting onto the monodromy eigenvectors, or run a targeting problem for the next several revolutions.
3. Compute the manoeuvre; check it against thruster and attitude constraints (for example sun-shield orientation).
4. Execute, determine the orbit again, and update.
5. Provide a budget with margin for execution error and missed manoeuvre opportunities (a skipped manoeuvre increases the next).

## Gotchas
- Station keeping requires accurate SRP modelling, because SRP uncertainty is a primary error source.
- Lower-cost strategies exist for orbit amplitude growth: keeping a large amplitude can be easier than a small one.

## Verify
- [ ] A Monte Carlo of navigation and execution errors shows the delta-v budget met at the chosen confidence.
