---
id: engineering-technology.aerospace-engineering.aircraft-structures.spanwise-load-distribution-schrenk
name: spanwise-load-distribution-schrenk
category: engineering-technology
field: aerospace-engineering
product: aircraft-structures
tags: [aircraft-structures, loads, flight-loads, spanwise-loading, schrenk, shear-bending-torque, inertia-relief, wing-loads]
level: practitioner
status: draft
description: "Build wing shear, bending and torque diagrams from a spanwise lift distribution (Schrenk or VLM) with inertia relief from structure and fuel."
sources:
  - "Niu, Airframe Structural Design"
  - "Megson, Aircraft Structures for Engineering Students"
  - "Schrenk, A simple approximation method for obtaining the spanwise lift distribution (NACA TM 948)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Spanwise load distribution and wing loads

**Goal:** shear, bending moment and torque along the wing for a load case.

## Method
1. **Lift distribution:** Schrenk's approximation is the average of the planform chord distribution and an elliptical distribution of the same area; a vortex-lattice or CFD solution gives better results, especially with sweep and twist.
2. **Scale to the load case:** total lift = `n W` (limit factor times weight).
3. **Inertia relief:** subtract wing structural weight, fuel and engine weights distributed along the span, multiplied by `n`.
4. **Integrate:** shear `V(y) = integral from y to tip of (lift - inertia) dy`; bending `M(y) = integral of V dy`; torque from chordwise centre of pressure offset relative to the elastic axis plus pitching moment and inertia offsets.
5. Use discrete stations (spar positions, rib stations) for sizing loads.

## Practice
- Include aero pitching moments and flap loads in the torque.
- Several cases are critical: max positive manoeuvre, max negative, gust, landing, engine failure side loads.
- Aeroelastic correction: flexible wing loads differ from rigid (swept wings shift load).

## Gotchas
- Fuel in wing tanks gives relief, so zero-fuel cases can be critical for bending.
- Sign conventions for torque.

## Verify
- [ ] Shear at the root equals total lift minus total inertia; moment at the tip is zero.
