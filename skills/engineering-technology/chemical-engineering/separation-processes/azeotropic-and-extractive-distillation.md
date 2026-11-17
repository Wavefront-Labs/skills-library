---
id: engineering-technology.chemical-engineering.separation-processes.azeotropic-and-extractive-distillation
name: azeotropic-and-extractive-distillation
category: engineering-technology
field: chemical-engineering
product: separation-processes
tags: [chemical-engineering, separation-processes, sep-special-distillation, azeotropic-and-extractive-distillation, azeotropic-distillation, extractive-distillation, entrainer]
level: practitioner
status: draft
description: "Separate azeotropes with an entrainer: choose heterogeneous azeotropic or extractive distillation and set the column train."
sources:
  - "Seader Henley and Roper Separation Process Principles, Perry Chemical Engineers Handbook, Kister Distillation Design, Treybal Mass-Transfer Operations"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Azeotropic and extractive distillation

**Goal:** Separate azeotropes with an entrainer: choose heterogeneous azeotropic or extractive distillation and set the column train.

## Steps
1. Confirm the azeotrope with VLE data or a validated model; map residue curves or distillation boundaries for the ternary system.
2. Extractive distillation: add a high-boiling solvent that changes the relative volatility and does not form new azeotropes; the solvent is fed above the main feed and recovered in a second column.
3. Heterogeneous azeotropic distillation: use an entrainer that forms a heterogeneous azeotrope so a decanter splits it into two liquid phases and the entrainer is recycled.
4. Screen entrainers by selectivity at infinite dilution, boiling point, toxicity and cost.
5. Simulate with a model validated against the LLE and VLE data (NRTL or UNIQUAC with regressed parameters), then check feasibility and optimise solvent ratio.

## Gotchas
- Predicted separations are very sensitive to the model; regress from data.
- Entrainer losses and make-up need to be included.

## Verify
- [ ] Residue curve map shows a feasible path.
- [ ] Entrainer balance closes with make-up.
