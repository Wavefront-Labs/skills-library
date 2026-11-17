---
id: engineering-technology.aerospace-engineering.aerodynamics.airfoil-selection-reynolds-cl
name: airfoil-selection-reynolds-cl
category: engineering-technology
field: aerospace-engineering
product: aerodynamics
tags: [aerodynamics, airfoils, airfoil-selection, reynolds-number, design-cl, thickness-ratio, laminar-flow-airfoil, conceptual-design]
level: practitioner
status: verified
description: "Choose an airfoil by working out operating Reynolds number, design lift coefficient, thickness and pitching-moment needs before comparing candidate polars."
sources:
  - "Raymer, Aircraft Design: A Conceptual Approach"
  - "Abbott and von Doenhoff, Theory of Wing Sections"
  - "Selig, UIUC low-speed airfoil tests"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Airfoil selection

**Goal:** a short list of sections justified by requirements.

## 1. Fix the operating point
- Reynolds number `Re = rho V c / mu`. At ISA sea level `rho/mu` is about 68,500 per m/s per m, so `Re ~= 6.85e4 x V[m/s] x c[m]`. A 1.5 m chord at 60 m/s is about 6.2e6 (rho 1.225, mu 1.789e-5 gives 68,460).
- Section design `cl`: roughly `CL_cruise` divided by the wing efficiency of the planform (about 1 for unswept, corrected by `cos^2` sweep for swept wings), then check at climb and loiter.
- Required `cl_max` from stall speed (see CLmax sizing skill).

## 2. Constraints
- Thickness: structural depth (wing weight falls with t/c), fuel volume, and wave drag on high-speed aircraft.
- Pitching moment: large nose-down `cm` costs trim drag and tail load.
- Leading-edge radius: sets stall type (thin sections stall abruptly from the leading edge, thicker ones more gently).
- Roughness sensitivity: laminar-flow sections lose their advantage when contaminated by insects, rain or paint.

## 3. Compare polars
1. Pull candidate polars at your Re (wind tunnel data such as the UIUC low-speed database for small vehicles, NACA reports, or XFOIL).
2. Overlay `cd` vs `cl`, `cl` vs alpha and `cm` vs alpha at the operating Re, not a different Re.
3. Prefer the section whose low-drag bucket brackets the cruise `cl` and whose stall is benign.

## Gotchas
- Published polars at 3e6 or 6e6 do not transfer to a small UAV at 2e5.
- A wide drag bucket needs surface quality you may not have in service.
- Sections for transonic cruise need a separate check on Mdd; see the supercritical airfoil skill.

## Verify
- [ ] Re, design cl, t/c and cm requirement are written down with numbers.
- [ ] Polars compared are from the same Re (within a factor of ~2) and Ncrit.
