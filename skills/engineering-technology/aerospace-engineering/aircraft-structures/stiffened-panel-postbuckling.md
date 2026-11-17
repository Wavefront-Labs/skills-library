---
id: engineering-technology.aerospace-engineering.aircraft-structures.stiffened-panel-postbuckling
name: stiffened-panel-postbuckling
category: engineering-technology
field: aerospace-engineering
product: aircraft-structures
tags: [postbuckling, effective-width, diagonal-tension, stiffened-panels, skin-buckling, thin-walled-structures]
level: practitioner
status: draft
description: "Estimate postbuckled stiffened-panel capacity using effective width for compression and diagonal tension for shear, and state where the methods stop being valid."
sources:
  - "Niu, Airframe Structural Design"
  - "Bruhn, Analysis and Design of Flight Vehicle Structures"
  - "Megson, Aircraft Structures for Engineering Students"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Stiffened panel postbuckling

**Goal:** capacity of a panel that buckles locally but still carries more load.

## Compression: effective width
- After the skin buckles, load shifts to the stiffeners and to strips of skin next to them. Von Karman's concept: the skin acts as a strip of effective width `b_e` at the edge stress, with `b_e/b` approximately `sqrt(sigma_cr / sigma_edge)`.
- Panel strength: sum of stiffener area plus effective skin area, times the stiffener crippling or column stress.
- Check column buckling, stiffener crippling, and the interaction of local and global modes.

## Shear: diagonal tension
- Thin webs and skins in shear buckle at low load and develop a diagonal tension field. Wagner pure tension field theory and Kuhn's incomplete tension field method give the web stress, the stiffener loads and the angle of the tension field, with a factor `k` between 0 (unbuckled) and 1 (fully developed).
- Uprights get compression plus bending from the tension field; flanges get extra bending.

## Practice
1. Get `sigma_cr` for the skin (see panel-buckling-analysis).
2. Decide the allowed buckling: many programmes require no buckling at limit load, with postbuckling only between limit and ultimate. This is a company or programme criterion, not a universal rule.
3. Use the closed-form method for preliminary sizing; use nonlinear FE (geometric nonlinearity, imperfections) for final analysis, and compare with tests.

## Gotchas
- Fastener spacing and rivet pull-through limit postbuckled capacity.
- Imperfections lower the strength of stringer panels; include them in FE.
- Composite panels may delaminate at stiffener runouts when postbuckled.

## Verify
- [ ] Closed-form panel capacity is within the scatter of a nonlinear FE result before design is frozen.
