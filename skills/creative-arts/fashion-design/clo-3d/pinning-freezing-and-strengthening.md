---
id: creative-arts.fashion-design.clo-3d.pinning-freezing-and-strengthening
name: pinning-freezing-and-strengthening
category: creative-arts
field: fashion-design
product: clo-3d
tags: [fashion-design, clo-3d, clo-simulation, clo-freeze, clo-pin, clo-strengthen, simulation-control, clo-layer-control]
level: practitioner
status: draft
description: "Control CLO simulation with pins, freeze, deactivate, strengthen and hide: holding fabric in place, isolating layers, and speeding up complex garment setups."
sources:
  - https://support.clo3d.com/hc/en-us
  - https://www.clo3d.com/en/
  - https://support.clo3d.com/hc/en-us/categories/360000059787
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pinning, freezing and strengthening

**Goal:** hold parts of a garment still or stiff while others simulate, to fix problems,
build layers and speed up work.

## Tools
- **Pin (3D)**: hold particles in place (Pin tool, or Shift+right-click drag in 3D in
  recent versions); pinned areas stay put while you drag or simulate; useful to hold a
  collar, a draped fold, or tuck a shirt.
- **Freeze**: right-click a pattern > Freeze; it becomes rigid and other garments collide
  with it but it doesn't move. Use to lock an inner layer while adjusting the outer.
- **Deactivate**: pattern ignored in simulation and collisions (sewing temporarily inactive).
- **Strengthen**: temporarily stiffens a pattern (right-click > Strengthen) so it holds
  shape during arrangement; un-strengthen afterward.
- **Hide/Show**: reduce visual clutter; hidden patterns may still simulate depending on
  settings.

## Workflows
- **Layering**: simulate inner garment; freeze it; dress and simulate the outer; unfreeze
  and simulate together briefly to settle.
- **Tucking**: pin the shirt hem inside the trouser waist area, simulate, then release.
- **Draped design**: pin folds where they should hold (as you would pin on a stand), then
  convert to tacking (tack lines/points) for permanent holds.
- **Performance**: freeze or deactivate pieces not being edited to speed simulation.

## Gotchas
- Forgetting to unfreeze before final render leaves rigid, unnatural garments.
- Pins left in place distort fit maps.
- Strengthened pieces look stiff if you forget to restore them.

## Verify
- [ ] No unintended pins, freeze or strengthen states before final simulation.
- [ ] Layer order correct after unfreezing.
- [ ] Permanent holds converted to tacks if needed.
