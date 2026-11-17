---
id: engineering-technology.marine-naval-engineering.maxsurf.hull-model-to-stability-and-resistance
name: hull-model-to-stability-and-resistance
category: engineering-technology
field: marine-naval-engineering
product: maxsurf
tags: [maxsurf, maxsurf-modeler, maxsurf-stability, maxsurf-resistance, bentley, naval-architecture, hull-modelling, nurbs, fairing, hydrostatics, intact-stability, gz-curve, is-code, imo, holtrop-mennen, savitsky, delft-series, resistance-prediction, msd]
level: practitioner
status: draft
description: "Take a Maxsurf hull from Modeler (frame of reference, fairing, hydrostatics) into Stability (tanks, loadcases, IS Code criteria) and Resistance (method choice, validity)."
sources:
  - "Bentley Maxsurf Modeler, Stability and Resistance user manuals (current CONNECT Edition)"
  - "IMO International Code on Intact Stability, 2008 (IS Code)"
  - "Holtrop & Mennen, An approximate power prediction method (1982) and Holtrop (1984) update"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Maxsurf: one hull model through Modeler, Stability and Resistance

**Goal:** build a single, watertight, fair hull in Maxsurf Modeler and carry the same
`.msd` file into Stability and Resistance so that hydrostatics, GZ curves and resistance
all come from one consistent geometry.

Menu names below follow recent Maxsurf CONNECT releases; they move between versions,
so check your version's manual if an item is not where stated.

## 1. Modeler: set up before you shape
1. **Units and frame of reference first.** Data › Units (metres, tonnes). Then Data ›
   Frame of Reference: set the baseline, the design waterline (DWL) and the forward and
   aft perpendiculars. Every hydrostatic result (LCB, LCF, KM) is referenced to these;
   changing them later silently shifts all numbers.
2. **Zero point.** Put it at AP/baseline (or midships) and keep it identical in every
   module. A mismatched zero point is the usual reason LCG in Stability looks wrong.
3. **Surfaces, not one patch.** Start from a parametric template or a minimal NURBS
   surface (e.g. 5 x 5 control points) and add rows only when the shape demands it.
   Fewer control points = easier fairing.
4. **Surface properties matter for analysis:** each surface's *Use* (hull, internal
   structure, superstructure) and whether it is included in hydrostatics. Decks and
   bulkheads must not be counted as buoyant hull.
5. **Fair with the tools, not the eye.** Turn on curvature display (Gaussian
   curvature colour map and curvature porcupines on sections/waterlines). Look for
   sign changes and kinks; drag control points in rows, never single points in
   isolation.
6. **Bond edges** of adjoining surfaces (keel to topsides, transom); a millimetre gap
   can break section calculation.
7. **Check hydrostatics in Modeler** (Data › Calculate Hydrostatics) at the DWL and
   record displacement, LCB, Cb, Cp, waterplane area. These are your reference values.

## 2. Stability: geometry, tanks, loadcases, criteria
1. Open the same `.msd`. Compute sections (Analysis › Sections or equivalent); use
   enough stations (start ~100-200 along the length) and view them to confirm every
   section is closed. Missing chunks = an open or unbonded surface.
2. **Cross-check**: run Upright Hydrostatics at the design draft. Displacement and LCB
   should match Modeler within about 0.5 %. If not, fix geometry before going further.
3. Define **rooms/tanks** in the Room Definition window: boundaries, permeability
   (e.g. 0.98 for tanks, 0.95 for accommodation, 0.85 for machinery spaces, 0.60 for
   stores; confirm against your rule set), fluid type and density.
4. Set **downflooding points** (vents, air pipes, unprotected openings). Stability
   uses them to find the flooding angle that truncates the GZ area criteria.
5. Build **loadcases**: lightship (weight, LCG, VCG, TCG) plus tank fill levels and
   deadweight items. Choose free-surface treatment: maximum free-surface moment per
   tank (the IS Code approach for criteria) rather than actual fill level, unless your
   approval body accepts otherwise.
6. Select **criteria** from the library (IMO IS Code 2008 Part A general criteria and
   weather criterion) and run Large Angle Stability, heel range 0-60 deg or more,
   with **free-to-trim** on. Fixed-trim GZ curves overestimate stability for vessels
   with large trim change.
7. Use KN Values or Limiting KG for the stability booklet; see
   engineering-technology.marine-naval-engineering.ship-stability.intact-stability-criteria-check
   for the criteria themselves.

## 3. Resistance: pick a method whose database fits the hull
1. Open the `.msd`; Resistance measures the hull at the chosen draft. Override
   measured parameters (wetted area, half-angle of entrance, transom area) if the
   automatic measurement is obviously off.
2. **Choose the method by hull type:** Holtrop for displacement merchant hulls;
   Savitsky (pre-planing/planing) for planing craft; Delft series for sailing-yacht
   canoe bodies; others (Compton, Fung, Van Oortmerssen, Series 60) for their niches.
3. **Read the validity window.** Each method shows parameter limits (Fn, Cp, L/B,
   B/T, LCB). Values outside the range turn red or are flagged; results there are
   extrapolation, not prediction.
4. Set the speed range and the overall efficiency so the tool reports power as well
   as resistance; confirm whether your version's efficiency setting means propulsive
   (ηD) or total efficiency.
5. Compare two applicable methods; a spread above ~15 % means one is out of its depth.

## Gotchas
- Hydrostatics in Modeler and Stability use separate calculations; disagreement is
  a geometry problem, not a rounding issue.
- Skin thickness: surfaces are moulded by default. Shell plating displacement
  (typically 0.2-0.6 % for steel ships) is added separately (appendage factor).

## Verify
- [ ] Frame of reference and zero point identical in all three modules.
- [ ] Every Stability section is closed; upright displacement within ~0.5 % of Modeler.
- [ ] Curvature display shows no unintended inflections on the hull.
- [ ] Downflooding points defined; large-angle run is free to trim.
- [ ] Resistance method parameters all inside validity limits at design speed.
