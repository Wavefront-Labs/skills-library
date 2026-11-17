---
id: creative-arts.animation.blender.multires-shape-keys
name: multires-shape-keys
category: creative-arts
field: animation
product: blender
tags: [blender, multires-shape-keys, multires-armature, multiresolution, shape-keys, rigging, sculpted-characters]
level: practitioner
status: docs-checked
description: "Combine Multiresolution with armatures and shape keys in Blender: modifier order, deform modifiers on multires levels, baking from Multires and topology limits."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/multiresolution.html
  - https://docs.blender.org/manual/en/latest/animation/shape_keys/workflow.html
  - https://docs.blender.org/manual/en/latest/animation/shape_keys/shape_keys_panel.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# multires-shape-keys

Goal: an animated character that keeps sculpted detail, with sculpted shape keys on the base mesh.

## Armature and other deform modifiers

- Multires has to come before modifiers that change geometry. Deform modifiers (for example Armature) placed after it are applied to the multires subdivision levels instead of the base mesh, which is accurate but heavier.
- For animation keep **Levels Viewport** low and **Render** high; the Render level is the detailed one at render time.
- To keep a light animation mesh, bake the sculpted detail instead: Multires supports baking Normals, Displacement and Vector Displacement through Bake from Multires in the Render panel. It compares two levels: Viewport Levels as the low-resolution base and Render Levels as the high-resolution detail. For a correct bake set Viewport Levels to 0, Render Levels to the highest sculpt level with the wanted detail, UV unwrap the object and select an Image Texture node to receive the bake. Use 16-bit or 32-bit formats for displacement and Non-Color for the image.

## Shape keys

- Shape keys live on the mesh data and are edited in Properties > Object Data > Shape Keys. Each key stores positions for every vertex.
- A shape key cannot add or remove vertices. Finalize topology before creating keys; adding vertices later is technically possible (existing keys record new vertices at their creation position) but not recommended.
- The panel's key operations (New Combined, New from Objects, Flip, Make Basis, Apply to Basis) are described in `creative-arts.animation.blender.blendshape-sculpting`.
- Remeshing ignores shape keys and is not possible with a Multires modifier, so decide on topology first.

## Gotchas

- Changing the base mesh topology breaks Multires detail, and also conflicts with shape keys that were created for the old topology.
- Plan the order: finalize topology, sculpt Multires detail, then create the shape keys on the base mesh.

## Verify

Pose the rig and move a shape key slider: the surface deforms without detail tearing. A bake compared at level 0 and the top level shows the sculpted detail in the normal map.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release branch). Confirmed against modeling/modifiers/generate/multiresolution (modifier order, deform modifiers after Multires, Bake from Multires requirements and bake types), animation/shape_keys/workflow and shape_keys_panel (topology guidance), and meshes/retopology (no remeshing with Multires, shape keys ignored). Removed unconfirmed claims about tangent-space storage, per-shape-key multires detail, sculpting a shape key at level 0 and the Apply Multires first rule.
Method: documentation only; no commands were run.
