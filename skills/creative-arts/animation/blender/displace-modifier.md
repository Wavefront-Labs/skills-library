---
id: creative-arts.animation.blender.displace-modifier
name: displace-modifier
category: creative-arts
field: animation
product: blender
tags: [blender, displace-modifier, modifiers, deform, height-map, terrain, texture-coordinates]
level: practitioner
status: verified
description: "Push vertices by a texture with Blender's Displace modifier: direction, Strength and Midlevel maths, texture coordinates (UV, Object, Global, Local), vertex group."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/displace.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/common_options.html
  - https://docs.blender.org/manual/en/latest/render/materials/legacy_textures/index.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# displace-modifier

Goal: displace vertices by texture intensity as real geometry (terrain from a height map, bumpy ground, rough rock, animated ripples), unlike shader bump.

## Setup

*Add Modifier > Deform > Displace*. The **Texture** field takes a texture data-block (procedural or image), created and edited in the Texture Properties tab; the properties icon next to the field jumps there. If the field is empty the modifier uses 1.0 (white).

- **Direction**: *X/Y/Z* (one axis), *Normal* (vertex normal), *Custom Normal* (averaged custom normals), *RGB to XYZ* (red moves along X, green along Y, blue along Z, i.e. vector displacement).
- **Space**: with X/Y/Z (or RGB to XYZ) directions, displace along local or global axes.
- **Strength** and **Midlevel**: displacement = texture value - Midlevel, then vertex offset = displacement x Strength. Values below Midlevel move negatively, above it positively; a negative Strength inverts the effect. Texture values run 0.0-1.0, not 0-255.
- **Vertex Group** (+ Invert): influence per vertex; empty means all vertices equally.

## Texture coordinates and channel

- **UV** (+ UV Map): from face UVs. Falls back to Local if the object has no UVs; a blank UV Map field uses the active one. Each vertex takes its UV from the first face found using it, so non-contiguous UVs can cause artefacts.
- **Object**: from another object's coordinate system; moving that object changes the mapping. To keep the displacement while moving the modified object, parent the coordinate object to it.
- **Global**: world coordinates. **Local**: the object's own coordinates.
- **Use Channel**: described in the 5.2 manual (Intensity as the average of RGB, Red, Green, Blue or Alpha). The Blender 4.5.14 Displace modifier has no channel property (the texture's intensity is used), so expect intensity only on that version.

## Density

The modifier moves existing vertices only, so a flat plane needs subdivision first for detail. Compare a subdivision modifier before it with one after it.

## Verify

Strength 0 returns the original shape; with Midlevel matching the texture's neutral value flat regions stay put.

## Checked

Date: 2026-10-27. Documentation release: Blender manual, 5.2 release branch (Displace page, Common Options page; the legacy textures page was confirmed to exist). Confirmed: direction options, Space, the Strength/Midlevel formulas, coordinate options and fallbacks, Use Channel. Removed the texture-type list, default Midlevel, numeric recipes and unconfirmed bit-depth, normal and shading claims.

Run check, 2026-11-01, Blender 4.5.14 LTS headless: Displace with Python: Direction X, Y, Z, Normal (default), Custom Normal, RGB to XYZ; Space Local (default) and Global (a rotated object displaced along its local X in Local space and along global X in Global space); Strength 1.0 and Midlevel 0.5 defaults; with no texture the offset was (1 - Midlevel) x Strength (0.5, and 1.5 for Midlevel 0.25 with Strength 2, -1.5 for Strength -2); Strength 0 changed nothing; a vertex group limited the effect and Invert reversed it; a Blend texture with Local coordinates followed the mesh while Global changed when the object moved and Object changed when the coordinate object moved; UV on a mesh without UVs fell back to Local coordinates, and a blank UV Map field used the active UV layer (a named layer used its own UVs). Not run: Use Channel (not in 4.5.14) and the dense-mesh advice (practice).

Method: manual text confirmed from documentation; behaviour run headless in Blender 4.5.14.
