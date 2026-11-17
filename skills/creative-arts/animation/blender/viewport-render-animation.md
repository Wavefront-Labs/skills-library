---
id: creative-arts.animation.blender.viewport-render-animation
name: viewport-render-animation
category: creative-arts
field: animation
product: blender
tags: [blender, workbench, viewport-render-animation, viewport-render-image, playblast, viewport-render]
level: practitioner
status: docs-checked
description: "Make fast playblasts with View > Render Viewport Preview, Render Playblast and Render Playblast on Keyframes: which settings they use, overlays, output path and metadata stamps."
sources:
  - https://docs.blender.org/manual/en/latest/editors/3dview/viewport_render.html
  - https://docs.blender.org/manual/en/latest/render/output/properties/output.html
  - https://docs.blender.org/manual/en/latest/render/output/properties/metadata.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# viewport-render-animation

Goal: render exactly what the viewport shows to images or a movie, quickly.

## How

3D Viewport > **View > Render Viewport Preview** (still), **Render Playblast** (animation) and **Render Playblast on Keyframes**. The last renders only frames where the selected objects have a key; the other frames are still written to the output, repeating the last rendered frame (the first frame is always rendered). Esc aborts.

It uses:
- The current viewport settings. Solid mode uses Workbench render settings; Material Preview uses EEVEE settings. It works for Workbench and EEVEE only, not Cycles.
- The camera view if the viewport is in camera view (Numpad 0), otherwise a virtual camera matching the current perspective.
- Overlays as shown; disable overlays for a render without rigs and empties. Render Regions can limit the area.
- Output Properties: Resolution, Aspect, output path and file format.
- Both Playblast operators raise an error if automatic render output is disabled in the Output panel header.

## Dailies recipe (practice)

1. Camera view, overlays off (or only the ones you want), Solid with the Workbench settings you want.
2. Output: reduced Resolution %, Media Type Video with a common container and codec, frame rate matching the scene.
3. Output Properties > Metadata: enable the fields you need (Frame, Scene, Camera, Filename, Note) and **Burn into Image**.
4. View > Render Playblast. The file is at the output path.

## Gotchas

- Hidden-in-viewport objects do not appear, because viewport visibility applies (practice).
- Speed follows the viewport; a lower resolution percentage helps.

## Verify

Play back the movie: frame count equals the range and the stamp is visible.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release): editors/3dview/viewport_render.rst (menu names Render Viewport Preview, Render Playblast, Render Playblast on Keyframes, Workbench/EEVEE only, keyframe behaviour, camera, overlays tip), output.rst (Playblast error when render output is disabled), metadata.rst (Burn into Image). Fixed wrong menu names (the old skill used Viewport Render Image/Animation/Keyframes) and removed the Material Preview HDRI claim and Simplify advice. Method: documentation only; no commands were run.
