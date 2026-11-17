---
id: engineering-technology.aerospace-engineering.ansys-fluent.fluent-size-functions-curvature-proximity
name: fluent-size-functions-curvature-proximity
category: engineering-technology
field: aerospace-engineering
product: ansys-fluent
tags: [fluent, ansys, fluent-meshing, size-functions, curvature-sizing, proximity-sizing, local-sizing, body-of-influence]
level: practitioner
status: draft
description: "Control Fluent Meshing sizes with curvature, proximity, soft and hard size functions so edges, gaps and wakes are resolved without exploding the cell count."
sources:
  - "Ansys Fluent Meshing user guide (size functions and local sizing)"
  - "Ansys documentation"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Fluent size functions

**Goal:** surface and volume resolution where it matters.

## Types
- **Curvature:** cell size scaled to local curvature (normal angle and min size); put it on leading edges, fillets, nacelle lips.
- **Proximity:** sizes in narrow gaps (cells across the gap); needed for slats, flaps, control-surface gaps.
- **Soft vs hard:** soft sizes are respected unless a conflicting size is smaller; hard sizes override growth constraints, so use sparingly.
- **Local sizing / Body of influence (BOI):** explicit size on faces, edges or in a volume region (a box around the wake or shock).

## Procedure
1. Set global min and max size from the geometry scale and the expected number of cells.
2. Add curvature with normal angle about 10-18 degrees (smaller for finer) and a min size from the geometry detail; set growth rate (about 1.2).
3. Add proximity for gaps with 3-5 cells across the smallest gaps.
4. Add BOI for wake and shock zones.
5. Generate the surface mesh and review in sections.

## Gotchas
- Too many hard sizes give abrupt size jumps and poor volume mesh quality.
- Proximity with tiny gaps can drive absurd counts; set a minimum size.

## Verify
- [ ] Surface mesh shows smooth size transitions; the cell count is consistent with budget.
