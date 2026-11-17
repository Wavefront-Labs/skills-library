---
id: creative-arts.animation.blender.normal-editing-toon
name: normal-editing-toon
category: creative-arts
field: animation
product: blender
tags: [blender, normal-editing-toon, anime-face-normals, custom-normals, normal-edit-modifier, data-transfer-custom-normals, cel-shading]
level: advanced
status: draft
description: "Shape toon shading on anime faces by editing normals: transfer from a sphere or proxy, Normal Edit radial to a head empty, vertex groups for masks, and 4.1+ custom normal rules."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/normals/normal_edit.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/structure.html#modeling-meshes-normals-custom
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# normal-editing-toon

Goal: clean, graphic face shadows (no nose and cheek blotches) by replacing the face's shading normals with simpler ones.

## Method A: transfer from a proxy (most control)

1. Add a UV sphere or a smooth simplified head shape `NRM_proxy` around the face; sculpt it to the desired shading volume (rounder cheeks, flat front). Hide from render.
2. On the face: vertex group `face_normals` (skin of face, excluding lips/eyes edges and outline-critical borders, weighted 1 inside, fading at the border).
3. Data Transfer modifier: Source `NRM_proxy`, *Face Corner Data → Custom Normals*, *Mapping: Nearest Face Interpolated*, Vertex Group `face_normals`, *Object Transform* on. (Before 4.1 also enable Auto Smooth on the face mesh.)
4. Keep it high in the stack, before Subdivision (or after, with care; subdivision with custom normals needs 4.1+).

## Method B: Normal Edit radial

Normal Edit modifier, *Mode: Radial*, *Target* an empty at the head centre, vertex group mask, *Mix Factor* 0.5-1, Mix Mode Copy. Fast spherical normals; less sculptable than a proxy.

## Nose and mouth details

Exclude the nose tip and lips from the group or give them low weights so a small shading cue survives; many styles keep only a nose shadow drawn as a separate decal or texture.

## Gotchas

- Custom normals do not move geometry; an inverted-hull Solidify outline offsets along its own computed normals, so check outline thickness around the face after the transfer.
- Moving facial rig shapes: the proxy must deform with the head (parent to head bone or include in the armature deform) or shading slides.
- Exporting to engines: export custom normals (FBX *Normals: Face* plus custom split normals are exported by default) and verify in the engine.

## Verify

Rotate a key light around the head in Material Preview: shadow shapes are smooth, graphic and symmetrical; toggling the modifier shows the improvement; animation of the head keeps the shading stuck to the face.
