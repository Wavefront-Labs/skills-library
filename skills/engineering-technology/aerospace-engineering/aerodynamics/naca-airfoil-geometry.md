---
id: engineering-technology.aerospace-engineering.aerodynamics.naca-airfoil-geometry
name: naca-airfoil-geometry
category: engineering-technology
field: aerospace-engineering
product: aerodynamics
tags: [aerodynamics, airfoils, naca-airfoils, naca-4-digit, naca-5-digit, airfoil-coordinates, camber, thickness-distribution]
level: practitioner
status: verified
description: "Decode NACA 4- and 5-digit airfoil designations and generate their coordinates correctly, including the trailing-edge closure gotcha."
sources:
  - "Abbott and von Doenhoff, Theory of Wing Sections"
  - "Jacobs, Ward and Pinkerton, NACA Report 460"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# NACA 4- and 5-digit airfoil geometry

**Goal:** know what the digits mean and produce usable coordinates.

## Decoding
- **4-digit MPXX:** M = max camber in percent chord, P = its position in tenths of chord, XX = max thickness in percent chord. NACA 2412: 2% camber at 40% chord, 12% thick. NACA 0012 is symmetric.
- **5-digit LPQXX:** first digit L: design lift coefficient = 3/20 x L (so 2 gives 0.3); the next two digits PQ give twice the position of maximum camber in percent chord (30 means 15%); XX is thickness. NACA 23012: design CL 0.3, max camber at 15% chord, 12% thick. Q=0 is the standard camber line, Q=1 the reflexed one.

## Thickness distribution (4-digit, t as fraction of chord)
`yt = 5 t (0.2969 sqrt(x) - 0.1260 x - 0.3516 x^2 + 0.2843 x^3 - 0.1015 x^4)`
The last coefficient is -0.1015 for the original open trailing edge and -0.1036 for a closed (zero-thickness) trailing edge.

## Building coordinates
1. Use cosine spacing in x: `x = 0.5(1 - cos(beta))` for beta from 0 to pi. This clusters points at the leading edge.
2. Camber line for 4-digit: forward of P, `yc = (m/p^2)(2 p x - x^2)`; aft, `yc = (m/(1-p)^2)((1-2p) + 2 p x - x^2)`, with m and p as fractions.
3. Offset the thickness perpendicular to the camber line: `xu = x - yt sin(theta)`, `yu = yc + yt cos(theta)`, with `theta = atan(dyc/dx)`; lower surface with signs flipped.

## Gotchas
- Open trailing edge (-0.1015) leaves a finite thickness that some panel and CFD tools reject; use the closed variant or add a blunt-trailing-edge treatment deliberately.
- Several tools take the points ordered upper surface trailing edge to leading edge to lower surface trailing edge; check the format.
- Scale before use: coordinates are for unit chord.

## Verify
- [ ] Plotted section shows expected max thickness (x about 0.30 for 4-digit) and camber location.
- [ ] Leading-edge radius is about `1.1019 t^2` (4-digit); the points near x=0 show it.
