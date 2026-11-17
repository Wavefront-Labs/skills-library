---
id: engineering-technology.aerospace-engineering.aerodynamics.xfoil-viscous-analysis
name: xfoil-viscous-analysis
category: engineering-technology
field: aerospace-engineering
product: aerodynamics
tags: [aerodynamics, airfoils, xfoil, viscous-analysis, airfoil-polar, ncrit, panel-method, low-reynolds-number, drela]
level: practitioner
status: verified
description: "Run viscous airfoil polars in XFOIL: load or generate a section, set Re, Mach and Ncrit, sweep alpha, and recognise unconverged or untrustworthy results."
sources:
  - "XFOIL user guide (Mark Drela, MIT)"
  - "Drela, XFOIL an analysis and design system for low Reynolds number airfoils"
  - "https://web.mit.edu/drela/Public/web/xfoil/xfoil_doc.txt"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# XFOIL viscous polars

**Goal:** a trustworthy lift/drag/moment polar for a 2D section at a given Re and Mach.

## Session outline
```
naca 2412          # or: load mysection.dat
pane               # re-panel to about 140+ panels
oper
visc 1e6           # turns on the viscous mode and sets Re
mach 0.0
iter 200
pacc               # open polar accumulation; give a save file name
aseq -4 14 0.5     # sweep alpha from -4 to 14 in 0.5 steps
pacc               # close polar file
```
Set transition criterion with the `vpar` submenu: `n 9` sets Ncrit. Drela's guide suggests roughly 9 for an average wind tunnel, 10-12 for a clean tunnel, 12-14 for a good sailplane environment and lower (4-8) for a dirty tunnel or rough surface. Force transition with `xtr` (top, bottom trip locations as x/c).

## Practice
- Re-run from the previous converged alpha upward and downward; sweep both ways and compare.
- Use the Mach number only for the Karman-Tsien correction; XFOIL is not valid in transonic flow with shocks.
- Trust drag at attached conditions; treat `cl_max` and post-stall as indicative only.
- For airfoils with open trailing edges or very blunt shapes, check panelling and results.

## Failure modes
- "Convergence failed" near stall: lower alpha step, raise `iter`, or accept stall has been reached.
- Strange polars from poor panelling at the leading edge; refine with `ppar`.
- Results highly sensitive to Ncrit at low Re (laminar separation bubbles): quote the Ncrit used.

## Verify
- [ ] Re-panelled polar and polar from a finer panelling agree on cl and cd to a few percent.
- [ ] A NACA 0012 at Re 3e6 reproduces known values: cl_alpha near 0.11 per degree and cdmin of about 0.006 (published wind tunnel data lie in this range (gated: unconfirmed, source is paywalled or blocked)).
