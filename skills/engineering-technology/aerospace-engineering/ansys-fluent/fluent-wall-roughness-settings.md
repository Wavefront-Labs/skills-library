---
id: engineering-technology.aerospace-engineering.ansys-fluent.fluent-wall-roughness-settings
name: fluent-wall-roughness-settings
category: engineering-technology
field: aerospace-engineering
product: ansys-fluent
tags: [fluent, ansys, fluent-boundary-conditions, wall-roughness, sand-grain-roughness, roughness-height, skin-friction, surface-finish]
level: practitioner
status: draft
description: "Apply sand-grain roughness to Fluent walls, choosing roughness height and constant, and check that the near-wall mesh and y+ suit roughness modelling."
sources:
  - "Ansys Fluent user guide (wall roughness effects in turbulent flows)"
  - "Schlichting and Gersten, Boundary-Layer Theory (sand-grain roughness)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Fluent: wall roughness

**Goal:** model the skin-friction increase of rough surfaces (paint, ice, insects, composite surface).

## Steps
1. **Wall boundary condition > Momentum > Wall Roughness:** set **Roughness Height Ks** and **Roughness Constant Cs** (default 0.5; Cs 0.5-1 is the usual range, 0.5 corresponds to uniform sand-grain roughness).
2. Mesh: the wall-adjacent cell must be thicker than the roughness height (Fluent's guidance is that the cell height should exceed Ks); with fine `y+` meshes this limits Ks.
3. Note the equivalent sand-grain roughness for the surface; typical values are tens of micrometres for painted aircraft skin (use measured or reference data, since values depend on finish).

## Practice
- Run smooth and rough cases and compare `Cf` and drag; the effect grows with Reynolds number.
- Use the same turbulence model as for the smooth baseline.

## Gotchas
- Fully-rough regime needs `Ks+` greater than about 70: compute `Ks+ = Ks u_tau / nu` to see the regime.
- Roughness changes transition: a smooth-wall transition model may not capture it.

## Verify
- [ ] `Ks+` computed and regime stated; drag increase is in the expected range from literature.
