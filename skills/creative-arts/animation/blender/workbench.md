---
id: creative-arts.animation.blender.workbench
name: workbench
category: creative-arts
field: animation
product: blender
tags: [blender, workbench, playblast, viewport-render, solid-shading, matcap, cavity, studio-light, dailies, animation-review, outline, random-color, opengl-render]
level: practitioner
status: docs-checked
description: "Blender Workbench engine and Viewport Render for playblasts and clay review: lighting, colour, shadow, cavity, outline, sampling."
sources:
  - https://docs.blender.org/manual/en/latest/render/workbench/index.html
  - https://docs.blender.org/manual/en/latest/render/workbench/options.html
  - https://docs.blender.org/manual/en/latest/render/workbench/lighting.html
  - https://docs.blender.org/manual/en/latest/render/workbench/color.html
  - https://docs.blender.org/manual/en/latest/render/workbench/sampling.html
  - https://docs.blender.org/manual/en/latest/editors/3dview/viewport_render.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# workbench

Goal: a fast image sequence of what the viewport shows, for animation review, turntables and layout approvals, without a full render.

## Two ways to get it

1. **Viewport Render**: renders the current viewport (Solid mode uses the Workbench render settings, Material Preview uses EEVEE's). It works only for Workbench and EEVEE, not Cycles. It also uses the scene Resolution, Aspect, Output path and File format.
   - Still: 3D Viewport View menu, Render Viewport Preview. Animation: Render Playblast. Only keyed frames: Render Playblast on Keyframes (frames without a key still get written, repeating the last rendered frame).
   - If you are not in the active camera view a virtual camera matches your perspective; enter the camera view with Numpad 0. Esc aborts.
   - Disable overlays to drop rigs, empties and other clutter. Render Regions can limit the area.
2. **Workbench as the Render Engine** (Render properties): usable for final-render output with the Render-tab settings, but the manual says it is not intended for final images of a project.

Workbench does not use scene lights and does not use shader nodes.

## Settings (Render properties; same as the viewport Shading popover)

- **Lighting:** *Flat* (no highlights or shadows); *Studio* (predefined setups such as key plus rim light; by default lights follow the viewport camera, *World Space Lighting* fixes them in place, *Rotation* turns them on Z); *MatCap* (image with lighting baked in, shaded by normal direction relative to the camera; flip button; custom MatCaps are loaded in Preferences).
- **Color:** *Material* (Material Viewport Display colour), *Object* (Object Viewport Display colour), *Random* (a colour per object), *Attribute* (active Color Attribute, falling back to the object Viewport Display colour), *Texture* (active image texture with the active UV map), *Custom* (single chosen colour for the whole scene).
- **Options:** Backface Culling; X-Ray (slider sets transparency); Shadow (sharp shadow with Darkness 0 to 1, Light Direction, Shadow Shift to limit self-shadowing artifacts, Shadow Focus for edge falloff); Depth of Field (uses the active camera's DoF settings, only visible through the camera); Outline (colour adjustable); Specular Highlighting (only with Studio lighting or a MatCap that has a specular pass); Cavity (Type World = more precise but slower, Screen = fast but ignores feature size, Both; Ridge and Valley control visibility).
- **Sampling:** No anti-aliasing, Single Pass (post-process), or Multisample (steps 5, 8, 11, 16, 32; suited to small detail like hair). The 3D Viewport method is a user preference; viewport-render and final-render settings are saved per scene.

## Review recipe

1. Enter the camera view (Numpad 0), set Output resolution and format.
2. Set Lighting to Studio, enable World Space Lighting if you want lights fixed rather than following the view, Color to Random or Material, turn on Shadow and Cavity as needed.
3. View, Render Playblast.

## Gotchas

- Viewport Render needs the 3D Viewport active and renders its view, not necessarily the camera.
- Cavity World is slower than Screen; prefer Screen for long animations.
- Studio lights follow the viewport camera unless World Space Lighting is on, so lighting appears to move relative to the object.
- X-Ray left on makes the whole render transparent.

## Checked

Method: 2026-11-09 read the Blender manual source for the render/workbench pages (index, options, lighting, color, sampling) and viewport_render; removed unstated claims (timings, CLI flags, FFmpeg settings, Film Transparent, passes, turntable numbers) and corrected menu names.
