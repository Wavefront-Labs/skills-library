---
id: engineering-technology.aerospace-engineering.ansys-fluent.fluent-watertight-geometry-workflow
name: fluent-watertight-geometry-workflow
category: engineering-technology
field: aerospace-engineering
product: ansys-fluent
tags: [fluent, ansys, fluent-meshing, watertight-geometry, meshing-workflow, surface-mesh, boundary-layers, external-aero]
level: practitioner
status: draft
description: "Run the Fluent Meshing Watertight Geometry task workflow for external aerodynamics, from import to volume mesh, with the checks to do at each task."
sources:
  - "Ansys Fluent Meshing user guide (task-based workflows)"
  - "Ansys Fluent documentation overview"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Fluent Meshing: Watertight Geometry workflow

**Goal:** a clean volume mesh of an aircraft or wing in a farfield box from watertight CAD.

## Task sequence (names as in the task-based workflow)
1. **Import Geometry:** CAD (STEP, or the native format); set units; use 'Create Object per' option so wing, fuselage and tail stay separate objects.
2. **Add Local Sizing:** curvature and proximity sizing on leading and trailing edges, junctions; face or edge sizing where needed.
3. **Generate the Surface Mesh:** set min/max size, growth rate; check the surface mesh quality and inspect trailing edges.
4. **Describe Geometry:** choose that the geometry is solid (fluid region wraps around), no leakages (watertight).
5. **Update Boundaries / Regions:** name inlet, outlet, farfield, wall zones; set symmetry plane for half models.
6. **Add Boundary Layers:** first height from the `y+` estimate, growth rate 1.1-1.2, number of layers; use aspect-ratio or offset method per the guide.
7. **Generate the Volume Mesh:** choose poly-hexcore, hexcore or tetrahedral fill; set the volume fill growth rate.

## Practice
- Create a farfield (enclosure) of at least tens of chords for subsonic cruise; use a body-of-influence mesh for the wake.
- Save the mesh and the workflow for repeatability, and use Python/journal scripting of the workflow where design sweeps are needed.

## Gotchas
- A gap or overlap in CAD gives a leak: use Shrinkwrap or CAD cleanup before the workflow.
- Trailing edge zero thickness needs a blunt edge or special handling.

## Verify
- [ ] Mesh Check passes; no negative volumes.
- [ ] Prism layers present on all walls, thickness near the estimate.
