---
id: engineering-technology.aerospace-engineering.orbital-mechanics.lagrange-point-locations
name: lagrange-point-locations
category: engineering-technology
field: aerospace-engineering
product: orbital-mechanics
tags: [orbital-mechanics, three-body-dynamics, cr3bp, lagrange-points, lagrange-point-locations, libration-points, l1-l2, restricted-three-body]
level: practitioner
status: verified
description: "Find the five Lagrange points of the circular restricted three-body problem and judge their stability and use for missions such as L1 and L2 halo orbits."
sources:
  - "Curtis, Orbital Mechanics for Engineering Students"
  - "Koon, Lo, Marsden and Ross, Dynamical Systems the Three-Body Problem and Space Mission Design"
  - "Vallado"
  - "NASA Earth Fact Sheet, https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html (Sun-Earth distance)"
  - "Recomputed in Python (scipy brentq on the collinear equation)"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Lagrange point locations

**Goal:** equilibrium positions in the rotating frame of the circular restricted three-body problem (CR3BP).

## Locations
With mass ratio `mu = m2/(m1+m2)`, normalised distance between primaries 1:
- L1, L2, L3 are collinear points on the line through the primaries: roots of the collinear quintic for the position `x`.
- L4 and L5 form equilateral triangles with the primaries.
- Approximation for small `mu`: L1 and L2 lie about `r_H = a (m2/(3 m1))^(1/3)` from the smaller body (Hill radius): Sun-Earth L1 and L2 are about 1.5 million km from Earth.

## Stability
L1, L2, L3 are unstable (exponential divergence, so station-keeping is needed); L4 and L5 are linearly stable if `m1/m2 > 24.96` (Routh criterion) - holds for Sun-Earth and Earth-Moon in the CR3BP, though the Sun strongly perturbs Earth-Moon L4 and L5 in reality.

## Procedure
1. Solve the collinear equation by Newton from starting guesses (for L1: `x = 1 - mu - (mu/3)^(1/3)`).
2. Nondimensionalise by distance and angular rate; compute the Jacobi constant at each point.
3. Use halo or Lissajous orbits around L1 or L2 for missions; the unstable manifold guides transfer design.

## Gotchas
- Real ephemeris dynamics add perturbations and require station-keeping.
- Distances: Earth-Moon L1 is about 58,000 km and L2 about 64,500 km from the Moon (solved from the CR3BP collinear equation, mass ratio 0.01215: 58,019 and 64,515 km; Sun-Earth, mass ratio 3.00348e-6: L1 1.4916 and L2 1.5015 million km from Earth; Hill-radius approximation 1.4966 million km). Routh limit recomputed as 24.96 (27 mu (1 - mu) < 1).

## Verify
- [ ] Newton solution satisfies the force balance in the rotating frame to numerical precision.
