---
id: engineering-technology.electrical-engineering.electromagnetics.electrostatics-and-capacitance
name: electrostatics-and-capacitance
category: engineering-technology
field: electrical-engineering
product: electromagnetics
tags: [capacitance-calculation, dielectric-breakdown, electric-field-strength, electrical-engineering, electromagnetics, electrostatics, electrostatics-and-capacitance, gauss-law-applications, insulation-electric-stress]
level: practitioner
status: draft
description: "Compute electric fields and capacitance for common geometries and assess electric stress in insulation."
sources:
  - "https://standards.ieee.org/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Electrostatic field calculations

1. **Gauss's law** for symmetric geometries: `E = Q/(e A)` (parallel plates, uniform), `E = lambda/(2 pi e r)` (line charge), `E = Q/(4 pi e r^2)` (point or sphere).
2. **Capacitance:** parallel plates `C = e0 er A/d`; coaxial cable `C = 2 pi e0 er L / ln(b/a)`; isolated sphere `C = 4 pi e0 a`.
3. **Cable insulation stress:** maximum at the conductor surface `Emax = V/(a ln(b/a))`; the minimum overall stress occurs when `b/a = e` (2.718), a classic result for the optimum conductor-to-sheath ratio.
4. **Example:** 11 kV cable (V phase = 6.35 kV), conductor radius 6 mm and insulation outer radius 11 mm: `Emax = 6350/(0.006 x ln(1.833)) = 1.75 MV/m`, well under the XLPE design stress ranges quoted by manufacturers (check the datasheet).
5. **Layered dielectrics:** stress is higher in the layer with lower permittivity; air gaps and voids lead to partial discharge.
6. **Corona:** onset around 3 MV/m in air at sea level for smooth electrodes (reduced by roughness and altitude); design with radiused electrodes.

**Verify:** compare hand calculations with an electrostatic FEM solution for the same geometry.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
