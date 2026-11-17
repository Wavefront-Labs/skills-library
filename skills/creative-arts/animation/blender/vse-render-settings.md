---
id: creative-arts.animation.blender.vse-render-settings
name: vse-render-settings
category: creative-arts
field: animation
product: blender
tags: [blender, vse, sequencer, edit-render, vse-render-settings, sequencer-render]
level: practitioner
status: docs-checked
description: "Set render settings for a VSE edit: resolution and frame rate matching the media, post processing sequencer on, output format, colour management, and rendering ranges."
sources:
  - https://docs.blender.org/manual/en/latest/render/output/properties/post_processing.html
  - https://docs.blender.org/manual/en/latest/editors/video_sequencer/sequencer/navigating.html
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/strips/scene.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# vse-render-settings

Goal: the exported edit matches the preview at full quality.

## Checklist (Output Properties of the edit scene)

- **Resolution** and **%**: match the delivery, usually the footage resolution at 100 percent.
- **Frame Rate**: same as the footage (the Movie add option Set Scene Frame Rate sets it on import).
- **Frame Range**: the sequencer's Range menu has **Set Frame Range to Strips** (sets scene Start and End to encompass the selected strips), **Set Start Frame** (Ctrl Home) and **Set End Frame** (Ctrl End).
- **Post Processing > Pipeline > Sequencer**: renders the output of the Video Sequence Editor instead of the view from the 3D scene's active camera. Scene strips are rendered as part of this pipeline.
- **Pipeline > Compositing**: if also enabled, the Scene strip becomes the output of the Compositor.
- **Output**: choose FFmpeg video (container, video codec, audio codec in the Encoding panel) or an image sequence.
- **Color Management**: set a View Transform suited to the footage (the Movie add option Set View Transform picks one automatically, usually Standard; see sequencer-color-space).

## Rendering

Use the **Render** menu in the top bar (Render Animation) to output the final video.

The sequencer's own *Sequence Render Image* and *Sequence Render Animation* do not render Scene strips by default: they use the preview's shading mode (initially Solid). To render Scene strips through them, set Sidebar > View > Scene Strip Display > Shading to Rendered, available in Preview or Sequencer & Preview mode.

A **preview range** (Set Preview Range, P; clear with Alt P) limits playback and Sequence Render Animation to a section.

## Gotchas

- Media of different resolution is scaled according to the strip's Fit Method. Check frames from each source.
- Scene strips do not render individual render passes, only Combined.
- If Sequencer is off in Post Processing, the 3D scene renders instead of the edit.

## Verify

Render a short range and play it alongside the timeline preview: same picture, timing and audio.

## Checked

- Date: 2026-10-27. Documentation: Blender 5.2 manual (blender-v5.2-release branch of blender-manual).
- Confirmed: Post Processing Pipeline Sequencer and Compositing behaviour, Range menu entries and shortcuts (P, Alt P, Ctrl Home, Ctrl End), Sequence Render note about Scene strips and the Scene Strip Display Shading option, Scene strip Combined-pass limit, Fit Method scaling. Removed the Ctrl Alt P and Ctrl F12 shortcuts and the black-frame claim, which the manual does not give (the preview-range key is P, cleared with Alt P).
- Method: documentation only; no commands were run.
