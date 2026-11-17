---
id: engineering-technology.structural-engineering.structural-analysis.hand-checking-software-models
name: hand-checking-software-models
category: engineering-technology
field: structural-engineering
product: structural-analysis
tags: [structural-analysis, hand-calculation, sanity-check, model-checking, finite-element, frame-analysis, equilibrium, tributary-area, portal-method, cantilever-method, beam-formulas, deflection, moment-distribution, rayleigh-method, approximate-analysis, etabs, sap2000, robot, risa, staad, spacegass, model-verification, quality-assurance]
level: practitioner
status: verified
description: "Sanity-check FE frame models by hand: reaction totals, tributary and portal-method checks, beam formulas, deflection bounds and the usual modelling errors to hunt."
sources:
  - "Hibbeler, Structural Analysis"
  - "Leet, Uang and Gilbert, Fundamentals of Structural Analysis"
  - "IStructE Essential Knowledge Text No. 14, Principles for computer analysis of structures (MacLeod and Weir, 2016)"
  - "AISC Steel Construction Manual, Part 3 beam diagrams and formulas"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Hand-checking software models — trust the model only after it agrees with you

**Goal:** confirm, in under an hour, that an analysis model carries the right total
load along the right path with believable forces and deflections. Then look for the
handful of modelling errors that cause most wrong answers.

The order is global first, then local. A model can have perfect member forces in the
wrong building.

## 1. Global equilibrium (always first)
1. Hand-total each load pattern: (area × pressure) + (line loads × length) + self
   weight. Sum the vertical reactions per pattern in the model. The two should agree
   **within about 1–2%**. If they don't, a load is missing, doubled, on the wrong pattern
   or pointing the wrong way. Check the sign convention for gravity, which is −Z in most
   packages.
2. For lateral patterns, the base shear equals the sum of the applied story forces.
   The overturning moment equals Σ F·h. Uplift appears where you expect it.
3. For self-weight, check the density, the unit weight of the material and whether
   the slab is counted both as an area load and as shell self-weight.

## 2. Local gravity checks
- **Column axial loads** from tributary area × floor load × number of floors. Expect
  interior columns of continuous frames to carry about 10–15% more than strict
  tributary, and first-interior columns more than that (rule of thumb; for two equal spans the central support reaction is 1.25wL, so 25% more than tributary, computed).
- **Beam moments** (uniform load w, span L):
  - simply supported: wL²/8 midspan;
  - fixed–fixed: wL²/12 at supports and wL²/24 midspan;
  - continuous interior spans: about wL²/10 to wL²/11 at supports and wL²/16 midspan
    (the classic ACI-coefficient region (gated: unconfirmed, source is paywalled or blocked); these are envelope coefficients that include pattern loading).
  Do NOT expect continuous-beam moments to sit between the simple and fixed values. Computed with the three-moment equation for equal spans under full uniform load: support moment wL²/8 for two spans, wL²/10 at both supports of three spans, wL²/9.33 and wL²/14 for four spans, and the middle span of a three-span beam has only about wL²/40 at midspan. The reliable check is statics: midspan moment + average of the two end moments = wL²/8 for each span.
- **Deflection:** simply supported 5wL⁴/(384EI) and fixed–fixed wL⁴/(384EI). A
  continuous span lands between them. Cantilever: wL⁴/(8EI) for uniform load and
  PL³/(3EI) for a tip load.
- **Moment distribution** or a 2–3 bay sub-frame (columns fixed at far ends) is a fast,
  credible check on one critical floor.

## 3. Lateral checks
- **Portal method** for moment frames: interior columns take twice the shear of
  exterior columns, with inflection points at mid-height of columns and mid-span of
  beams. Column moment ≈ V_col × h/2.
- **Cantilever method** for tall, slender frames: column axial forces are proportional
  to the distance from the frame centroid.
- **Wall/frame sharing:** stiffness ratios give a rough split. Walls typically take
  most of the shear low down, and frames pick up more of it near the top.
- **Period:** compare with the ASCE 7 approximate period Ta = Ct·hn^x (for example
  0.02·hn^0.75 for "other" systems, with hn in feet (gated: unconfirmed, source is paywalled or blocked)) or the rough T ≈ 0.1N
  (N = number of stories; rough rule (gated: unconfirmed, source is paywalled or blocked)). Rayleigh, T = 2π √(Σwδ² / (gΣFδ)), using the static
  deflections, is a strong independent check.
- **Drift:** a single storey of a moment frame drifts roughly V·h³/(12ΣEIc) (fixed–fixed
  columns), bounded by flexible-beam cases. Order of magnitude is what matters here.

## 4. The usual suspects (hunt these when numbers disagree)
- Units: kN vs kip, mm vs m, a modulus entered in the wrong units. These give a 10³
  or 10⁶ error.
- Member releases: a released beam end that should be continuous, or both ends of a
  column released, which makes a mechanism. Some solvers stabilise mechanisms
  silently with tiny springs, so read the warnings.
- Local axes: rotated columns (weak axis resisting the frame), and area loads applied
  in the local direction instead of the global one.
- Offsets and rigid links that stiffen far more than intended.
- Property modifiers left over from a copied model.
- Support conditions: pins where fixity is assumed in design, or the reverse.
- Mesh: shells too coarse for the stress gradient, or nodes not connected (a beam
  passing a wall edge without a shared node).
- Nonlinear cases (P-delta, tension-only, staged) combined by superposition. Combine
  these by analysing each combination, not by adding results.

## 5. Tolerances and reporting
Global checks: within about 2%. Local member checks: within about 10–20% is normal,
because hand methods are approximate (office practice, not a code value). Differences above about 25% need an explanation
before you sign anything. Record each check (hand value, model value, ratio) in the
calculation package so a reviewer can repeat it.

## Verify
- [ ] Every load pattern's reactions match the hand total within about 2%.
- [ ] At least one critical beam, column and lateral element is checked by hand.
- [ ] Deflections fall between the simple and fixed bounds, and moments satisfy the span statics check.
- [ ] Period and drift are of the expected order of magnitude.
- [ ] All solver warnings (mechanisms, ill-conditioning, disconnected joints) are resolved.
- [ ] Checks are recorded with ratios in the calculation package.
