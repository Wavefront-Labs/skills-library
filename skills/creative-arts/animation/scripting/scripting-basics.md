---
id: creative-arts.animation.scripting.scripting-basics
name: scripting-basics
category: creative-arts
field: animation
product: scripting
tags: [scripting, blender, bpy, python, automation, data-driven, headless, modifiers, keyframing, append-link]
level: advanced
status: draft
description: "Blender Python (bpy) for a data-driven headless pipeline: scene/object/material creation, modifiers, keyframing, append/link, and the gotchas that bite."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SKILL: Blender Python (bpy) scripting basics — the data-driven headless pipeline

**What it is:** driving Blender entirely from Python so a whole series is built by code,
not by hand. Sets, characters, lip-sync, and shots are each a script
(`series/production/blender/build_*.py`) run headless; a shotlist JSON feeds data in.
Scripting is what makes a one-person 10-episode show possible: the asset is the script,
and the `.blend` is its deterministic output.

## 1. Run headless and pass data in
```bash
blender -b --python build_mainst_set.py                 # background, run script
blender -b --python build_chip_talk.py -- rhubarb.json out/ 24 57   # args after --
```
- `-b` / `--background`: no UI; required for a render farm / batch.
- Everything **after `--`** is your script's argv. Read it with:
  ```python
  import sys
  argv = sys.argv[sys.argv.index("--") + 1:]   # ['rhubarb.json', 'out/', '24', '57']
  ```
  This is how one generic shot script renders any shot from its shotlist row.
- Exit code: an uncaught exception makes Blender exit non-zero — good, your batch
  runner can detect a failed build. Print a `DONE` sentinel at the end so logs are
  greppable.

## 2. Start from a known-empty scene
Never trust the startup file. Begin every build script with:
```python
import bpy, os, math
bpy.ops.wm.read_factory_settings(use_empty=True)   # clean, empty, reproducible
scene = bpy.context.scene
```
`use_empty=True` drops the default cube/camera/light so your scene is exactly what the
script makes — the whole point of a deterministic pipeline.

## 3. Create objects — ops put the result in the active object
`bpy.ops.mesh.primitive_*_add()` creates and *selects/activates* the new object; grab
it immediately:
```python
def box(name, loc, sc):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object            # the just-created object
    o.name = name; o.scale = sc
    bpy.ops.object.transform_apply(scale=True)   # bake scale into the mesh
    return o
```
- **Apply transforms** (`transform_apply`) after scaling primitives so modifiers,
  outlines, and physics see real geometry, not a scaled bounding box.
- Reassign collections explicitly (`for c in o.users_collection: c.objects.unlink(o)`
  then `target_coll.objects.link(o)`) — ops drop objects into the active collection by
  default, which is rarely where you want them. Use collections per sub-group
  (`ground`, `buildings`, `props`) so shots can toggle parts.

## 4. Materials are node graphs, built in code
Cel look = a fixed node recipe applied by a helper (`cel_mat()` in the build scripts):
```python
def cel_mat(name, rgba, shadow):
    mat = bpy.data.materials.new(name); mat.use_nodes = True
    nt = mat.node_tree; nt.nodes.clear()
    out  = nt.nodes.new('ShaderNodeOutputMaterial')
    diff = nt.nodes.new('ShaderNodeBsdfDiffuse'); diff.inputs['Color'].default_value = rgba
    s2r  = nt.nodes.new('ShaderNodeShaderToRGB')       # EEVEE Next only
    ramp = nt.nodes.new('ShaderNodeValToRGB'); ramp.color_ramp.interpolation = 'CONSTANT'
    nt.links.new(diff.outputs['BSDF'], s2r.inputs['Shader'])
    nt.links.new(s2r.outputs['Color'], ramp.inputs['Fac'])
    # ...Multiply by base colour → Emission → output...
    return mat
```
- Address inputs/outputs **by name** (`inputs['Color']`), not index — indices shift
  between Blender versions.
- `interpolation = 'CONSTANT'` on the ColorRamp is what makes the hard toon banding
  (no gradient between shadow and light).
- Clear a mesh's slots before assigning (`o.data.materials.clear()`) so you don't stack
  stale slots when re-running.

## 5. Modifiers in code (outlines, subsurf, arrays)
```python
m = o.modifiers.new('ol', 'SOLIDIFY')         # inverted-hull outline
m.thickness = 0.03; m.use_flip_normals = True; m.material_offset = idx; m.use_rim = False
```
- **Inverted-hull outline** = a Solidify with flipped normals + a black backface-culled
  emission material; cheapest cel ink line, and it renders headless (Freestyle is the
  alternative but slower).
- `ARRAY` for repeating modular pieces (lampposts, storefronts); `SUBSURF` for smooth
  hero forms — but see the subsurf gotcha below.

## 6. Keyframing (for lip-sync, cameras, FX)
```python
o.hide_viewport = False
o.keyframe_insert(data_path="hide_render", frame=12)
# hard swaps (viseme visibility): set constant interpolation
for fc in o.animation_data.action.fcurves:
    for kp in fc.keyframe_points:
        kp.interpolation = 'CONSTANT'
scene.frame_start = 1; scene.frame_end = dur_frames
```
Lip-sync (`build_chip_talk.py`) keyframes each of 9 viseme mouths' visibility from the
Rhubarb `mouthCues` JSON with **constant interpolation** = instant mouth swaps, not a
tween. Camera moves use `BEZIER`; mechanical swaps use `CONSTANT`.

## 7. Append vs link (reuse locked assets)
Shots must not rebuild sets/characters — they pull the locked `.blend`:
```python
with bpy.data.libraries.load("assets/sets/mainst.blend", link=False) as (src, dst):
    dst.collections = [c for c in src.collections if c == "buildings"]
for c in dst.collections:
    scene.collection.children.link(c)
```
- `link=False` = **append** (copy into this file, editable per shot — usual for shots).
- `link=True` = **link** (reference; edits propagate from the source — for assets you
  want to update globally). Linked data is read-only here; override only if you must.

## 8. Render settings + save
```python
scene.render.engine = 'BLENDER_EEVEE_NEXT'      # cel look needs ShaderToRGB
scene.view_settings.view_transform = 'Standard' # not Filmic/AgX — keeps flat toon colour
scene.eevee.taa_render_samples = 24
scene.render.resolution_x = 1280; scene.render.resolution_y = 720
scene.render.filepath = os.path.join(OUT, "frame_")
bpy.ops.render.render(write_still=True)                      # still
bpy.ops.wm.save_as_mainfile(filepath="assets/sets/mainst.blend")  # lock the asset
```

## 9. HARD-WON GOTCHAS (don't repeat the pilot's bugs)
- **`filepath` must be absolute — use `bpy.path.abspath()`.** Relative `//foo.png`
  resolves against the *.blend's* directory, which in a headless `--python` run with no
  saved file is unpredictable. Build output paths with `os.path.join(ABS_DIR, name)` or
  wrap with `bpy.path.abspath()`.
- **Deselect before join.** `bpy.ops.object.join()` merges *all selected* objects into
  the active one. If a stray object is selected (ops leave things selected), you silently
  weld it in. Always `bpy.ops.object.select_all(action='DESELECT')`, then select exactly
  the parts to join and set the keeper active last.
- **Subsurf detaches disjoint islands.** A `SUBSURF` modifier on a mesh made of separate,
  non-welded islands rounds each island independently, so they pull apart and leave gaps
  at the seams. Either merge-by-distance the vertices first
  (`bpy.ops.mesh.remove_doubles()` in edit mode) so it's one watertight island, or keep
  the detail pieces as separate objects and don't subsurf across the join.
- **Ops act on context, not arguments.** `bpy.ops.*` operate on the active object /
  selection / mode, not on an object you pass. In headless runs set the state first
  (select, activate, `bpy.ops.object.mode_set(mode='EDIT')`) or the op no-ops or throws
  a "context incorrect" error. Prefer the data API (`o.modifiers.new`, `mesh.vertices`)
  over ops where one exists — it's context-free and more reliable headless.
- **Clear materials / collections on re-run** so repeated builds are deterministic, not
  cumulative.

## 10. Build reusable asset scripts
Factor the repeated work into helpers (`box`, `cyl`, `cone`, `cel_mat`, `emit_mat`,
`outline`) at the top of each script, and keep them identical across build scripts so
every asset shares one material recipe and one outline treatment. A new set is then a
few dozen lines of "place these primitives"; the look comes for free and stays
on-model. Drive per-shot variation from the shotlist JSON argv, never by editing the
script.

## Verify
- [ ] Script runs clean via `blender -b --python <f>.py` and exits 0 with a `DONE` print.
- [ ] Scene starts from `read_factory_settings(use_empty=True)` — output is exactly what
      the code makes.
- [ ] All output `filepath`s are absolute (`bpy.path.abspath` / `os.path.join`), not `//`.
- [ ] Transforms applied after scaling; objects in the intended collections.
- [ ] Joins preceded by an explicit deselect; no stray objects welded in.
- [ ] Any subsurfed mesh is one welded island (or detail kept as separate objects).
- [ ] Re-running the script yields an identical `.blend` (materials/collections cleared,
      not stacked).
- [ ] Locked asset saved with `save_as_mainfile`; shots append/link it, never rebuild.

See also: `../environment-design/set-building.md`, `../blender/cel-shading`,
`../pipeline/shot-episode-structure.md`.
