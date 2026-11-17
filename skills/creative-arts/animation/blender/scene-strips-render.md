---
id: creative-arts.animation.blender.scene-strips-render
name: scene-strips-render
category: creative-arts
field: animation
product: blender
tags: [blender, scene-strips, scene-strip, edit-render, ffmpeg-output, sequencer, vse, multi-shot, camera-override, render-edit, h264, prores, encoding, delivery]
level: advanced
status: docs-checked
description: "Build and render an edit from Blender scenes: Scene strips with camera override, an Edit scene, Output and Encoding settings, FFmpeg codecs and command-line rendering."
sources:
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/strips/scene.html
  - https://docs.blender.org/manual/en/latest/render/output/properties/output.html
  - https://docs.blender.org/manual/en/latest/render/output/properties/post_processing.html
  - https://docs.blender.org/manual/en/latest/files/media/video_formats.html
  - https://docs.blender.org/manual/en/latest/advanced/command_line/render.html
  - https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# scene-strips-render

Goal: one .blend that holds the shots as scenes and an *Edit* scene that cuts them together and encodes the deliverable, or renders them as a sequence for an external edit.

## Scene strips

Add > Scene > scene name in the Sequencer of the **Edit** scene (a Scene strip cannot reference the sequence's own scene). Sidebar > Strip > Scene (see scene-strip-input for every option):
- **Input**: *Camera* (the scene's 3D camera) or *Sequencer* (the scene's own edit, for nested edits).
- **Camera** override: any object, so one shot scene can supply several strips with different cameras.
- **Show** > Transparent for overlays; **Sound > Strip Volume** for the scene's audio.
- The strip length comes from the referenced scene's animation settings; Strip > Update Scene Frame Range refreshes it after the scene's range changes.
- Scene strips are not prefetched (see vse-cache-prefetch) and render only the Combined pass.
- Sequence Render Image and Sequence Render Animation in the sequencer use the preview shading mode (initially Solid) instead of rendering Scene strips. Use the top bar Render menu, or set Sidebar > View > Scene Strip Display > Shading to Rendered (Preview or Sequencer & Preview mode).

## Workflow

1. Shot scenes with their own cameras and frame ranges. Keep the frame rate identical across scenes.
2. Edit scene: Output resolution and frame rate, **Post Processing > Pipeline > Sequencer** on (it renders the Video Sequence Editor output instead of the 3D scene's camera view; Scene strips are rendered as part of it). If **Compositing** is also on, the Scene strip becomes the output of the Compositor.
3. Scene strips on lower channels, sound above or on its own channels, titles above. Transitions and grades per vse-effects-transitions.
4. Render with the top bar Render menu. Heavy Cycles shots make the edit render as slow as all the shots together.
5. For heavy shots render image sequences first (see compositor-file-output), bring them in as Image strips and keep Scene strips for lighter previews.

## Output and encoding (Output Properties)

- **Media Type**: Image (one file per frame), Multi-Layer EXR, or Video (encodes each frame into a container; options in the Encoding panel).
- **Image sequence** suits farm rendering and downstream compositing. The manual's primitive farm hint: use a shared directory, disable **Overwrite**, enable **Placeholders**, and start several machines rendering into it.
- **Encoding** panel: **Container** (MPEG-4, Matroska, WebM, AVI, DV, Flash, MPEG-1, MPEG-2, Ogg, QuickTime), **Video Codec**, **Autosplit Output** (splits after 2 GiB). Some containers and codecs are not compatible, and some codecs do not work with arbitrary dimensions.
- Video codecs listed in the manual: AV1, H.264, H.265 / HEVC, WebM / VP9, DNxHD, DV, FFmpeg video codec #1, Flash Video, HuffYUV, MPEG-1, MPEG-2, MPEG-4 (DivX), ProRes, PNG, QuickTime Animation, Theora. Its Supported Features table gives compression, colour depth, alpha and HDR support per codec; check it before choosing a codec for alpha or HDR.
- **Color Depth** (8, 10, 12): 10 is available for H.264, H.265 and AV1, 12 for H.265 and AV1.
- **ProRes Profile**: ProRes 422 Proxy, 422 LT, 422, 422 HQ, 4444, 4444 XQ.
- **Output Quality** presets or custom **CRF** (0 to 51 for AV1, H.264 and H.265; 0 to 63 for WebP/VP9; 1 to 31 for MPEG-4/DivX; 0 is lossless), **Encoding Speed** presets, **Keyframe Interval** (0 means intra-only), **Max B-frames**.
- **Rate**: Bitrate, Minimum, Maximum, Buffer, Mux Rate, Mux Packet Size.
- **Audio**: Audio Codec (No Audio encodes video only), Audio Channels, Sample Rate, Bitrate, Volume. Container and codec details are in the manual's video formats page.
- Output Color Management panel: Follow Scene or Override.

## Command line and farm

- Arguments are executed in the order given, so put `-f` or `-a` last: `blender -b edit.blend -S Edit -o //delivery/edit_ -F FFMPEG -x 1 -a`.
- `-b` background, `-S` scene name, `-o` output path, `-F` format (the manual lists FFMPEG among the formats that may not be available on every build), `-s` and `-e` start and end frame, `-x` add the file extension, `-E` render engine, `-a` render the animation, `-f` render a single frame.
- The codec and container come from the settings saved in the file. Check them in the Encoding panel before sending the file to a farm.

## Gotchas

- Scene strips render with their own scene's settings and are scaled to the edit resolution according to the strip Fit Method.
- If Post Processing > Sequencer is off, the Edit scene's 3D view is rendered instead of the edit.
- A file saved with an image format renders images on the command line unless `-F` overrides it.

## Verify

- Scrubbing the Edit preview shows each shot through its override camera.
- The render produces one file with picture and audio; a media inspector reports the expected codec, frame rate, resolution and audio stream.
- Replacing a Scene strip with its rendered sequence gives the same framing (toggle mute to compare).

## Checked

- Date: 2026-10-27. Documentation: Blender 5.2 manual (blender-v5.2-release branch of blender-manual).
- Confirmed: Scene strip options and limits, Sequence Render note, Post Processing Sequencer and Compositing behaviour, Media Type options, farm hint (Overwrite off, Placeholders on), container and codec lists, Color Depth availability, ProRes profile names, CRF ranges, Keyframe Interval, Rate fields, Audio fields, Autosplit 2 GiB, command-line argument order and flags. Removed the unconfirmed claims: Ctrl F12, specific H.264/H.265 quality and bitrate advice, DNxHR, alpha availability for ProRes (the manual is inconsistent, so see its table), linked-scene and ffmpeg commands, timecode and metadata remarks, headless audio mixdown commands and colour pipeline claims.
- Method: documentation only; no commands were run.
