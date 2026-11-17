---
id: creative-arts.animation.blender.retopo-addons
name: retopo-addons
category: creative-arts
field: animation
product: blender
tags: [blender, retopoflow, bsurfaces, retopo-addons, quad-remesher, retopology, instant-meshes]
level: practitioner
status: docs-checked
description: "Choose retopology helpers beyond core Blender: Bsurfaces from strokes, RetopoFlow tools, Quad Remesher and Instant Meshes auto-retopo, and when manual work is still needed."
sources:
  - https://extensions.blender.org/add-ons/bsurfaces-gpl-edition/
  - https://github.com/CGCookie/retopoflow
  - https://exoside.com/quadremesher/
  - https://github.com/wjakob/instant-meshes
  - https://docs.blender.org/manual/en/latest/modeling/meshes/retopology.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# retopo-addons

Goal: speed up retopology with the right tool for the asset type.

## Bsurfaces GPL Edition (free; bundled to 4.1, extension afterwards)

A modeling and retopology tool for creating surfaces from strokes drawn across the high poly. Its panel is in the Edit Mode sidebar, *Edit* tab. The Blender 4.1 manual page for it is only a stub, and the extension is offered with limited support, so follow the add-on's own panel for the current stroke workflow.

## RetopoFlow (Orange Turbine, formerly CG Cookie; paid on Blender Market and Superhive, GPL-3.0 source on GitHub)

A suite of sketch-based retopology tools whose geometry snaps to your high poly objects as you draw. Its documentation covers Contours, PolyStrips, PolyPen, Strokes, Patches, Loops, Knife, Tweak, Relax and Select.

## Auto-retopology

- **Quad Remesher** (Exoside, paid, with a one-month trial): automatic quad remesher (auto retopology) offered as a Blender plugin among other applications.
- **Instant Meshes** (external field-aligned mesh generator; source on GitHub, check its licence): remesh outside Blender and bring the result back.
- **Core Blender**: the *Remesh* panel in Object Data (*Voxel* and *Quad* modes, Quad being QuadriFlow); the manual notes automatic remesh results generally do not suit deformation, so use them for static props.

## When manual still wins

Faces and hands for animation, joints, game assets with tight budgets: auto results rarely give correct loops. Common hybrid: auto-remesh for bodies and clothes, manual for face and hands (`creative-arts.animation.blender.face-topology`).

## Gotchas

- Add-on versions lag Blender releases; check compatibility before upgrading Blender mid-project.

## Verify

Final topology passes the same checks as manual retopo: quads, loops around deforming areas, budget met, no non-manifold edges (Select → Select All by Trait → Non Manifold finds nothing unintended).

## Checked

2026-10-27. Sources: Blender 4.1 manual add-on pages (Bsurfaces GPL Edition, LoopTools), Blender manual 5.2 Retopology page, extensions.blender.org listing for Bsurfaces GPL Edition (id bsurfaces_gpl_edition, compatible with 4.3 and newer), the CGCookie/retopoflow GitHub README, docs folder and blender_manifest.toml, the wjakob/instant-meshes repository description, and the Exoside Quad Remesher page. Confirmed: Bsurfaces location and bundled-to-4.1 history; RetopoFlow owner, sales channels, GPL-3.0 code and tool list; Quad Remesher paid with one-month trial; Select All by Trait > Non Manifold menu path. Corrected: the Bsurfaces menu path (it is a sidebar panel) and the RetopoFlow owner. Removed: Quad Remesher guide details, the Instant Meshes OBJ workflow, RetopoFlow symmetry and value claims, and the unsourced manifold-input gotcha.

Method: documentation only; no commands were run.
