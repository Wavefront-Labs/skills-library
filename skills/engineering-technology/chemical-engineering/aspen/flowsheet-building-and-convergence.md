---
id: engineering-technology.chemical-engineering.aspen.flowsheet-building-and-convergence
name: flowsheet-building-and-convergence
category: engineering-technology
field: chemical-engineering
product: aspen
tags: [chemical-engineering, aspen, aspen-plus, hysys, aspentech, process-simulation, flowsheet, convergence, tear-stream, wegstein, broyden, newton, property-method, peng-robinson, srk, nrtl, uniquac, unifac, elecnrtl, electrolyte-nrtl, steam-tables, iapws, radfrac, dstwu, design-spec, sensitivity-analysis, case-study, adjust, recycle, dwsim, chemcad, pro-ii]
level: practitioner
status: gated
description: "Build and converge an Aspen Plus/HYSYS flowsheet: property method choice, tear streams, Wegstein/Broyden, RadFrac/DSTWU, design specs, sensitivity, common errors."
sources:
  - "AspenTech Aspen Plus and Aspen HYSYS online help (property methods, convergence, RadFrac)"
  - "Carlson, E. C. (1996) Don't gamble with physical properties for simulations, Chem. Eng. Prog. (not indexed in Crossref; citation unconfirmed)"
  - "AspenTech Aspen Plus certification study guide AT-05198 (learning objectives, aspentech.com)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Building and converging a flowsheet in Aspen Plus / HYSYS

**Goal:** a flowsheet that converges reliably from a cold start, on a property method you
can defend, with every spec traceable to the design basis.

## 1. Components and property method first (most wrong answers start here)
Pick the method from the chemistry, not habit:
- **Hydrocarbons, gases, light ends, high pressure** (refinery, gas plant): Peng-Robinson
  (`PENG-ROB`) or SRK (`RK-SOAVE`). Water only as a near-immiscible second liquid;
  glycol/amine units need their dedicated packages.
- **Polar, non-ideal liquids below ~10 bar** (alcohols, ketones, acids, water–organic):
  activity model, `NRTL` or `UNIQUAC`, with an ideal or Redlich-Kwong vapour. Check every
  binary has regressed parameters (Properties › Binary Interaction): a blank pair means
  ideal behaviour for that pair and a missed azeotrope. Use `UNIFAC` only to fill gaps,
  and say so in the basis. Vapour-phase association (acetic/formic acid) needs
  `NRTL-HOC` (gated: unconfirmed, source is paywalled or blocked).
- **Liquid–liquid splits:** fit parameters to LLE data, not VLE data; VLE-regressed NRTL
  often predicts the wrong two-phase region.
- **Electrolytes** (sour water, caustic, acid gas in amine, salts): `ELECNRTL` via the
  Electrolyte Wizard, apparent vs true components chosen deliberately; HYSYS uses the Acid
  Gas / OLI packages.
- **Pure water/steam utilities:** `STEAMNBS` or IAPWS-95 steam tables, never a cubic EOS (method names (gated: unconfirmed, source is paywalled or blocked)).
Run **Analysis › Binary/Ternary** (T-xy, residue curves) before building columns. If the
diagram doesn't show the known azeotrope, nothing downstream will be right.

## 2. Build in order, run in pieces
1. Feed streams with full composition, T, P and flow; one block at a time, run after each.
2. Start columns with a **DSTWU** (Fenske–Underwood–Gilliland) shortcut: give light/heavy
   key recoveries (e.g. 0.99/0.01) and R/Rmin = 1.2–1.3, read N, feed stage, reflux and
   D/F. Use those to initialise **RadFrac** (stages, feed stage, reflux ratio, distillate
   rate). Note: Aspen numbers stages from the top, condenser = stage 1 (gated: unconfirmed, source is paywalled or blocked).
3. Converge RadFrac on easy specs (reflux ratio + D/F) first, then swap to product-purity
   specs with **Design Specs/Vary inside the column** (RadFrac › Specifications › Design
   Specifications), not an outer flowsheet loop.
4. Close recycles last.

## 3. Recycles and tear streams
- Let Aspen choose tears, or pick the stream with the fewest components/least sensitive
  variables. Give the tear a **good initial estimate** (from a once-through run); a zero-flow
  guess is the most common cause of failure.
- Methods: **Wegstein** (default, bounded acceleration, good for single loops), **Broyden**
  (quasi-Newton, better for several interacting loops or tears coupled with design specs),
  **Newton** (expensive, for tightly coupled specs). In HYSYS the RECYCLE operation does
  the same job with its own acceleration settings.
- Always put a **purge** on recycles of inerts; without one the inert builds without bound
  and the loop "fails to converge" because there is no steady state.

## 4. Design specs and sensitivity
- Design spec = one manipulated variable, one target, with **realistic lower/upper bounds**.
  If the target is out of reach within the bounds, the spec fails; widen or rethink.
- Run a **Sensitivity** (HYSYS: Case Study) on the manipulated variable first to see whether
  the target is reachable and monotonic. A non-monotonic response means the spec can flip
  between two solutions.
- Keep specs few; converge nested specs + recycles together in one Broyden block.

## 5. Common errors and fixes
| Message / symptom | Usual cause | Fix |
|---|---|---|
| RadFrac "failed to converge", oscillating | infeasible specs (purity above azeotrope, D/F wrong) | relax to reflux + D/F, check azeotrope, then re-add specs |
| "Tear stream not converged in N iterations" | bad initial guess, no purge, Wegstein overshoot | estimate the tear, add purge, raise max iterations, try Broyden |
| Flash "temperature/pressure out of range" or no liquid | spec in single-phase region, wrong method | check phase envelope, use valid-phases setting |
| Missing parameter warnings | binary pair not in databank | regress data or estimate (UNIFAC), document |
| Heater duty sign reversed | spec defines outlet vapour fraction across a phase boundary | specify T and P, then read the duty |

Worked check: a column feed of 100 kmol/h with 40% light key at 99% recovery must give
≈39.6 kmol/h of light key in the distillate. If the stream table disagrees, a spec is not
what you think it is.

## Verify
- [ ] Property method justified in writing; binaries checked; T-xy/residue curves match known data.
- [ ] Every column started from DSTWU or hand estimate, then converged on easy specs first.
- [ ] Recycles have tear estimates and purges; tear converged to tolerance, not "completed with warnings".
- [ ] Overall mass balance closes (Results Summary › Convergence and stream balance) to <0.1%.
- [ ] Sensitivity confirms design-spec targets are reachable and monotonic.
- [ ] Model reconverges after Reinitialize from a cold start.

Related: engineering-technology.chemical-engineering.separation-processes.distillation-column-shortcut-design,
engineering-technology.chemical-engineering.process-design.mass-and-energy-balances.
