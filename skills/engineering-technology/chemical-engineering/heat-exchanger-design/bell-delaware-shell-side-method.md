---
id: engineering-technology.chemical-engineering.heat-exchanger-design.bell-delaware-shell-side-method
name: bell-delaware-shell-side-method
category: engineering-technology
field: chemical-engineering
product: heat-exchanger-design
tags: [chemical-engineering, heat-exchanger-design, hx-shell-and-tube-selection, bell-delaware-shell-side-method, bell-delaware, shell-side, j-factors, leakage-streams, bypass-stream, baffle-correction, shell-side-pressure-drop, taborek]
level: advanced
status: gated
description: "Apply the Bell-Delaware method for shell-side heat transfer and pressure drop with correction factors Jc, Jl, Jb, Js, Jr and the typical effect of leakage and bypass streams."
sources:
  - "Kern Process Heat Transfer, Perry Handbook heat transfer section, TEMA Standards, Heat Exchanger Design Handbook (HEDH), Kemp Pinch Analysis and Process Integration, Smith Chemical Process Design and Integration"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bell-Delaware shell-side method

**Goal:** a shell-side coefficient and pressure drop that account for leakage and bypass streams, not just ideal crossflow.

## Idea
The typical J-factor ranges below are rules of thumb (gated: unconfirmed, source is paywalled or blocked); confirm against Taborek (HEDH) or a rating program.
The ideal tube-bank crossflow coefficient h_ideal (from the tube bank correlation with Colburn j-factor versus Reynolds number for the layout) is corrected:
h_o = h_ideal Jc Jl Jb Js Jr
- **Jc**: baffle window flow and cut (about 1 for 25% cut; larger cuts raise it a bit).
- **Jl**: baffle leakage (tube-to-baffle and baffle-to-shell clearances); typically 0.7 to 0.9.
- **Jb**: bundle bypass (between bundle and shell); sealing strips raise it (about 0.7 to 0.9).
- **Js**: unequal baffle spacing at inlet and outlet.
- **Jr**: laminar flow correction (Re below about 100).
The product of J factors is commonly in the range 0.6 to 0.8 for a good design; a much lower product signals a poor geometry (large clearances, no sealing strips).
Shell-side pressure drop uses analogous correction factors (R_l, R_b, R_s) for the crossflow and window sections.

## Procedure
1. Compute geometry: baffle cut area, window area, crossflow area, bypass area, leakage areas.
2. Compute ideal coefficient and pressure drop for the crossflow section from published j and f charts or correlations (Taborek, HEDH).
3. Apply the correction factors and sum the pressure drops of crossflow, window and end zones.
4. Use rating software (commercial packages implement the method); check by hand to catch input errors.
5. Improve a low Jb with sealing strips and a tight bundle clearance; improve Jl with tighter tolerances.

## Gotchas
- The method's validity requires correct clearances (TEMA tolerances); input as built.
- Results are only as good as the geometry data; small errors in bundle-shell gap change Jb a lot.

## Verify
- [ ] J-factor product in the expected range, or the cause explained.
- [ ] Hand calculation within 20% of the rating program.
