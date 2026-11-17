---
id: creative-arts.animation.blender.sculpt-retopo
name: sculpt-retopo
category: creative-arts
field: animation
product: blender
tags: [blender, sculpt, retopo, hero-model, subsurf, boolean, join, cel, murder-drones]
level: practitioner
status: verified
description: "Turn a blockout into a hero model headless: unify meshes, carve eye sockets, subsurf only continuous meshes, one clean outline."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sculpt / Retopo — hero characters (cel/MD style, headless-first)

Turning a proportion blockout into a HERO model: one clean unified form with a
real face, that deforms and reads as a designed character — not a snowman of
visible primitives. Target = Murder Drones tier, which is **clean stylized forms
with strong shading, NOT hyper-detailed ZBrush sculpts.** That's the key
liberation: our ceiling is reachable with careful geometry + subdivision,
headless, no manual sculpting marathon.

## The honest constraint
True interactive sculpt→retopo is a GUI, many-hours, artist-in-the-seat craft.
We work headless (python). So we DON'T chase photoreal pores. We chase the MD
look, which is: smooth simple volumes, big expressive eyes set INTO the face,
clean continuous silhouette, bold shapes. All of that is procedural-friendly.

## Why a blockout reads as "cheap" (diagnosed on Dill v1)
1. **Disjoint primitives** — each sphere/cylinder gets its own outline → a
   snowman of stacked rings instead of one body contour.
2. **Features sit ON the surface** — eye spheres poke out of a flat face plane
   instead of nestling in sockets.
3. **No unifying smoothness** — hard primitive boundaries visible under shade.

## The headless hero recipe (fixes all three)
1. **Build the forms** as primitives (blockout proportions, already locked).
2. **Join per silhouette group**, not per part: all body/clothing skin into ONE
   mesh; head+neck into one; keep eyes/brows/mouth as separate FEATURE objects.
   `bpy.ops.object.join()` after selecting a group + setting an active target.
3. **Unify the surface**: add **Subdivision Surface** (viewport+render levels
   1–2) for smooth stylized volumes. For a fully seamless blobby form (MD robots)
   use **Remesh (VOXEL, ~0.03)** or a **Skin+Subsurf** on an edge skeleton
   instead of join — voxel remesh welds overlapping primitives into one manifold.
4. **ONE outline per group** — Solidify (flip normals, black backface-culled
   emission) on the joined mesh → a single clean contour, the MD silhouette.
5. **Eyes into sockets** — don't float eye spheres in front of the face. Boolean
   a shallow socket into the head, or recess the eye so the lid/brow geometry
   overlaps its upper edge. Big eyes = appeal; set them IN.
6. **Face**: brows + mouth as thin curve/mesh features parented to the head, so
   they drive expression & visemes (see lip-sync). Keep a nose plane/ridge for
   3/4 read.
7. **Cel shade** every group (Shader-to-RGB ramp, see cel-shading); internal
   material borders can carry line via Freestyle or a shader edge pass later —
   v1 silhouette outline is enough.

## Headless gotchas (verified building hero Dill)
- **Subdivision Surface SHRINKS & DETACHES disjoint joined islands.** Join does
  NOT weld verts, so subsurf treats each primitive as its own cage and pulls it
  toward its own centre → gaps open at every joint (snowman falls apart). Only
  subsurf a CONTINUOUS mesh (e.g. a single-sphere head worked great at level 2).
  For a body of overlapping primitives: JOIN, NO subsurf, keep them overlapping →
  one outline, connected read. If you need smoothing across the join, weld first
  (Remesh VOXEL, or Merge-by-Distance in edit mode) then subsurf.
- **`bpy.ops.object.join()` eats ALL selected objects, not just the ones you
  think.** Always `bpy.ops.object.select_all(action='DESELECT')` first, then
  select your group. A stray-selected object silently merges in and its geometry
  appears flung far from the group (bit me: a hair join spanned to x=-0.74).

## Deformation / retopo note
For shots needing real body deformation (walk, big gesture), the unified subsurf
mesh rigs fine with an armature + automatic weights (see rigging). True edge-loop
retopo for clean deformation is only needed if auto-weights pinch at joints —
upgrade that joint's loops then, not speculatively.

## Verify
- [ ] Silhouette is ONE continuous contour per character (no stacked rings).
- [ ] Eyes nestle into the face (not floating proud of it).
- [ ] Surface reads smooth under cel shade (no primitive seams).
- [ ] Face has brow+mouth features that can key expression/visemes.
- [ ] Still matches the design lock (proportions, palette, the one asymmetry).

See character-blockout (proportions), cel-shading, rigging, lip-sync.
