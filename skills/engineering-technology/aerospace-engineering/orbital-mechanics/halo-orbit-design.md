---
id: engineering-technology.aerospace-engineering.orbital-mechanics.halo-orbit-design
name: halo-orbit-design
category: engineering-technology
field: aerospace-engineering
product: orbital-mechanics
tags: [halo-orbits, libration-point-orbits, differential-correction, crtbp, three-body-dynamics]
level: practitioner
status: verified
description: "Construct halo orbits about L1 or L2 in the circular restricted three-body problem from an analytic seed and differential correction, with stability notes."
sources:
  - "Howell, three-dimensional periodic halo orbits (Celestial Mechanics literature)"
  - "Vallado, Fundamentals of Astrodynamics and Applications"
  - "Koon, Lo, Marsden and Ross, Dynamical Systems, the Three-Body Problem and Space Mission Design"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Halo orbits

**Goal:** a periodic three-dimensional orbit near a collinear libration point.

## Dynamics
CRTBP in the rotating frame, mass parameter `mu = m2/(m1+m2)`; equations of motion with potential `U = (x^2 + y^2)/2 + (1-mu)/r1 + mu/r2`.

## Procedure
1. Locate the libration point (see lagrange-point-locations).
2. Seed: a third-order analytic (Richardson-type) approximation for a chosen out-of-plane amplitude `Az`, or take a nearby orbit from continuation.
3. Differential correction: halo orbits are symmetric about the `x-z` plane; integrate from an initial state on that plane (`y = 0`, `vx = vz = 0`) until the next plane crossing, and adjust the initial `x`, `vy` (or `z`, `vy`) so the crossing velocity components `vx` and `vz` vanish (single shooting with the state transition matrix).
4. Continue in `Az` to build the family (natural-parameter continuation).
5. Check: period, Jacobi constant (conserved), and the monodromy matrix eigenvalues: halo orbits near L1 and L2 are unstable with one real unstable eigenvalue, so station keeping is needed (see libration-point-station-keeping).
6. Transition to an ephemeris model (add Sun, Moon, perturbations) with multiple shooting for mission design.

## Examples
Sun-Earth L2 halo orbits (large amplitudes of the order of hundreds of thousands of kilometres) are used by space observatories; periods are about half a year (NASA states Webb's L2 orbit takes about 6 months and is similar in size to the Moon's orbit; the linearised Sun-Earth L2 in-plane period is 178 days, computed).

## Gotchas
- Shooting is sensitive: use short arcs or multiple shooting for long periods.
- The CRTBP orbit does not exist in the real ephemeris; the corrected orbit is quasi-periodic.

## Verify
- [ ] The corrected initial state after one period returns to itself within the tolerance and the Jacobi constant is constant to integrator precision.
