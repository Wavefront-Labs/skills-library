---
id: engineering-technology.automotive-vehicle-engineering.chassis-suspension-design.body-modal-and-stiffness-fea-checks
name: body-modal-and-stiffness-fea-checks
category: engineering-technology
field: automotive-vehicle-engineering
product: chassis-suspension-design
tags: [body-modal-fea, modal-fea, nastran, sol-103, optistruct, free-free-modes, modal-assurance-criterion, mac, biw, stiffness-fea, mesh-check]
level: practitioner
status: gated
description: "Run modal and static stiffness FEA on body-in-white and trimmed body: set-up, mesh and mass checks, free-free boundary conditions, target modes and test correlation with MAC."
sources:
  - "Happian-Smith, Introduction to Modern Vehicle Design (chapter list)"
  - "Harrison, Vehicle Refinement (chapter list)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Body modal and stiffness FEA checks

## 1. Models
- **BIW:** shell mesh of structure with spot welds, adhesives, seam welds; glass (bonded) as shells; closures optional.
- **Trimmed body:** adds mass of interior, powertrain mounts, seats, cockpit, fuel, as lumped masses connected by rigid or flexible elements.
Typical shell element size 5-10 mm for body panels (gated: unconfirmed, source is paywalled or blocked); use quads preferentially, controlled quality (warpage, skew, minimum length, Jacobian).

## 2. Model checks before solving
1. Free-free unconstrained check: six rigid-body modes at near-zero frequency (in a Nastran-type normal-mode run, SOL 103 (gated: unconfirmed, source is paywalled or blocked)) and no extra mechanisms.
2. Total mass and centre of gravity against the CAD and weigh data.
3. Unit consistency (mm-tonne-s: density in tonne/mm^3, modulus in MPa).
4. Connector coverage: every flange pair has weld or adhesive elements, with correct stiffness.
5. Contact-free: modal runs are linear; remove nonlinear contacts or replace with tied connections.

## 3. Modal analysis
Extract modes to a frequency range above the range of interest (e.g. up to 200 Hz). Identify the first torsion and first bending modes, front-end and rear-end shake modes, and panel modes. Compare with targets cascaded from the vehicle NVH targets (see NVH target cascade). Use modal strain energy and participation to identify where to add stiffness or mass.

## 4. Static stiffness cases
Torsion, bending, lateral bending, subframe mount and suspension attachment local stiffness (dynamic stiffness at mounts), door sag, tailgate, front and rear beam stiffness. Run with SOL 101 or equivalent static solvers.

## 5. Correlation with test
Experimental modal analysis of the BIW or trimmed body (free-free on soft supports) gives mode shapes and frequencies. Compute the modal assurance criterion (MAC) between FE and test modes: MAC near 1 means similar shapes; values above roughly 0.8-0.9 are commonly regarded as a good match (apply your own criterion (gated: unconfirmed, source is paywalled or blocked)). Update joint, connector and damping assumptions; correlate before using the model for decisions.

## Verify
- [ ] Rigid body modes, mass, CG and units checked.
- [ ] Connectors present at all joints.
- [ ] Target modes tabulated with FE result and margin.
- [ ] MAC and frequency error vs test recorded.
