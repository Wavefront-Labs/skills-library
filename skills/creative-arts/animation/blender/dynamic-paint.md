---
id: creative-arts.animation.blender.dynamic-paint
name: dynamic-paint
category: creative-arts
field: animation
product: blender
tags: [blender, dynamic-paint, dynamic-paint-canvas, brush, canvas, wetmap, footprints, ripples, waves, displace, weight-maps, image-sequence-bake, physics]
level: advanced
status: docs-checked
description: "Blender Dynamic Paint canvases and brushes for footprints, wet maps, ripples and reveal masks: surface types, vertex vs image output, drying, baking."
sources:
  - https://docs.blender.org/manual/en/latest/physics/dynamic_paint/index.html
  - https://docs.blender.org/manual/en/latest/physics/dynamic_paint/canvas.html
  - https://docs.blender.org/manual/en/latest/physics/dynamic_paint/brush.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# dynamic-paint

Goal: let one object (brush) write data onto another (canvas) over time — colour, displacement, weights or waves — and use that data in shaders, modifiers or exports.

## Model

Physics → **Dynamic Paint** → *Canvas* or *Brush*. A canvas holds **surfaces** (`+` for several); each surface has a *Format* (**Vertex** — stored on the canvas mesh as colour attributes/vertex groups/displacement; **Image Sequence** — baked to PNG/EXR files via UVs) and a *Surface Type*:
- **Paint** — colour + wetness (vertex colour layers `dp_paintmap` and `dp_wetmap`, or image files).
- **Displace** — outputs brush intersection depth: on Vertex format it dents the canvas mesh (*Max Displace*, *Displace Factor*, *Incremental*); on Image Sequence format the Output panel shows *Displace Type* (Displacement/Depth) and *Max Displace*.
- **Weight** — writes a vertex group (footstep masks for grass bending, snow compression via Displace modifier, mask for shader).
- **Waves** — a 2D wave sim on the surface: *Open Borders*, *Timescale*, *Speed*, *Damping*, *Spring*, *Smoothness*; output is displacement — ripples from objects touching water.

Canvas *Frame Start/End*, *Sub-Steps* (extra samples between frames, needed for very fast brushes), *Anti-Aliasing*, *Dissolve* (surface returns to its original state over *Time* frames, *Slow* = logarithmic; not offered on Waves surfaces), *Dry* (Paint surfaces: wetness decays over *Time* frames, *Slow*), **Output** panel (vertex format: pick the colour attribute / vertex group by name; a red name means the layer does not exist yet, use the `+` button to create it; Displace and Waves surfaces in Vertex format have no Output panel), **Cache** panel (Vertex format only: point cache Bake / Free). Image Sequence format: the Output panel has *Bake Image Sequence*, *Cache Path*, *UV Map*, *File Format* (PNG or OpenEXR) and *Premultiply Alpha*; Paint surfaces add *Paintmaps* and *Wetmaps* sub-panels, each with a *Name* and a checkbox.

Brush: *Paint* source (Mesh Volume / Mesh Volume + Proximity / Proximity / Object Center / Particle System), *Paint Color*, *Alpha*, *Wetness*; *Absolute Alpha*, *Erase Paint* (brush removes paint instead). For the proximity-based sources: *Distance*, *Falloff* (Smooth, Constant or Color Ramp) and *Project* with a *Ray Direction* (Canvas Normal, Brush Normal or Z-Axis); Mesh Volume + Proximity adds *Inner Proximity* and *Negate Volume*. **Velocity** panel: *Multiply Alpha*, *Replace Color*, *Multiply Depth* (all driven by a colour ramp over brush speed, measured in units per frame) and *Do Smudge* with *Smudge Strength*. **Waves** panel for Waves surfaces: *Wave Type* (Depth Change / Obstacle / Force / Reflect Only), *Factor*, *Clamp Waves*. Particle System source: choose a particle system on the brush object, then *Effect Solid Radius* (or *Use Particle's Radius*) and *Smooth Radius*.

## Recipes

**Footprints in snow/sand (vertex, displace + weight):**
1. Ground: a plane subdivided densely (Vertex format needs a highly subdivided mesh), Canvas → surface *Displace*, *Max Displace* 0.05, *Incremental* on if prints should deepen; add a second surface of type *Weight* and create its vertex group with the Output `+` button.
2. Feet: Brush, *Paint* source *Mesh Volume + Proximity*, *Distance* 0.02. Feet must actually intersect/approach the ground vertices.
3. Use the weight vertex group as a mask in a modifier's *Vertex Group* field for extra crumble or shading control.
4. Bake the cache (Canvas → Cache → Bake).

**Wet map / rain splashes on a street (image sequence paint):**
Street UV-unwrapped (no overlaps); Canvas surface *Paint*, Format *Image Sequence*, *UV Map* set, *Resolution* 2048, *Dissolve* off, *Dry* on (Time 60). Brush: a particle system of rain drops as *Particle System* source with *Wetness* 1. *Bake Image Sequence* writes the wetmap images named in the Wetmaps panel. Shader: Image Texture with the sequence as source and *Auto Refresh* → Roughness mix/darkening.

**Paint reveal / ink spreading:** canvas Paint with *Dissolve* off, brush *Object Center* with *Proximity* and a *Ramp* falloff, animate the empty over the surface; use the paintmap as a mix factor between two materials.

**Ripples (Waves):** water plane dense (150×150), surface *Waves*, *Speed* 1, *Damping* 0.04, *Spring* 0.2; floating object as Brush with *Wave Type: Depth Change*; outputs displacement live. Add Subsurf after for smooth crests; bake for stable playback.

**Grass bending by characters:** Canvas Weight surface on the ground, brush = character collider mesh with Proximity; the vertex group can drive a particle system's *Vertex Group* inputs (for example *Length*).

## Baking and output

- Vertex surfaces: results are stored by the point cache (see `creative-arts.animation.blender.file-management`) and shown in the viewport.
- Image sequences: *Bake Image Sequence* writes UV-wrapped image files of the chosen resolution; *Cache Path* can be blend-relative (`//`); paintmap and wetmap are separate outputs; *File Format* is PNG or OpenEXR.

## Gotchas

- Nothing happens: the Output layer name is red (layer not created, press `+`); the brush does not reach the canvas vertices (vertex format resolution too low — paint is per vertex); Frame Start/End wrong; the canvas surface's *Brush Collection* excludes the brush.
- Image format needs clean UVs inside 0–1, no overlaps; the result has a 1 px seam unless *Anti-Aliasing* and the shader's bleed cover it.
- Fast brushes skip vertices — raise *Sub-Steps*.
- Dissolve and Dry times are in frames, so changing fps changes the look.
- The default vertex layers are `dp_paintmap`, `dp_wetmap` (Face Corner Byte colour attributes) and `dp_weight` for Weight surfaces.
- Spread, Drip and Shrink effects exist only on Paint surfaces.

## Verify

- With the brush intersecting the canvas, Solid → *Attribute* colour or Weight Paint mode shows marks appearing frame by frame.
- Displace surface visibly dents the mesh and *Incremental* deepens on repeated passes.
- After *Bake*, scrubbing backwards shows the same state; the Timeline cache bar is solid.
- Image sequence files exist and load into an Image Texture node as a sequence that advances with the frame.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (physics/dynamic_paint pages, branch blender-v5.2-release) and the 5.2 source (rna_dynamicpaint.cc, dynamicpaint.cc, properties_physics_dynamicpaint.py). Confirmed: surface formats and types; Dissolve/Dry panels (Time, Slow; Dissolve hidden on Waves); Output panel contents per format; default layer names dp_paintmap, dp_wetmap, dp_weight and Face Corner Byte colour; brush Source options (Distance, Falloff Smooth/Constant/Color Ramp, Project with Ray Direction, Inner Proximity, Negate Volume); Velocity and Waves panels; Effects only on Paint surfaces.

Method: documentation only; no commands were run.
