---
id: creative-arts.animation.texturing.painter-texture-sets
name: painter-texture-sets
category: creative-arts
field: animation
product: texturing
tags: [texture-sets, substance-painter, material-id, texture-set-list, uv-tiles, mesh-import, project-configuration, adobe-substance-3d]
level: practitioner
status: draft
description: "Plan and manage Substance 3D Painter texture sets: material assignments on import, splitting/merging sets, per-set resolution and channels, UDIM tiles."
sources:
  - https://helpx.adobe.com/substance-3d-painter/interface/texture-set.html
  - https://helpx.adobe.com/substance-3d-painter/project-management/project-configuration.html
  - https://helpx.adobe.com/substance-3d-painter/project-management/udim.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Painter texture sets

**Goal:** the right number of texture sets: each becomes a separate set of output maps and a separate
material in the engine/renderer. Too many sets cost draw calls and memory; too few force unrelated
surfaces to share resolution.

## Where sets come from

Painter creates one texture set per **material assigned in the mesh** (FBX/OBJ/GLTF/USD). Plan in the
DCC before export:
- Character: `body`, `head`, `clothes`, `hair`, `eyes` (eyes and hair often need different shaders).
- Prop: one material unless parts need different shaders (glass vs metal).
- Name materials clearly; the name becomes the texture set and output file prefix.

With **UDIM** ("Use UV Tile workflow" at project creation), each UV tile becomes its own texture within
a texture set; tiles can be painted across seamlessly.

## Texture Set Settings

Per set: resolution (can differ per set), channels (Base colour, Metallic, Roughness, Normal, Height,
Emissive, Opacity, user channels), mesh maps baked per set, UV padding settings.
- Add Opacity channel only where needed and use a shader with alpha.
- User channels (user0..7) for custom masks exported to the engine.

## Changing sets after import

- Re-import mesh (Edit - Project Configuration) keeps painting when material names stay the same;
  renaming a material creates a new empty set.
- Merge sets by giving parts the same material in the DCC and re-importing (layer stacks of merged
  sets do not merge automatically: copy layers manually).

## Gotchas

- Hidden/unused materials from the DCC still create sets; clean the export.
- Mirrored UVs on overlapping shells paint on both sides; fine for symmetric texture, wrong for text or
  asymmetry.
- Reimports with changed UVs keep painting only if "Preserve strokes positions on mesh" is enabled
  (projection re-maps; check results).

## Verify

Texture Set list shows the planned sets with expected names and resolutions; a test export produces one
map group per set with matching prefixes.
