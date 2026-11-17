---
id: creative-arts.animation.blender.character-blockout
name: character-blockout
category: creative-arts
field: animation
product: blender
tags: [blender, blockout, primitives, character, cel, bezier, turnaround, proportions]
level: practitioner
status: verified
description: "Block a stylized character from primitives headless: half-extent scale law, bezier face features, emissive screen, ortho turnaround."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SKILL: Character blockout from primitives (scripted) — expert

Block a stylized character in Blender **from primitives, headless/scripted**, cel-shade
+ outline it, and render an orthographic turnaround — in one deterministic builder.
This is the pro-right-sized maquette+model step for geometric/stylized casts (collapses
2D-turnaround→model when you are designer+modeler). Verified on a production character.
Pairs: `character-design/model-sheet-turnaround`, `cel-shading`, `character-modeling`.

## Workflow
1. Read the design LOCK (proportions in heads, shapes, hex, materials, do/don't).
2. Build each body part as a primitive at its locked position; assign cel material.
3. Facial features: emissive screen/eyes + a **curve** for the mouth (see below).
4. Per-object inverted-hull outline (skip on emissive face bits & screen).
5. Parent everything to a turntable **Empty**; rotate it to render front/side/back/¾.
6. Save the .blend as the locked asset. Renders ARE the de-facto model sheet.

## GOTCHAS (hard-won, verified)
- **Primitive scale convention:** `primitive_cube_add(size=1)` is **±0.5** (1 unit
  across). After `obj.scale=(sx,sy,sz)` + `transform_apply`, half-width = `0.5*sx`.
  (Mis-reading this as ±1.0 put Pixel's LIVE dot outside the head.) `uv_sphere_add`
  radius default 1 → ±1 before scale, so a sphere with scale 0.1 is 0.2 across.
  **Always reason in half-extent = radius×scale (sphere) or 0.5×scale (cube).**
- **Smile/curved features = a Bezier CURVE, not a torus.** A torus renders a full
  ring (reads as a surprised "O"). Use a 3-point bezier, ends up / middle down for a
  smile (∪), with `bevel_depth` for thickness:
  ```python
  mc = bpy.data.curves.new('mouth','CURVE'); mc.dimensions='3D'
  mc.bevel_depth=0.016; mc.bevel_resolution=4
  sp=mc.splines.new('BEZIER'); sp.bezier_points.add(2)
  for bp,(x,y,z) in zip(sp.bezier_points,[(-0.14,0,0.04),(0,0,-0.03),(0.14,0,0.04)]):
      bp.co=(x,y,z); bp.handle_left_type=bp.handle_right_type='AUTO'
  o=bpy.data.objects.new('mouth',mc); bpy.context.scene.collection.objects.link(o)
  o.location=(...); o.data.materials.append(mint)   # curves have no polygons/outline
  ```
  Curves render in EEVEE with bevel; they have NO `.data.polygons` → exclude from the
  smooth-shade loop and the solidify-outline helper (handle separately).
- **Emissive face features need NO outline** and should sit *proud* of the screen
  plane (nudge toward camera a few mm) so they don't z-fight the glass.
- **Outline helper** (per closed mesh): Solidify, `use_flip_normals=True`, thickness
  ~0.015–0.02 (world units; small body = small thickness), `material_offset` → a
  black emission material with `use_backface_culling=True`. Thickness is world-scale,
  so pick one value per character and reuse (line-weight = brand; see cel-shading).
- **Turntable render:** parent all parts to an Empty at origin; set
  `pivot.rotation_euler=(0,0,radians(deg))`, `view_layer.update()`, render each view.
  Cleaner than moving the camera. ortho cam: `cam.data.type='ORTHO'`, tune `ortho_scale`
  to frame height; `film_transparent=True` for clean sheets on alpha.
- **Smooth shading:** `for p in obj.data.polygons: p.use_smooth=True` on round parts
  (spheres/cylinders) so the cel terminator is a clean curve, not faceted.

## Cel material (recap, see cel-shading for full)
`Diffuse → Shader to RGB → ColorRamp(CONSTANT, shadow hue-shifted blue) → MixRGB
MULTIPLY over base → Emission → Output`. Emissive parts (screens, HUD, mint face):
plain `Emission` (strength 2.5–3). `view_transform='Standard'`, EEVEE Next, samples 16.
- Node idnames: `ShaderNodeShaderToRGB`, `ShaderNodeValToRGB` (ramp),
  `ShaderNodeMixRGB` (still valid in 4.5), `ShaderNodeBsdfDiffuse`, `ShaderNodeEmission`.
- **sRGB→linear the hex** (`c**2.2`) before feeding as default_value, or saturated
  toon colors wash out.

## Build helpers (pattern)
```python
def add(obj, mat, do_outline=True):      # mesh parts only
    obj.data.materials.clear(); obj.data.materials.append(mat)
    for p in obj.data.polygons: p.use_smooth = True
    if do_outline: outline(obj)
    parts.append(obj); return obj
```
`cube/sph/cyl` wrappers: add primitive, name, set scale, `transform_apply(scale=True)`
so modifiers/outline read true size.

## When to stop blockout → go to real model
Blockout proves silhouette + look + colors. Promote to final when you need: clean
edge-flow for deformation (retopo), a face rig beyond swapped states, or cloth.
For a shader-faced character (Pixel), the blockout mesh may be near-final; a deforming
organic character (Ivy) needs proper topology (character-modeling) after the blockout
confirms proportions.

## Self-check
- [ ] Reasoned every position/size in correct half-extents (cube ±0.5×scale)?
- [ ] Reads as the design's silhouette from front AND side?
- [ ] Face/curved features via bezier curve, emissive, proud of screen, no outline?
- [ ] One outline thickness, reused; emissive bits excluded?
- [ ] Turntable Empty renders front/side/back/¾ aligned?
- [ ] .blend saved as locked asset; renders archived as the model sheet?

Verified build: `scratchpad/build_pixel_blockout.py` → `assets/chars/pixel_blockout.blend`.
