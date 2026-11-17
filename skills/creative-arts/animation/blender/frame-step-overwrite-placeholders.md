---
id: creative-arts.animation.blender.frame-step-overwrite-placeholders
name: frame-step-overwrite-placeholders
category: creative-arts
field: animation
product: blender
tags: [blender, output-settings, frame-step-overwrite, placeholders, overwrite, render-farm]
level: practitioner
status: docs-checked
description: "Control which frames render and get written: frame step, overwrite off, placeholders for simple multi-machine rendering, and file extensions, plus restart and cleanup."
sources:
  - https://docs.blender.org/manual/en/latest/render/output/properties/frame_range.html
  - https://docs.blender.org/manual/en/latest/render/output/properties/output.html
  - https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# frame-step-overwrite-placeholders

Goal: render only what is needed, resume after a crash, and share frames between machines without a farm manager.

## Settings

- Output Properties > Frame Range: **Frame Start / End / Step**. Step is the number of frames to advance for each frame rendered, so 2 renders every other frame (fast motion previews). Keep it at 1 for finals.
- Output Properties > Output:
  - **Overwrite** (Media Type Image or Multi-Layer EXR): overwrites existing files when rendering. With it off, frames that already exist on disk are not rendered again, which lets you resume a crashed render.
  - **Placeholders** (same media types): creates empty placeholder frames while rendering, so other Blender instances with Overwrite off skip them.
  - **File Extensions**: adds the correct file extension for the file type to the output files. Keep it on.

## Poor-man's farm

The manual's "Primitive Render Farm" hint: set up a shared directory over a network file system, disable Overwrite, enable Placeholders in the Render Output panel, and start as many machines as you like rendering to that directory. For example each machine runs `blender -b shot.blend -a` (`-a` is `--render-anim`) with the .blend and output folder on the shared drive; each machine takes frames that have no file yet.

## Cleanup after crashes

A machine that crashes leaves a zero-byte placeholder that no one re-renders. After the run, find and delete empty files, then render again with Overwrite off:
```bash
find /renders/sh010 -name "*.exr" -size 0 -delete
```

## Gotchas

- Overwrite off also skips old frames from a previous version of the shot. Use versioned output folders.
- Placeholders and Frame Step together are fine, but frames outside the step are never written.
- Overwrite and Placeholders only appear for the Image and Multi-Layer EXR media types, not Video, which writes one file. Render image sequences for any multi-machine or resumable job.

## Verify

Start two instances on one shot and confirm that each frame number exists once, with no zero-byte files at the end.

## Checked

2026-10-27. Documentation release: Blender manual 5.2 (branch blender-v5.2-release). Confirmed: Frame Start/End/Step and its meaning (render/output/properties/frame_range.rst); File Extensions, Overwrite and Placeholders, their availability for Image and Multi-Layer EXR only, and the Primitive Render Farm hint (render/output/properties/output.rst); the -a / --render-anim command-line flag (advanced/command_line/arguments.rst). Wrong or unconfirmed in the old text: the Overwrite on-by-default claim (not stated in the manual) and the //server path in the command example, both removed; the claim that Placeholders and Frame Step are fine together is a logical consequence rather than documented. The find -delete cleanup command is a standard GNU find use and was not run.

Method: documentation only; no commands were run.
