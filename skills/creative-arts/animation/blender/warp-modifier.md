---
id: creative-arts.animation.blender.warp-modifier
name: warp-modifier
category: creative-arts
field: animation
product: blender
tags: [blender, warp-modifier, warp-deform, warp, modifiers, two-empty-deform, dent, magnet]
level: practitioner
status: verified
description: "Use Blender's Warp modifier as an animatable two-empty magnet: From/To objects, falloff type and radius, vertex group and texture masks for dents, bulges and local tweaks."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/warp.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# warp-modifier

Goal: deform a region "as if you grabbed it at point A and dragged it to point B", driven by two objects, with a smooth falloff — for dents, bulges, art-directed bumps, and finger-poke effects without sculpting.

## Setup

1. Add two Empties, *From* and *To*, at the same location on the surface.
2. *Modifiers → Deform → Warp*: *Object From* = empty A, *Object To* = empty B (the two objects' origins define the points; the *From* point is pulled toward the *To* point, much like Proportional Editing).
3. Set **Strength**, a **Falloff Type** (Blender 4.5: None, Curve, Smooth, Sphere, Root, Inverse Square, Sharp, Linear, Constant; the Proportional Editing types without Random, plus None and Curve) and **Radius**, the distance from the transforms that can be warped.
4. Move the *To* object: vertices near *From* follow, blending out towards *Radius*. *Preserve Volume* enables volume preservation when rotating one of the transforms.

Masks: **Vertex Group** (with invert) and **Texture** (see the common masking options in the manual) control which vertices are affected and how much.

## Recipes

These recipes are practice, not from the manual; tune the numbers by eye.

- **Finger poke on a soft body**: From/To parented to the hand bone; *To* slightly below the surface; a small Radius with a smooth falloff.
- **Car door dent**: From on panel, To pushed slightly inward, a sharper falloff.
- **Breathing chest cheat**: To scaled slightly with keyframes, From at sternum.
- **Eye-bulge on a cartoon**: To scaled; combine with Vertex Group of the eye region.
- **Parented pair**: parent *To* to *From* so one controls position and the other the offset.

## Gotchas

- Both empties at different locations on creation = immediate deformation; create them coincident then move *To*.
- Practice, not from the manual: Warp before Subdivision for speed; after it for smoother results on low-poly meshes.
- Warp needs no vertex group to pick the region, so it is a handy interactive stand-in for Proportional Editing on meshes still being edited (the manual notes its use case is rather small).

## Verify

- Move *To* back onto *From* (for example Shift S, Selection to Active): the mesh is undeformed.
- Falloff ring is visible as a smooth circle when *To* is pushed inward in wireframe.
- Keyframed *To* produces a clean ease with no popping (check in Graph Editor).

## Checked

2026-10-27, Blender manual, branch blender-v5.2-release (raw RST, projects.blender.org/blender/blender-manual). Confirmed against modeling/modifiers/deform/warp.rst: Object From/To, Preserve Volume, Strength, Vertex Group with Invert, Falloff Type (defers to Proportional Editing), Radius, Texture masking. Removed unconfirmed Bone fields, texture coordinate list, falloff list, stacking claims and numeric recipe values (now marked practice).

Run check, 2026-11-01, Blender 4.5.14 LTS headless: with From and To empties coincident the largest vertex displacement was 6e-8 (undeformed); moving To by 0.5 moved the vertices by up to 0.5; no vertex group or texture is needed to deform; an inverted full-weight vertex group left the mesh untouched; the falloff enum is the list given above; Bone From/To and a Texture Coordinates setting also exist.

Method: manual text confirmed from documentation; Warp behaviour run headless in Blender 4.5.14.
