---
id: creative-arts.animation.blender.fluid-mesh-generation
name: fluid-mesh-generation
category: creative-arts
field: animation
product: blender
tags: [blender, fluid, mantaflow, fluid-mesh-generation, fluid-mesh, upres-factor, mesh-smoothing]
level: practitioner
status: docs-checked
description: "Generate Mantaflow liquid meshes: enable mesh, upres factor, particle radius, smoothing, concave settings, mesh generator and speed vectors."
sources:
  - https://docs.blender.org/manual/en/latest/physics/fluid/type/domain/liquid/mesh.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# fluid-mesh-generation

## Mesh panel (Domain > Liquid > Mesh)

- **Mesh** checkbox: tells the cache which data to read; with no baked mesh the original domain is shown. It does not reset the cache, so it can switch the view between domain and baked mesh.
- **Upres Factor**: factor by which the mesh resolution is enhanced; the mesh is this many times bigger than the base simulation resolution.
- **Particle Radius**: radius of one liquid particle in grid cells; larger radii make the mesh cover more volume around particles. It is the same value as in the liquid settings, and the mesh shape depends on the combination of all mesh parameters.
- **Mesh Generator**: Final (higher quality, more options) or Preview (faster, less smooth).
- **Smoothing Positive**: more iterations smooth the outline but can stop small drops from being meshed. **Smoothing Negative**: more iterations sharpen the outline and keep details but make it more ragged.
- **Concavity Upper / Lower**: high values smoothen and fill concave regions; keep Lower below Upper, otherwise the mesh can be distorted and non-manifold.
- **Speed Vectors**: creates a `velocity` attribute with each vertex's velocity per frame, used automatically when rendering with motion blur. In Cycles, Deformation Motion Blur must be enabled on the object.
- **Bake Mesh / Free Mesh**: Modular cache only; Esc aborts, and a Bake Mesh can be paused and resumed.

## Workflow

1. Bake Data (Modular cache).
2. Enable Mesh, then Bake Mesh and review.
3. Adjust the mesh settings and rebake the mesh only.

## Verify

Compare Upres Factor 1 against a higher value: the surface detail increases while the overall motion stays the same.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (physics/fluid/type/domain/liquid/mesh; branch blender-v5.2-release) and the 5.2 source (rna_fluid.cc). Confirmed: Mesh checkbox behaviour, Upres Factor, Particle Radius, Mesh Generator Final/Preview, Smoothing Positive/Negative, Concavity Upper/Lower warning, Speed Vectors velocity attribute and Cycles Deformation Motion Blur requirement, Bake Mesh availability.

Method: documentation only; no commands were run.
