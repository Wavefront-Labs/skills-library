---
id: engineering-technology.aerospace-engineering.aerodynamics.thin-airfoil-theory-zero-lift-angle
name: thin-airfoil-theory-zero-lift-angle
category: engineering-technology
field: aerospace-engineering
product: aerodynamics
tags: [aerodynamics, airfoils, airfoil-theory, thin-airfoil-theory, zero-lift-angle, camber-line, lift-slope, anderson]
level: practitioner
status: verified
description: "Apply thin airfoil theory to get lift slope, zero-lift angle and quarter-chord moment from a camber line, and know where the theory stops being valid."
sources:
  - "Anderson, Fundamentals of Aerodynamics (thin airfoil theory chapter)"
  - "Abbott and von Doenhoff, Theory of Wing Sections"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Thin airfoil theory

**Goal:** first-pass section lift and moment from the camber line alone.

## Results (inviscid, incompressible, small angles)
- Lift slope: `cl_alpha = 2*pi` per radian (about 0.110 per degree), independent of camber and thickness.
- `cl = 2*pi*(alpha - alpha_L0)`, with `alpha_L0 = -(1/pi) * integral_0^pi (dz/dx)(cos(theta) - 1) dtheta`, where `x = (c/2)(1 - cos theta)` and z(x) is the camber line.
- Moment about the quarter chord is independent of alpha; the aerodynamic centre is at c/4. Symmetric section: `cm_c/4 = 0`, `alpha_L0 = 0`.
- Fourier form: `dz/dx = alpha - A0 + sum An cos(n theta)`; `cl = pi(2 A0 + A1)`, `cm_c/4 = (pi/4)(A2 - A1)`.

## How to use it
1. Get the camber line from the section definition (see NACA geometry skill) and differentiate it.
2. Evaluate the integral numerically (a few hundred theta points is plenty) to find `alpha_L0`. For a NACA 2412 the answer is -2.08 degrees (numerical integral); check yours against published section data.
3. Use `cl_alpha = 2*pi` for conceptual work; real sections at moderate Reynolds number show roughly 0.09-0.11 per degree because of the boundary layer.
4. Use the measured or XFOIL value for `cl_max`; thin airfoil theory gives no stall.

## Where it fails
- Thickness effects: leading-edge radius and thickness set stall, not the theory.
- Viscous effects reduce lift slope and add pressure drag; the theory predicts zero drag (d'Alembert).
- Above about M 0.7, or with large flap deflections, use compressibility corrections or CFD.

## Verify
- [ ] A symmetric section returns alpha_L0 = 0 and cm_c/4 = 0.
- [ ] Your numerical alpha_L0 for a known NACA section matches published data to a few tenths of a degree.
