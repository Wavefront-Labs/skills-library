---
id: engineering-technology.aerospace-engineering.aerodynamics.lifting-line-span-efficiency
name: lifting-line-span-efficiency
category: engineering-technology
field: aerospace-engineering
product: aerodynamics
tags: [aerodynamics, finite-wing, lifting-surfaces, lifting-line, span-efficiency, induced-drag, elliptic-loading, prandtl]
level: practitioner
status: verified
description: "Use Prandtl lifting-line theory to estimate finite-wing lift slope, induced drag and span efficiency, including the Fourier-series solution and its limits."
sources:
  - "Anderson, Fundamentals of Aerodynamics (finite wings)"
  - "Bertin and Cummings, Aerodynamics for Engineers"
  - "Raymer, Aircraft Design"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Lifting-line theory

**Goal:** CL, induced drag and spanwise loading of an unswept, moderate-to-high-aspect-ratio wing.

## Key results
- Elliptic loading minimises induced drag: `CDi = CL^2/(pi AR)`; downwash is constant along the span.
- General wing: `CDi = CL^2/(pi AR e)` with `e = 1/(1 + delta)`, `delta = sum_{n>=2} n (An/A1)^2` from the Fourier series of circulation, `Gamma(theta) = 2 b V sum An sin(n theta)`.
- Finite-wing lift slope (elliptic, small angles): `a = a0 / (1 + a0/(pi AR))`, where a0 is the section slope (2 pi per radian). With an e other than 1, replace pi AR by pi AR e.
- Optimum taper for an unswept straight wing is about 0.3-0.5 (a 100-station lifting-line solve at AR 6 gives e = 0.988, 0.991, 0.990 at taper 0.5, 0.4, 0.3); an unswept rectangular wing has e of about 0.95 at AR 6 and 0.94 at AR 8 (same solve), and a lift slope of 4.53 per radian at AR 6 against 4.71 from the elliptic formula.

## Procedure
1. Divide the half span into N stations in theta (`y = -(b/2) cos theta`), N of 20-50.
2. Write the lifting-line equation at each station using local chord, section lift slope and zero-lift angle (which includes geometric twist).
3. Solve the linear system for An; get CL from A1 (`CL = A1 pi AR`), `e` from the sum.
4. Output the spanwise `cl` distribution and compare to section `cl_max` to see where stall starts.

## Limits
- Poor for sweep above about 20 degrees, low aspect ratio (below 4), or when sections stall; use a vortex-lattice method or CFD instead.
- No compressibility; apply Prandtl-Glauert only for moderate Mach.

## Verify
- [ ] Rectangular wing AR 6: e is about 0.95 and CL slope about 4.5 per radian, below the 2D value.
- [ ] Setting an elliptic chord distribution returns e = 1 within numerical error.
