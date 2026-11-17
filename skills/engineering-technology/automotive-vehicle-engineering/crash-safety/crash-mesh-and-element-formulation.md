---
id: engineering-technology.automotive-vehicle-engineering.crash-safety.crash-mesh-and-element-formulation
name: crash-mesh-and-element-formulation
category: engineering-technology
field: automotive-vehicle-engineering
product: crash-safety
tags: [crash-mesh, mesh, element-formulation, shell-elements, time-step, hourglass, mass-scaling, crash-cae, belytschko-tsay, mesh-quality, integration-points]
level: practitioner
status: gated
description: "Build a crash FE mesh: element size and quality limits, shell formulation and integration, hourglass control, time-step and mass scaling, and mesh checks before running."
sources:
  - "LS-DYNA user manual contents (keyword manual volumes I-III; vendor documentation at https://www.ansys.com)"
  - "Huang, Vehicle Crash Mechanics (chapter list)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Crash mesh and element formulation

Typical sizes, thresholds and keyword choices below are practice rules; the c = sqrt(E/rho) estimate was computed (5170 m/s for E 210 GPa, rho 7850 kg/m3, so a 5 mm element gives about 1 microsecond). ELFORM 2 as reduced-integration Belytschko-Tsay and ELFORM 16 as fully integrated were seen in Ansys/DynaSupport documentation but the manual was not fetched (gated: unconfirmed, source is paywalled or blocked).

## 1. Element size and type
Body structure sheet metal: mostly shell elements with a typical target size of about 5 mm (finer for fine details and fracture, up to 10 mm for coarse; follow your company's meshing standard). Fully quad-dominant (aim for few triangles, commonly under ten percent) and mapped to follow flanges and radii. Resolve section buckling: at least several elements across a flange or radius, otherwise folds are too stiff.

## 2. Shell formulation
- Reduced-integration shell (Belytschko-Tsay type, LS-DYNA ELFORM 2) is cheap and common; needs hourglass control.
- Fully integrated shells (such as ELFORM 16) resist hourglassing and are better for bending, at higher cost.
- Use five through-thickness integration points for plasticity-dominated shells (standard practice) rather than the minimum.
Solid elements for thick castings, adhesives (layers), foam and batteries; use fully integrated or selectively reduced solids with hourglass monitoring.

## 3. Time step
Explicit stability needs dt <= L_min / c, with c = sqrt(E/rho) about 5000 m/s for steel. A 5 mm element gives about 1 microsecond. The smallest element sets the step for the whole model, so remove tiny elements, merge short edges, or apply controlled **mass scaling** to a minimum step (typical practice is a fixed dt such as around 1 microsecond with added mass limited to a small fraction of model mass; check your standard). Monitor added mass and its distribution (added mass in a moving local region distorts momentum).

## 4. Mesh quality criteria
Typical checks: aspect ratio, skew, warpage, Jacobian, minimum and maximum internal angles for quads and trias, minimum element length, penetrations and free edges. Set thresholds from your meshing standard and fix before running.

## 5. Connectivity and details
Mesh flanges to align weld positions (see spot weld modelling); avoid duplicate nodes; maintain a constant thickness and material assignment per part; keep contacts clean (no initial penetration; use gap offsets). Include tolerances on hole sizes and fillets that drive stiffness.

## 6. Checks
Run a short termination to verify energy balance, check hourglass energy under about five percent of internal energy (typical criterion), added mass ratio small, no negative volumes.

## Verify
- [ ] Mesh quality report passes the standard.
- [ ] Minimum time step and mass scaling documented.
- [ ] Hourglass and added mass checked in a trial run.
- [ ] Shell integration points and formulations set per part type.
