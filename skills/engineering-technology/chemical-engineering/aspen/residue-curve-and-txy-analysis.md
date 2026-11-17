---
id: engineering-technology.chemical-engineering.aspen.residue-curve-and-txy-analysis
name: residue-curve-and-txy-analysis
category: engineering-technology
field: chemical-engineering
product: aspen
tags: [chemical-engineering, aspen, aspen-binary-parameters-and-regression, residue-curve-and-txy-analysis, residue-curve, txy-diagram, azeotrope, distillation-boundary, property-analysis, ternary-map, aspen-plus]
level: practitioner
status: gated
description: "Use Property Analysis to build Txy diagrams, residue curve maps and azeotrope tables to spot distillation boundaries before designing a column."
sources:
  - "Aspen Plus and Aspen HYSYS user guides and help (AspenTech), Seider et al. Product and Process Design Principles"
  - "https://www.aiche.org"
  - "AspenTech Aspen Plus certification study guide AT-05198 (learning objectives, aspentech.com)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Txy and residue curve analysis

**Goal:** see the VLE topology of the mixture (azeotropes, boundaries) before you sequence or size columns.

## Steps
1. **Binary Txy / Pxy**: Property Analysis > Binary (the study guide confirms Binary Mixture Analysis for azeotrope detection and residue curves), choose Txy at the column pressure, plot x and y; read azeotrope compositions and T.
2. **Azeotrope search**: use the simulator's azeotrope search (Tools > Analysis > Property > Azeotrope Search (gated: unconfirmed, source is paywalled or blocked)) to list all binary and ternary azeotropes with type (homogeneous / heterogeneous, min / max boiling).
3. **Residue curve map**: Property Analysis > Residue (ternary) at the intended pressure, add the boundary lines; identify the stable and unstable nodes and saddles.
4. **Interpret**: feeds on either side of a distillation boundary cannot both reach the same product pure by simple distillation (the boundary can be curved, so feasible regions are not simply the triangle edges).
5. **Check pressure sensitivity**: repeat at a second pressure; if the azeotrope shifts a lot, pressure-swing distillation is a candidate.

## Gotchas
- A fitted model can invent or hide an azeotrope; confirm against literature data.
- Heterogeneous azeotropes need a three-phase flash to show up.

## Verify
- [ ] Reported azeotropes match literature compositions within a few mol%.
- [ ] Map saved with pressure noted.
