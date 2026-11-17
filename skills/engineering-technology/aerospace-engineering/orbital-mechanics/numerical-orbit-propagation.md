---
id: engineering-technology.aerospace-engineering.orbital-mechanics.numerical-orbit-propagation
name: numerical-orbit-propagation
category: engineering-technology
field: aerospace-engineering
product: orbital-mechanics
tags: [orbit-propagation, cowell-method, numerical-integration, ode113, perturbations, two-body-motion]
level: practitioner
status: draft
description: "Propagate orbits numerically (Cowell) with perturbation accelerations, a variable-step integrator, tight tolerances and energy-based checks."
sources:
  - "Vallado, Fundamentals of Astrodynamics and Applications"
  - "Montenbruck and Gill, Satellite Orbits"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Orbit propagation

**Goal:** accurate trajectory over the interval of interest.

## Cowell method
State `y = [r; v]`, `dy/dt = [v; a]`, with `a = -mu r/|r|^3 + sum(perturbations)`.
Perturbations: non-spherical gravity (`J2` and higher harmonics), atmospheric drag, third-body gravity (Sun, Moon), solar radiation pressure, thrust.

## Procedure
1. Choose frame (inertial, e.g. GCRF) and units (km and s, or non-dimensional).
2. Pick an integrator: a high-order variable-step Runge-Kutta (Dormand-Prince 8(5,3)) or a multistep Adams method (MATLAB `ode113`) for smooth orbits; `ode45` works with tight tolerances but is less efficient.
3. Set tolerances: relative `1e-10` to `1e-12` for precise work; absolute scaled to units.
4. Add event detection for apsides, eclipses, ground station passes (see ode-event-detection).
5. Output at fixed times by dense output, not by forcing the step.

## Alternatives
- Analytic or semi-analytic (SGP4, see tle-and-sgp4-propagation) for catalogue-level accuracy.
- Encke's method integrates the deviation from a reference Kepler orbit.
- Special perturbation by equinoctial elements for long, near-circular arcs.

## Checks
1. Run two-body only and compare energy and angular momentum drift (should be near the tolerance).
2. Tighten tolerance by 10x; the result should not change beyond your accuracy needs.
3. Compare the closed-form Kepler propagation for one orbit.

## Gotchas
- Drag models need density from a model that depends on solar and geomagnetic activity; their errors dominate over integration error for LEO.
- Rounding error grows over long propagations; consider extended precision for very long runs.

## Verify
- [ ] After one period of a two-body orbit the state returns to the initial state within the tolerance.
