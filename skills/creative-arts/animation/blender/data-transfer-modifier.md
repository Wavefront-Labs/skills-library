---
id: creative-arts.animation.blender.data-transfer-modifier
name: data-transfer-modifier
category: creative-arts
field: animation
product: blender
tags: [blender, data-transfer, normal-transfer, vertex-weight-proximity, vertex-weight-mix, vertex-weight-edit, transfer-weights, transfer-uvs, custom-normals, modify-modifiers, uv-project, uv-warp, weighted-normal]
level: advanced
status: docs-checked
description: "Blender Data Transfer, Vertex Weight Edit/Mix/Proximity, Weighted Normal, Normal Edit, UV Project and UV Warp modifiers: settings, mapping methods and pitfalls."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/modify/data_transfer.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/modify/weight_proximity.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/modify/weight_mix.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/modify/weight_edit.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/modify/uv_project.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/modify/uv_warp.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/normals/weighted_normal.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/normals/normal_edit.html
licence: Apache-2.0
version: 5
updated: 2026-11-17
aliases: []
---

# data-transfer-modifier

Goal: copy per-element data between meshes and build vertex-group masks procedurally instead of painting them twice.

## Data Transfer

*Source* object → target (the modifier's owner). Toggle the data types to copy (vertex groups, UV maps, colour attributes, custom normals, Freestyle Mark and so on); *Layer Selection* picks all source layers or one, *Layer Mapping* matches destination layers by name or order.

Per data type a **Mapping** method:
- Vertices: *Nearest Vertex*, *Nearest Edge Vertex*, *Nearest Face Vertex*, *Nearest Edge Interpolated*, *Nearest Face Interpolated* (interpolates between the vertices of the nearest face), *Projected Face Interpolated*, *Topology* (matches by index: same element count and order).
- Corners: *Nearest Corner and Best Matching Normal*, *Nearest Corner and Best Matching Face Normal*, *Nearest Corner of Nearest Face*, *Nearest Face Interpolated*, *Projected Face Interpolated*.
- *Max Distance* (tick to ignore far geometry), *Ray Radius* (starting radius of the ray casts used by some mappings), *Islands Precision* (stops a face taking UVs from different source UV islands; 0.0 means no island handling), *Mix Mode* (Replace / Above Threshold / Below Threshold / Mix / Add / Subtract / Multiply), *Mix Factor* (a threshold for the Above/Below modes), *Vertex Group* (per-element control of Mix Factor, with *Invert*).
- **Object Transform** (axes icon beside the source): takes both objects' world transforms into account. Untick it if the source and destination do not overlap in world space; then the modifier treats them as sharing one position with default rotation and scale.

Workflows:
1. **Weights from body to clothing:** clothing gets Armature (same rig) + Data Transfer (source body, Vertex Data → Vertex Groups, *All Layers*, *Nearest Face Interpolated*). Click **Generate Data Layers** so the groups exist on the target (the modifier does not create missing layers itself, and the layers it adds stay behind when you remove the modifier).
2. **Custom normals from a smooth proxy:** low-poly foliage cards get normals from a sphere/blob (Face Corner → Custom Normals, *Nearest Corner and Best Matching Face Normal*); leaves shade as one volume instead of individual planes.
3. **Normals from a hero mesh to a low-res game mesh**: source hi-res, *Nearest Corner and Best Matching Normal*, Max Distance small.
4. **UVs between topologically similar meshes:** Face Corner → UVs, *Nearest Face Interpolated*; for identical topology use *Topology*.
5. **Vertex colour / AO bake sharing:** paint on one, transfer to variants.

One-shot alternative: the Transfer Mesh Data operator (linked from the modifier's manual page) copies the same data without a modifier.

## Vertex Weight Edit / Mix / Proximity

These make and modify vertex groups dynamically; they feed Armature, Displace, Shrinkwrap, GN and Cloth *pin* groups.

- **Vertex Weight Edit:** *Vertex Group*, *Default Weight* for vertices not in the group, *Group Add/Remove* (add vertices above *Add Threshold*, remove those below *Remove Threshold*), *Normalize Weights*, *Falloff Type* (Linear, Custom Curve, Sharp, Smooth, Root, Sphere, Random, Median Step; *Invert*), and the shared influence settings (*Global Influence* plus a vertex group or texture mask). Weights are clamped to 0.0-1.0. Use: invert a mask, remap a gradient, apply a curve to a painted mask.
- **Vertex Weight Mix:** two groups A and B, *Vertex Set* (All / A / B / A or B / A and B — which verts to affect), *Mix Mode* (Replace / Add / Subtract / Multiply / Divide / Difference / Average / Minimum / Maximum), *Default Weight A/B*, *Invert Weights A/B*. Use: subtract a "hands" group from "arm" to make a clean cloth pin mask; union masks; `Mix Mode: Replace` with *Vertex Set: All* to write group B's weights into A.
- **Vertex Weight Proximity:** sets weights from distance to a *Target Object* (*Proximity Mode: Object* uses the origin-to-origin distance, so every affected vertex gets the same weight; *Geometry* measures from each vertex to the target's Vertex/Edge/Face, the shortest distance winning if several are enabled), *Lowest* (distance mapped to weight 0.0) and *Highest* (weight 1.0), *Falloff* type, *Normalize Weights*. Use: a moving Empty melts/dissolves part of a mesh (feed into Displace or a shader via *Attribute* node), a character's hand pushing a blanket (pin group fades near the hand), auto-weight the area near a prop.

Stack trick: Vertex Weight Proximity → Vertex Weight Edit (falloff curve) → Displace/Mask/Shrinkwrap using the group. Masks update per frame with no painting. In Geometry Nodes the equivalents are *Geometry Proximity* + *Map Range* + *Store Named Attribute* and are usually clearer for new work.

## Weighted Normal

Recomputes custom normals weighted by *Face Area*, *Corner Angle*, or *Face Area and Angle*; *Weight* (50 weights all faces uniformly; above 50 favours larger areas or angles, below 50 does the opposite), *Threshold* (areas or angles closer than this get equal weights), *Keep Sharp* (preserves Sharp edges), *Face Influence* (uses weak/medium/strong face weights from the Set Strength tool or the Bevel modifier's Set Strength mode), *Vertex Group*.

## Normal Edit

Generates custom normals *Radial* (radiating from the object's origin or an optional *Target* object; the foliage trick without a source mesh) or *Directional* (all normals converge on a mandatory *Target*; *Parallel Normals* makes them parallel to the line between the two origins). *Mix Mode*, *Mix Factor* and *Max Angle* blend with existing normals; *Vertex Group* gives per-item control; *Offset* shifts the origin used for generation.

## UV Project / UV Warp

- **UV Project:** projects a UV map from up to ten *Projector* objects, emitting down each projector's negative Z axis (a camera projector follows its perspective/orthographic setting; *Aspect X/Y* and *Scale X/Y* apply only to cameras). Perspective projection onto low-poly geometry can show artefacts; subdividing reduces them. Camera mapping/matte painting: project a plate through the shot camera onto geometry, then bake the projected texture to a proper UV (`creative-arts.animation.blender.texture-baking`). Decal projection from an empty.
- **UV Warp:** offsets/rotates/scales a UV map using *Offset*, *Scale*, *Rotation* and *UV Center*, driven by the difference between the *From* and *To* objects or bones, with a *Vertex Group* for per-vertex influence; animate the empty to scroll a texture (conveyor belts, eye textures on a flat face), or use bone-driven UV offset for 2D-face rigs (`creative-arts.animation.blender.facial-rig`).

## Gotchas

- Data Transfer of vertex groups may not work until **Generate Data Layers** has created the missing layers.
- Custom normals transfer ignores faces more than *Max Distance* away if ticked; untick for whole-object transfers.
- Vertex Weight Proximity in *Object* mode measures between origins (an empty or camera target also falls back to its origin); use *Geometry* mode with *Face* for a true surface.
- The three Vertex Weight modifiers clamp weights to 0.0-1.0; disable one to see the original weights in Weight Paint mode.

## Verify

- Weight paint view (after Apply or with *Show in Edit Mode* + weight overlay) shows transferred weights without seams between body and cloth at the waistline.
- Custom-normal foliage: Overlay → Normals shows corner normals radiating from the proxy centre; shading has no per-card seams.
- Proximity mask: scrubbing the target empty changes the Displace/Mask live; Spreadsheet (`creative-arts.animation.blender.spreadsheet-editor`) shows weights 0→1 over the set distance range.

## Checked

2026-10-28. Confirmed against the Blender manual pages for the Data Transfer, Vertex Weight Edit/Mix/Proximity, Weighted Normal, Normal Edit, UV Project and UV Warp modifiers: mapping method names per data type, Mix Mode lists, Object Transform, Generate Data Layers, Islands Precision, Max Distance, Ray Radius, weight-modifier options and clamping, UV Project's ten projectors and camera-only Aspect/Scale, Weighted Normal and Normal Edit options. Removed or corrected: data-category lists and the material-index claim, a default mapping claim, shortcut and menu paths, Auto Smooth and version statements, the bevel-plus-Weighted-Normal recipe, stack-order and evaluated-mesh claims, export claims, and the wrong Falloff, Mix Factor and Parallel Offset names.
Method: documentation only; no commands were run.
