---
id: creative-arts.animation.blender.render-aov-passes
name: render-aov-passes
category: creative-arts
field: animation
product: blender
tags: [blender, eevee-next, aov, render-passes, cryptomatte, mist, depth, emission, toon, data-passes, compositor, multilayer-exr]
level: advanced
status: docs-checked
description: "Render EEVEE shots as separable AOV/render passes (diffuse, emission, mist, cryptomatte, custom toon line/fill) for per-element control in comp."
sources: [https://docs.blender.org/manual/en/latest/render/layers/passes.html, https://docs.blender.org/manual/en/latest/render/eevee/world_settings.html, https://docs.blender.org/manual/en/latest/files/media/image_formats.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Rendering in passes (AOVs) from EEVEE

**Goal:** stop baking the shot into one flat RGB frame. Render each shot as a stack of separable passes so the
compositor can grade the character without touching the sky, isolate the screen-face glow, build depth fog and pick a
single prop with a pixel-exact mask, without re-rendering. This feeds `multipass-compositing`; the single-graph finish
lives in `compositing-grade`.

## Why passes
A comp tweak is far cheaper than a re-render, so defer aesthetic choices (glow strength, fog density, a
character-only grade) to comp. Render light and geometry truth once; make look decisions downstream. Passes are the
interface between the two.

## Pass taxonomy for a cel show
1. **Data passes** (not colour, never grade them): Mist, Depth, Vector, Normal, Position, Cryptomatte.
2. **Light/shading passes**: in EEVEE the manual lists Diffuse (Light, Color), Specular (Light, Color), Volume (Light),
   Emission, Environment, Shadow, Ambient Occlusion and Transparent. Cycles has a different, larger set (Direct/Indirect
   splits, Transmission, Shadow Catcher). Check what your engine and scene actually output before a comp depends on it.
3. **Custom AOVs** you author in the shader (for example `toon_line`, `toon_fill`, `rim`).

### Enable the standard passes
`Properties > View Layer > Passes`:
- **Depth** is distance to the nearest visible surface and can feed the Defocus node for fake depth of field. The manual
  warns it is noisy when the render itself uses depth of field or motion blur, and recommends Mist for a cleaner
  result. Depth, Position and the index passes are not anti-aliased.
- **Mist** maps distance to 0.0 to 1.0 and is controlled in the World tab: *Start* is the distance from the camera
  where mist begins to fade in, and *Depth* is the distance from Start over which it fades in (beyond Start + Depth
  objects are fully hidden). Set them so the ramp spans the shot, not infinity.
- **Cryptomatte** (Object, Material, Asset) is an image standard for masks. Unlike Object/Material Index it supports
  several objects per pixel and transparency, and works with other compositing software. *Asset* groups objects by
  parent and is unrelated to Blender's asset libraries. *Levels* is the maximum number of objects distinguished per
  pixel; the Render Layers node outputs half that many images (CryptoObject00, CryptoObject01...). Raise Levels when
  overlapping thin edges lose coverage.
- **Emission** is emission from directly visible surfaces. Tick it to isolate screen-faces and HUD for bloom.
- **Grease Pencil** pass outputs only the visible strokes and fills, for compositing them separately.

## Custom AOVs: toon line and fill
Keep line and fill separable so comp can thicken a line, recolour it per mood or remove it on one element.
1. Register the AOV in the *Shader AOV* panel of the view layer (Name, and Data Type: *Color* for colour/vector data,
   *Value* for a single number such as a mask).
2. Write to it from the material with an AOV Output node whose name matches. The name is used in both the AOV Output
   node and the Render Layers node and must not conflict with other enabled passes. Treat a name mismatch as a likely
   cause of a black pass.
3. Put the two AOV Output nodes in one shared node group appended to every character and prop, so every asset writes the
   same AOVs (locked-asset discipline from `character-consistency`).
A `Value` AOV such as `id_face` is a simple alternative to Cryptomatte when one recurring element needs isolating.

## Output: one multilayer EXR per frame
Do not render passes as separate PNG sequences. Use an OpenEXR multilayer format, one file per frame, so the
compositor's Render Layers/Image input exposes every layer from one file.
- OpenEXR output has Color Depth *Float (Half)* (16 bits per channel, floating point) or *Float (Full)* (32 bits), and
  a Codec choice. ZIP is lossless; DWAA/DWAB, Pxr24 and B44 are lossy variants, so avoid the lossy ones for data
  passes (Cryptomatte IDs and depth must stay exact).
- Keep the multilayer EXR as the shot's negative and derive the delivered frame from it.
- Estimate size from a test frame of your own and budget disk for the full shot.

## Headless pass setup
Configure passes once on the shot template's view layer, not per shot. The view layer properties named in the manual
include `use_pass_z`, `use_pass_mist`, `use_pass_emit`, `use_pass_cryptomatte_object`, `use_pass_cryptomatte_asset` and
`pass_cryptomatte_depth` (the Levels setting). AOVs are added with `bpy.ops.scene.view_layer_add_aov`. Every shot from
the template then carries the same pass stack, so the comp graph can assume those layers exist.

## Handoff to comp
- Combined is a sanity image; rebuild the look from component passes.
- Emission drives isolated glow so bloom hits only emissives.
- Mist/Depth drive depth fog, desaturation and Defocus decided in comp.
- Cryptomatte gives per-character and per-prop mattes for local grades.
- `toon_line` / `toon_fill` give line thickness and recolour without smearing.
Hand comp the EXR path plus a list of the custom AOVs.

## Motion blur and the Vector pass
The Vector pass holds screen-space motion vectors for the Vector Blur node (four components from next and previous
frames). The manual states it is disabled when Motion Blur is enabled in the render settings. So for comp-side blur,
leave render motion blur off and drive Vector Blur from the pass. Keep blur light on a cel line (`cel-shading`) and
test on a fast pan before relying on it for a hero shot.

## Gotchas
- EEVEE passes are not Cycles passes; do not design a graph around a pass your render does not produce.
- Mist is a 0 to 1 ramp over Start/Depth, not world distance: binary-looking fog means Depth is too short.
- The Emission pass includes every emissive surface, so a global bloom also blooms the HUD; mask with an ID AOV or
  Cryptomatte if it needs its own curve (see `hud-engagement-counter`).

## Verify
1. Render one frame with a character, a prop and depth. Open the EXR in the compositor and confirm the layer list
   includes Combined, Emission, Mist, Depth, CryptoObject00, `toon_line` and `toon_fill`.
2. Emission to a Viewer: only emissive surfaces are non-black.
3. Mist to a Viewer: a smooth ramp from the character to the far wall.
4. Cryptomatte node with the eyedropper: the character matte is white including hair edges, black elsewhere.
5. If a data pass looks lossy or banded, check the codec and colour depth.

## Checked
Date: 2026-11-01. Confirmed in the Blender manual Passes page (data, light, EEVEE, Cryptomatte, Shader AOV sections and
the bpy property anchors), the EEVEE World settings page (Mist Start, Depth, Falloff) and the image formats page
(OpenEXR Float (Half)/(Full) and codec list). Removed: render-time and file-size figures, a stated default Cryptomatte
level count, a denoiser claim, a software-version pin, an invented `world.mist_settings` code sample, and the
statement that the Vector pass is combined with render motion blur (the manual says the opposite).
Method: documentation only; no commands were run.
