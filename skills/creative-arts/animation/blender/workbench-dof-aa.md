---
id: creative-arts.animation.blender.workbench-dof-aa
name: workbench-dof-aa
category: creative-arts
field: animation
product: blender
tags: [blender, workbench, workbench-dof, workbench-aa, anti-aliasing, depth-of-field]
level: practitioner
status: docs-checked
description: "Set Workbench anti-aliasing for the viewport and for renders (Single Pass or multisample) and use camera depth of field, outline and X-ray options for clean reviews."
sources:
  - https://docs.blender.org/manual/en/latest/render/workbench/sampling.html
  - https://docs.blender.org/manual/en/latest/render/workbench/options.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# workbench-dof-aa

Goal: smooth Workbench output for reviews, turntables and model sheets.

## Anti-aliasing (Render Properties > Sampling, engine Workbench)

Per the manual, an anti-aliasing method can be chosen separately for the 3D Viewport, viewport rendering and final rendering:
- **No Anti-Aliasing**.
- **Single Pass Anti-Aliasing**: a post-process pass.
- **Multisample**: the scene is rendered multiple times with a slight offset; the sample counts are predefined: 5, 8, 11, 16, 32. The manual notes it suits small details such as hair.
- The 3D Viewport setting is a user preference (Preferences > Viewport) chosen for what runs best on your system. The viewport-render and final-render settings are saved per scene.
- In the viewport, one sample is rendered at a time and the next is rendered when nothing changes (progressive).

Higher sample counts cost more render time; compare a thin-wire test frame at a low and a high count and pick the lowest that looks steady.

## Depth of field (Render Properties > Options > Depth of Field)

The manual describes it as using the Depth of Field settings of the active camera in the viewport, visible only when looking through the camera. The settings (focus object or distance, F-Stop) live in Properties > Camera > Depth of Field. Check a test render before relying on it for final output, since the manual only documents the viewport case.

## Other Options panel items

Backface Culling, X-Ray (with a transparency slider), Shadow (Darkness, Light Direction, Shadow Shift, Shadow Focus), Outline, Specular Highlighting (Studio lighting or a MatCap with a specular pass), and Cavity (World, Screen or Both, with Ridge and Valley).

## Gotchas

- Outlines and wireframe overlays can crawl in motion at low sample counts.
- Viewport Render uses the viewport anti-aliasing preference while F12 uses the scene's render setting. Choose one path for dailies so the look stays consistent.

## Verify

Render a frame with a thin wire object at the lowest and highest chosen sample counts and compare edge stair-stepping.

## Checked

Date 2026-10-27. Blender manual 5.2 (blender-v5.2-release RST).
Confirmed: Workbench anti-aliasing methods and the multisample counts 5, 8, 11, 16, 32; per-context settings (user preference versus per scene); progressive viewport sampling; Options panel contents including Depth of Field wording.
Removed as unconfirmed: the "8 to 16 is enough, 32 for wireframe" guidance, "at least 8 samples or it looks dithered", the claim that DOF in Workbench matches final render focus pulls, and the exact Preferences path "Viewport > Quality".
Method: documentation only; no commands were run.
