---
id: creative-arts.animation.blender.scene-strip-input
name: scene-strip-input
category: creative-arts
field: animation
product: blender
tags: [blender, scene-strips, scene-strip, scene-strip-input, sequencer-input, vse]
level: practitioner
status: docs-checked
description: "Use VSE scene strips with the right input: Camera renders the 3D scene, Sequencer uses that scene's own edit, plus camera override, render quality and nested edits."
sources:
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/strips/scene.html
  - https://docs.blender.org/manual/en/latest/editors/video_sequencer/sequencer/navigating.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# scene-strip-input

Goal: put 3D shots or other edits into an edit without rendering them first.

## Scene strip (Add > Scene)

Existing scenes are added from Add > Scene > scene name. Scene assets (including those in an Asset Library) also appear there and are appended or duplicated. Add > Scene > Empty Scene creates a new scene, with Type New, Copy Settings, Linked Copy or Full Copy.

Sidebar > Strip > Scene options:
- **Scene** and **View Layer** to render from.
- **Input**: **Camera** (use the scene's 3D camera) or **Sequencer** (use the scene's own sequencer timeline, so one scene can reuse another scene's edit; like a Meta strip, but supports multiple instances of the same data).
- **Camera**: override the scene's camera with any other object, to switch views inside a single scene.
- **Show**: Annotations (in non-render preview shading modes) and Transparent (a transparent background, useful for overlays such as Grease Pencil films).
- **Sound > Strip Volume**: volume of the audio taken from the chosen scene.

## Nested edits

A master scene with Scene strips set to Sequencer input, one per reel. Each reel scene has its own edit.

## Rendering

- The strip length is determined by the animation settings in the referenced scene. Use Strip > Update Scene Frame Range after changing that scene's length.
- The sequencer's Sequence Render Image and Sequence Render Animation do not render Scene strips by default; they use the preview shading mode. Use the Render menu in the top bar, or set Sidebar > View > Scene Strip Display > Shading to Rendered.
- Scene strips render only the Combined pass.
- Render shots to image sequences and replace the strips when full render quality is needed on every pass of the edit.

## Gotchas

- A Scene strip cannot reference the sequence's own scene. Use a secondary scene.
- Duplicating a strip with Shift D duplicates the scene; Alt D (linked) reuses the same scene.
- Trimming the strip handles changes which frames of the scene show.

## Verify

Play the edit: each scene strip shows the right camera and frame range, and a test render matches the preview timing.

## Checked

- Date: 2026-10-27. Documentation: Blender 5.2 manual (blender-v5.2-release branch of blender-manual).
- Confirmed: Add > Scene entries and new-scene types, Scene, View Layer, Input (Camera or Sequencer), Camera override, Show Annotations and Transparent, Sound Strip Volume, strip length from the scene, Update Scene Frame Range, Sequence Render note, Combined-pass limit, self-reference rule, Shift D versus Alt D behaviour. Removed the viewport-quality preview claim, the loop-prevention remark and the colour-management claim, which the manual does not state.
- Method: documentation only; no commands were run.
