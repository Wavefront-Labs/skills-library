---
id: engineering-technology.civil-engineering.plaxis.staged-excavation-model
name: staged-excavation-model
category: engineering-technology
field: civil-engineering
product: plaxis
tags: [plaxis, plaxis-2d, bentley, geotechnical-fem, finite-element, staged-construction, deep-excavation, retaining-wall, embedded-wall, sheet-pile, diaphragm-wall, ground-anchors, struts, hardening-soil, hs-small, mohr-coulomb, undrained-a, undrained-b, k0-procedure, interface, rinter, phi-c-reduction, safety-analysis, settlement, eurocode-7]
level: advanced
status: verified
description: "Model a supported excavation in PLAXIS 2D: soil model choice (HS vs MC), parameters, wall and anchors, staged phases, drainage type, and checking wall forces and settlements."
sources: ["Bentley PLAXIS 2D Reference Manual", "Bentley PLAXIS Material Models Manual", "Schanz, Vermeer & Bonnier (1999), The hardening soil model: formulation and verification", "Potts & Zdravkovic, Finite Element Analysis in Geotechnical Engineering", "CIRIA C760 Guidance on embedded retaining wall design", "EN 1997-1 Eurocode 7: Geotechnical design"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# PLAXIS staged excavation — wall forces and ground movements you can defend

**Goal:** a 2D plane-strain model of an embedded retaining wall (sheet pile, secant or
diaphragm) with anchors or props, built phase by phase, that predicts wall bending,
prop/anchor loads and surface settlement credibly enough for design and for setting
monitoring trigger levels.

## 1. Geometry and mesh
- Model **half the excavation** if symmetric (with a vertical fixity on the axis).
- Extend the model about **3–5 × excavation depth** behind the wall and at least
  **2–3 × depth** below formation (or to rock) (rules of thumb (gated: unconfirmed, source is paywalled or blocked); confirm with a boundary-sensitivity run). Boundaries too close stiffen the result.
- Wall = **plate** (EA, EI, w, ν). Anchors = **node-to-node anchor** for the free
  length + **embedded beam** (or geogrid) for the grouted length. Props = fixed-end
  anchor or node-to-node anchor between walls.
- Add **interfaces** on both sides of the wall, extended a little below the toe to avoid
  stress singularities.
- Mesh: Medium globally, refine around the wall and the grout bodies. Check the result
  doesn't change materially on a finer mesh.

## 2. Pick the soil model
- **Mohr-Coulomb (MC):** one stiffness for loading and unloading. In excavations it
  over-predicts base heave and often gives **upward** movement of the wall and
  retained ground — misleading for settlement. Fine for quick ULS checks only.
- **Hardening Soil (HS):** stress-dependent stiffness, separate unloading/reloading
  stiffness. The default choice for excavations.
- **HS small (HSsmall):** adds small-strain stiffness (G0, γ0.7); best for predicting
  settlement profiles behind stiff walls and near sensitive structures.
- Starting relationships (to be replaced by test data): E_oed,ref ≈ E50,ref and
  E_ur,ref ≈ 3 × E50,ref (Bentley PLAXIS wiki, Hardening Soil model: suggested defaults, and very soft or stiff soils tend to give other ratios); p_ref = 100 kPa (moduli referenced to 100 stress units by default, PLAXIS course handout); power m ≈ 0.5 for sands, approaching 1.0 for
  soft clays (gated: unconfirmed, source is paywalled or blocked); ν_ur = 0.2 (gated: unconfirmed, source is paywalled or blocked).
- Interface strength **R_inter**: around 0.67 for sand/steel or concrete and 0.5 for
  clay/steel are common starting points (gated: unconfirmed, source is paywalled or blocked); smooth bentonite-cast diaphragm walls may
  warrant lower. Treat as an assumption to state, not a constant.

## 3. Drainage type (the most common error)
- **Drained** for sands and for long-term clay states.
- **Undrained (A):** effective stiffness and strength; PLAXIS computes pore pressures.
  With MC, undrained A gives the wrong undrained shear strength — the stress path does
  not reproduce real su. Use HS/HSsmall or check su against tests.
- **Undrained (B):** effective stiffness, total strength input as su. Safer for clays
  with good su data; drawback: strength doesn't increase with consolidation.
- Short-term excavation phases in clay: undrained; then a **consolidation** phase or a
  drained long-term check.

## 4. Phases (Staged construction)
1. **Initial phase — K0 procedure** for horizontal ground (K0 = 1 − sin φ′ for NC soils;
   higher for overconsolidated). Use Gravity loading if the surface is sloping.
2. **Wall installation** (wished-in-place): activate plate and interfaces. Then
   **reset displacements to zero** in the next phase so settlement plots start at zero.
3. **Surcharge** behind the wall (typically 10 kPa construction load (gated: unconfirmed, source is paywalled or blocked); check your code or
   client spec).
4. **Excavate to ~0.5 m below anchor level**, then **install and prestress** the anchor
   (enter the lock-off load in the anchor's Adjust prestress), then next dig, etc.
5. **Dewatering:** define water levels per phase (user water levels or a groundwater
   flow calculation if seepage around the toe matters).
6. **Safety calculation** (phi/c reduction) after critical phases: the Msf (ΣMsf) plateau
   gives a global factor of safety. Under Eurocode 7 DA1 the design is usually done by
   factoring parameters (Combination 2) or effects (Combination 1) — the PLAXIS
   "Design approaches" feature can apply partial factors; confirm the setup with your
   project's national annex.

## 5. Read the results
- Plate: bending moment and shear envelopes over all phases (not just the last).
- Anchor/prop forces per phase; the maximum often occurs one phase after installation.
- Wall deflection vs depth; surface settlement trough behind the wall.
- Sanity-check against empirical envelopes: e.g. Clough & O'Rourke / Peck-type charts —
  maximum surface settlement for stiff-wall excavations in stiff clay is commonly
  around 0.1–0.3% of excavation depth (gated: unconfirmed, source is paywalled or blocked).

## Gotchas
- Not resetting displacements after wall installation makes settlements look far too big.
- Plates have zero thickness; wall self-weight and friction depend on w and R_inter.
- Plastic points piling up at the toe = inadequate embedment, not a mesh problem.
- Parameter values above are typical literature values, not substitutes for site tests.

## Verify
- [ ] Soil model and drainage type are stated and justified per layer.
- [ ] K0 initial stresses check out (σ′h / σ′v in Output matches input K0).
- [ ] Displacements reset after wall installation; phases mirror the actual construction sequence.
- [ ] Envelopes of moments, shears and anchor forces taken over all phases.
- [ ] Safety analysis Msf plateau reached and exceeds the required factor.
- [ ] Settlement and deflection are in line with empirical case-history ranges, or the difference is explained.
