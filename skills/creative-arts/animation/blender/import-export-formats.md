---
id: creative-arts.animation.blender.import-export-formats
name: import-export-formats
category: creative-arts
field: animation
product: blender
tags: [blender, import-export, fbx, gltf, glb, usd, alembic, abc, obj-export, stl, ply, svg, interchange, unity, unreal, game-export, axis-conversion, unit-scale]
level: advanced
status: docs-checked
description: "Move assets in and out of Blender cleanly: FBX, glTF, USD, Alembic, OBJ/STL/PLY/SVG settings, axis and unit conversion, armature and animation export, and what each keeps."
sources:
  - https://docs.blender.org/manual/en/latest/files/import_export/fbx.html
  - https://docs.blender.org/manual/en/latest/files/import_export/fbx_legacy.html
  - https://docs.blender.org/manual/en/latest/addons/scene_gltf2.html
  - https://docs.blender.org/manual/en/latest/files/import_export/usd.html
  - https://docs.blender.org/manual/en/latest/files/import_export/alembic.html
  - https://docs.blender.org/manual/en/latest/files/import_export/obj.html
  - https://docs.blender.org/manual/en/latest/files/import_export/stl.html
  - https://docs.blender.org/manual/en/latest/files/import_export/svg_curve.html
  - https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html
licence: Apache-2.0
version: 5
updated: 2026-11-17
aliases: []
---

# import-export-formats

Goal: pick the right interchange format for the destination and set the exporter so the result opens correctly the first time.

## Choosing the format (practice guidance, not from documentation)

| Destination | Format | Why |
|---|---|---|
| Unity, Unreal, Godot (static + skeletal) | **FBX** (or glTF for Godot/three.js) | skeleton, skin weights, shape keys, animation clips |
| Web, three.js, Godot, AR, Sketchfab | **glTF 2.0 (.glb)** | PBR materials travel, compact, open spec |
| Houdini, Maya, Katana, Nuke 3D, Omniverse | **USD (.usd/.usdz)** | hierarchy, materials (UsdPreviewSurface), animation, instancing |
| Cached deforming geometry (cloth, fluid, animated mesh) to any DCC | **Alembic (.abc)** | per-frame vertex positions, no rig needed |
| Static geometry to CAD/3D print/slicers | **OBJ** / **STL** / **PLY** | OBJ keeps UVs+materials (mtl); STL mesh only; PLY keeps vertex colour |
| 2D vector artwork in | **SVG** (curves) / Grease Pencil import | Illustrator/Inkscape logos become curves |
| Volumes | **OpenVDB** | see `creative-arts.animation.blender.volume-objects` |

Blender's node-tree materials only transfer through the Principled BSDF: the USD exporter converts a Principled node tree to USD Preview Surface (the manual says only simple trees of Diffuse BSDF, Principled BSDF, Image Textures, UVMap and Separate RGB nodes are supported), and the glTF exporter reads Principled inputs and Image Texture nodes. Procedural nodes do not export directly — bake first (`creative-arts.animation.blender.texture-baking`).

## Preparation (a practice checklist, applies to every format)

1. **Apply scale/rotation** (`Ctrl A`), especially on armatures. Non-applied scale is the #1 cause of 100× models in engines.
2. Units: Scene → Units → Metric, Unit Scale 1.0 is the simplest baseline. glTF 2.0 specifies metres for all linear distances; for FBX see *Apply Unit* and *Apply Scalings* below; check your engine's importer documentation for the rest.
3. Clean names (batch rename; no `.001` suffixes).
4. Triangulate only if the engine needs it; most importers triangulate. Leave n-gons out (Boolean leftovers tri-fan badly).
5. One UV map named consistently; a second only for lightmaps.
6. Delete unused material slots; one material = one draw call in engines.
7. Armature: rest pose applied, bone roll sane, no reliance on bendy bones (the USD exporter documents that bendy bones are not supported; check the other exporters), and deform bones identifiable (a `DEF-` naming set) or use *Only Deform Bones* in the FBX or USD exporter.

## FBX (`File → Export → FBX (.fbx)`; import is the native `File → Import → FBX (.fbx)`)

- **Limit to: Selected Objects**; *Object Types*: Armature + Mesh (untick Camera/Light/Empty unless needed).
- **Transform:** Scale 1.0 and *Apply Unit* on (defaults); *Apply Scalings* options are All Local, FBX Units Scale, FBX Custom Scale and FBX All, so pick per the target importer's behaviour; Forward `-Z`, Up `Y` are the exporter's defaults; leave **Apply Transform** off — its description says it is experimental and known to be broken with armatures/animations — and apply object rotation yourself instead.
- **Geometry:** *Smoothing* (Normals Only, Face, Edge or Smoothing Groups; the manual says Normals Only is generally most accurate if the importer supports custom split normals), *Apply Modifiers* (exports the evaluated mesh), *Tangent Space* if the engine needs tangents, *Triangulate Faces* if the target cannot handle non-triangle faces.
- **Armature:** *Primary Bone Axis Y, Secondary X* (default); *Add Leaf Bones* is on by default, untick it to drop the extra end bone per chain; *Only Deform Bones* (default off) for deform-only skeletons; Armature FBXNode Type is Null (default), Root or LimbNode — the add-on advises Null unless the other application has issues.
- **Baked Animation:** on by default; *Key All Bones*; *NLA Strips* (each non-muted strip becomes a take) and *All Actions* (each action becomes a take) decide the clips — all three default on; *Simplify* defaults to 1.0 (0 disables simplification, giving exact keys); *Force Start/End Keying* adds keys at the start and end of actions. See `fbx-animation-export`.
- Import (native importer): *Scale*, *Ignore Leaf Bones*, *Import Animation*, *Animation Offset*; *Manual Orientation* and *Automatic Bone Orientation* exist only in the deprecated *FBX (.fbx) (Legacy)* importer. Each FBX take imports as a separate Action with Action Slots.
- FBX limits (manual, Compatibility): constraints are exported only as their keyframed result; instanced objects are written as separate copies; NURBS surfaces, text and metaballs are converted to meshes on export.

## glTF 2.0 (`File → Export → glTF 2.0`)

- Format **glb** (single binary) for delivery; *Separate* (.gltf + .bin + textures) for editing in other tools.
- Include: *Selected Objects*, *Custom Properties* (exported as glTF extras), *Punctual Lights* (KHR_lights_punctual).
- Transform: `+Y Up` on (glTF is Y-up; exporter rotates correctly).
- Mesh: *Apply Modifiers* (exports the evaluated mesh), *UVs*, *Normals*, *Tangents*, *Vertex Color* options, *Loose Edges/Points* off.
- Materials: Principled-based; Base Color from an Image Texture or value; Metallic and Roughness: the manual recommends a Separate RGB node with the green (G) channel to Roughness and blue (B) to Metallic so the exporter can detect a packed texture. *Images* chooses the output format (PNG is lossless and generally preferred, JPEG gives smaller files, WebP optional); *Image Quality* applies to JPEG and WebP. Emission strength above 1 uses KHR_materials_emissive_strength. Transmission, volume, clearcoat, sheen and IOR map to KHR extensions.
- Animation: *Animation → Mode* is *Actions* (default; an action exports if it is the active action or is stashed in an NLA track, so stash the ones you want), *Active Actions Merged* (one animation from the active actions), *NLA Tracks* (each track is one glTF animation) or *Scene*; *Shape Keys* on for morph targets, plus *Shape Keys Animations*; *Bake All Objects Animations* when objects are constrained without being animated; *Sampling Rate* is how often animated values are evaluated, in frames; *Optimize Animation Size* removes duplicate keyframes.
- Skinning: *Bone influences* sets how many joint influences per vertex are exported; the manual warns models may appear incorrect in many viewers with a value other than 4 or 8 (limit weights in Blender first with Weights → Limit Total); *Export Deformation Bones only* is under Data → Armature.
- Mesh compression: Draco (*Data → Draco Compression*, KHR_draco_mesh_compression) and Meshopt options exist in newer releases (4.5.14 has the gltfpack-based `export_use_gltfpack` option instead and no `export_meshopt_compression_enable`); the receiving viewer must support the extension, so avoid them for DCC round-trips (practice).
- Import: *Bone Direction* chooses the heuristic for bone tips (the default does not change axes and is best for re-exporting from Blender; the manual notes the Fortune setting may be inaccurate with non-uniform scaling); *Guess Original Bind Pose* tries to recover the pose used to compute inverse bind matrices.

## USD (`File → Export → Universal Scene Description`)

- Extensions: the file extension chooses the USD flavour (`.usd`, `.usdz` and others; check the export dialog); `.usdz` is a zipped archive (UDIM textures cannot be included, and *USDZ Texture Downsampling* limits texture size).
- Export: *Selection Only*, *Animation* (exports the entire scene frame range; off exports only the current frame), *Use Settings for* (Viewport or Render visibility and modifiers), Object Types (Meshes, Lights, World Dome Light, Cameras, Curves, Point Clouds, Volumes, Hair), *UV Maps* and *Rename UV Maps* (exports the USD default name `st` instead of `UVMap`), *Normals*, *Materials* with *USD Preview Surface Network* and/or *MaterialX Network*, *Export Textures* (Keep, Preserve or New Path; New Path writes a `textures` folder next to the file), *Root Prim* (the Python default is `/root`), *Convert Orientation* (Forward/Up axis conversion; off by default), *Units* (`metersPerUnit`), *Triangulate*, and *Instancing* under Experimental (off by default).
- Import: *Path Mask* imports only the subset of the stage rooted at a primitive; Geometry options for UV Coordinates, Color Attributes and Mesh Attributes; *USD Shapes*; *Light Intensity Scale*; *Import USD Preview* converts USD Preview Surface to Principled BSDF (lossy). Animated transforms get a Transform Cache constraint and animated geometry gets a Mesh Sequence Cache modifier; USD file sequences (one file per frame) are not supported. A Y-up stage is rotated automatically to Blender's Z-up.
- USD keeps hierarchy and transforms, cameras (perspective only), lights, and custom attributes (as USD attributes, in the `userProperties` namespace by default). Node trees convert only through USD Preview Surface or MaterialX. *Armatures* export as USD skeletons and skinned meshes (bendy bones not supported; other modifiers are not applied) and *Shape Keys* as USD blend shapes (absolute shape keys unsupported).
- For a round-trip with other USD tools keep a consistent *Root Prim*, set *Convert Orientation*/*Units* to what the other tool expects, and tick *Relative Paths* for external files (practice).

## Alembic (`File → Export → Alembic`)

- Export: *Selection Only*, *Frame Start/End* (default: scene range), *Sub-frame Sampling* (*Samples Transform* and *Geometry*, with *Shutter Open/Close* between -1 and 1; the manual's motion-blur example uses 5 samples at -0.25 to 0.25), *Use Instancing*, *Custom Properties*, *Flatten Hierarchy* (drop parent relations; world-space transforms), *Settings* Render or Viewport, *UV Coordinates*, *Merge UVs*, *Normals*, *Color Attributes*, *Face Sets* (material names per face; the material data itself is not exported), *Subdivisions* (*Apply* bakes subsurf; *Use Schema* writes the SubD schema), *Triangulate*, *Export Hair* and *Export Particles*, *Scale*.
- Import: *Scale*, *Relative Path*, *Set Frame Range*, *Is Sequence* (cache split into separate files), *Validate Meshes*, *Always Add Cache Reader*; time-varying meshes get a **Mesh Sequence Cache** modifier and animated transforms get a **Transform Cache** constraint.
- Alembic = baked deformation: use for cloth/hair/fluid results and for sending animated characters to a lighting file without rigs. Alembic has no support for armatures or particle systems (hair exports as animated zero-width curves, particles as animated points).

## OBJ / STL / PLY / SVG

- OBJ: *Forward Axis* / *Up Axis* conversion (Blender is Y Forward, Z Up), *Apply Modifiers*, *UV*, *Normals*, *Colors* (writes the active vertex colour attribute), *Triangulated Mesh*, *Curves as NURBS*, *Materials* writes an MTL library (*PBR Extensions* adds roughness, metallic, sheen, clearcoat, anisotropy and transmission), *Animation* exports the frame range.
- STL: *Scale* and *Scene Unit* (applies the scene's unit as defined by unit scale) — confirm the unit your slicer expects (practice) — *Apply Modifiers*, *Format: ASCII* (off writes binary), *Batch* (one file per object). Check the mesh is manifold before printing (practice).
- PLY: options include *Vertex Colors*, *Normals* and *ASCII* output (see the manual's PLY page); commonly used for scans and point clouds (practice).
- SVG import (`File → Import → SVG as Curves (.svg)`) creates curve objects in the XY plane scaled by the SVG document units; only path geometry is imported (gradients, fills, strokes, text, images and filters are ignored). Convert curves to meshes or extrude them as needed. A separate Grease Pencil SVG import exists (see the manual's Grease Pencil SVG page).

## Scripting exports

```python
import bpy
bpy.ops.export_scene.fbx(filepath="//export/char.fbx", use_selection=True,
    object_types={'ARMATURE','MESH'}, apply_scale_options='FBX_SCALE_UNITS',
    add_leaf_bones=False, use_armature_deform_only=True, bake_anim=True,
    bake_anim_use_nla_strips=False, bake_anim_use_all_actions=True, bake_anim_simplify_factor=0.0)
bpy.ops.export_scene.gltf(filepath="//export/char.glb", export_format='GLB',
    use_selection=True, export_apply=False, export_animation_mode='ACTIONS', export_draco_mesh_compression_enable=False)
bpy.ops.wm.usd_export(filepath="//export/asset.usdc", selected_objects_only=True, export_materials=True, export_textures_mode='NEW')
bpy.ops.wm.alembic_export(filepath="//export/cloth.abc", selected=True, start=1001, end=1100, vcolors=True, face_sets=True)
```
Operator arguments change between versions — check the Python API reference for your release (for example `bpy.ops.wm.usd_export` now takes `export_textures_mode`, not a boolean).

## Gotchas

- An unexpected -90 degree X rotation on an imported root usually means an axis-conversion mismatch (practice); the FBX *Apply Transform* option is experimental and broken with armatures/animations, so fix axes with Forward/Up instead.
- Too many bone influences per vertex: limit weights (Weights → Limit Total) to what the engine or glTF *Bone influences* setting allows.
- Procedural shader nodes do not export; bake them to image textures.
- Alembic export of constrained objects: the manual's *Settings* option (Render or Viewport) controls which modifier and visibility state is used; bake constraints first if results differ (practice).
- Re-importing your own FBX does not round-trip exactly (the importer notes bone-orientation heuristics); keep the .blend as the source of truth (practice).

## Verify

- Import the exported file into a **fresh** Blender: scale 1, origin correct, normals outward (Face Orientation overlay all blue), materials visible, animation clips named and playing.
- Open in the real target (Unity, Unreal, a glTF viewer, a USD viewer): bone count matches the deform bones, no unwanted leaf bones, morph targets listed, textures linked.

## Checked

2026-10-27. Documentation release: Blender manual 5.2 (branch blender-v5.2-release), the Python API reference (current), the FBX and glTF add-on sources from the same branch, and the Khronos glTF 2.0 specification (section 3.4: metres, +Y up). Confirmed: FBX exporter option names and defaults (add-on source), native FBX importer options and takes-as-actions (fbx.rst), USD export/import option names and limitations (usd.rst), Alembic export/import options (alembic.rst), OBJ, STL and SVG options, glTF animation modes, skinning and compression options (scene_gltf2.rst), and the keyword arguments of bpy.ops.wm.usd_export, wm.alembic_export and export_scene.fbx. Wrong in the old text: Apply Transform advice for FBX (experimental, broken with armatures/animations), Add Leaf Bones default, there is no Group by NLA Track glTF option (modes are Actions, Active Actions Merged, NLA Tracks, Scene), usd_export has no export_textures boolean (it is export_textures_mode), several USD and Alembic option names (Visible Only, Pack UV Islands, Prim Path Mask, Evaluation Mode) differ or are absent from the manual, and Temperance is not a glTF Bone Direction name in the manual. Removed unconfirmed performance figures (Draco 5-10x), engine-specific import advice and tool names.

Run check, 2026-11-01, Blender 4.5.14 LTS headless: the keyword arguments used in the scripting example for export_scene.fbx (add_leaf_bones, use_armature_deform_only, bake_anim_use_nla_strips, bake_anim_use_all_actions, bake_anim_simplify_factor, apply_scale_options) and export_scene.gltf (export_format 'GLB', use_selection, export_apply, export_animation_mode 'ACTIONS', export_draco_mesh_compression_enable) exist; glTF animation modes in 4.5.14 are Actions, Active Actions, Broadcast, NLA Tracks and Scene (Broadcast is not in the list above); export_influence_nb defaults to 4; glTF Include flags export_extras and export_lights default off; wm.fbx_import has global_scale, ignore_leaf_bones, use_anim and anim_offset and no orientation options; export_scene.gltf has no Meshopt property. The USD, Alembic, OBJ, STL, PLY and SVG parts were not run, so this skill stays docs-checked.

Method: documentation, plus the operator properties listed above checked headless in Blender 4.5.14.
