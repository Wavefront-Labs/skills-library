---
id: creative-arts.animation.blender.vse-editing
name: vse-editing
category: creative-arts
field: animation
product: blender
tags: [blender, vse, sequencer, video-sequencer, video-editing, proxies, strips, cutting, channels, timecode, animatic, edit, trim, ripple, slip, speed]
level: practitioner
status: docs-checked
description: "Cut footage in the Blender Video Sequence Editor: importing strips, cutting/trimming/slip, channels and muting, proxies and prefetch for smooth playback, retiming, audio sync, markers."
sources:
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/editing.html
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/selecting.html
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/strips/introduction.html
  - https://docs.blender.org/manual/en/latest/video_editing/edit/montage/strips/strip_properties.html
  - https://docs.blender.org/manual/en/latest/editors/video_sequencer/introduction.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# vse-editing

Goal: assemble shots, animatics or edits inside Blender with responsive playback and clean cuts.

## Setup

- Use the default **Video Editing** workspace, or a Video Sequencer editor in one of its modes: *Sequencer*, *Preview* or *Sequencer & Preview*. The manual notes that *Sequencer & Preview* lacks most of the Preview tools, so separate Sequencer and Preview editors are often better.
- Set the scene resolution and frame rate to match the footage first. The Movie add options **Set Scene Frame Rate** and **Fit Method** help (see vse-import-media).
- Output > Post Processing > **Sequencer** must be on, otherwise the 3D scene renders instead of the edit (see vse-render-settings).
- Scene strips cannot reference the sequence's own scene, so use a secondary scene for 3D shots (see scene-strips-render).

## Importing

`Shift A` opens the Add menu (also in the header): Movie, Sound, Image/Sequence, Scene, Mask, effect and transition strips and more, plus a Search entry. New strips start at the playhead. Several files added at once are placed one after another. Movie strips can also create Sound strips from the movie's audio streams.

## The grammar of editing

- **Select**: click a strip's middle to select it, `A` all, `Alt A` none, `Ctrl I` invert, `B` box select, `Ctrl B` box select including handles, `Shift G` Select Grouped, `[` and `]` select strips left or right of the current frame.
- **Cut**: `K` Split at the current frame (both strips keep the same source, the hidden part stays reachable by dragging handles). `Shift K` Hold Split (you cannot drag the endpoints past the split; use the Hold Offset fields instead).
- **Move and trim**: `G` moves selected strips (hold Ctrl to toggle snapping, X or Y to lock to time or channel); drag a handle to change the start or end frame. `E` Move/Extend from Current Frame changes handles on the mouse side of the playhead together.
- **Slip**: `S` Slip Strip Contents shifts the source inside a strip without moving its bounds (Offset, Slip Keyframes, Shift for subframe sound slip, C to clamp).
- **Snap**: `Shift S` Snap Strips to the Current Frame; `Alt O` Clear Strip Offset; `Alt Left` and `Alt Right` Swap Strip.
- **Gaps**: `Backspace` Remove Gaps, `Shift Equals` Insert Gaps (see vse-snapping-overlap).
- **Duplicate**: `Shift D` unlinked copy (a Scene strip's scene is duplicated too), `Alt D` linked copy. `Delete` or `X` deletes. `Y` Separate Images turns an image sequence into one strip per frame.
- **Channels**: higher channels are drawn in front of lower ones; strips cannot overlap inside a channel (see vse-channels). Mute a strip `H`, unmute `Alt H`, lock `Ctrl H`, unlock `Ctrl Alt H`.
- **Meta strips**: `Ctrl G` group, `Ctrl Alt G` ungroup, `Tab` enter or exit (see vse-meta-strips).
- **Time panel** (Sidebar > Strip > Time): Start, Duration, End, **Strip Offset Start/End** (negative values extend the strip with frozen first or last frames), **Hold Offset Start/End** (trim source frames; combined with Strip Offset they can hold a frame other than the first or last), Current Frame.

## Playback performance

- **Proxies**: View tab **Proxy Render Size**, or the Proxy tab (Set Selected Strip Proxies, Rebuild Proxy and Timecode Indices). Default location is `BL_proxy` next to the footage (see vse-proxy-setup).
- **Cache**: Sidebar > Cache > Cache Settings has Prefetch Frames and Raw and Final cache; Show Cache in the timeline overlay shows what is cached (see vse-cache-prefetch).
- Preferences > System > Video Sequencer > **Memory Cache Limit**.

## Speed and retiming

- **Retiming keys** (Strip > Retiming; `Ctrl R` toggles the keys; `R` sets the speed of the selected strips): see vse-retiming.
- **Speed Control** effect strip is the older approach (see vse-speed-control).
- Strip properties > Video: **Reverse Frames** plays a strip backwards, **Strobe** shows every nth frame.

## Sidebar essentials (Strip tab)

- **Compositing**: Blend and Opacity (Opacity can be animated, drawn as an overlay on the strip).
- **Transform**: Position, Scale, Rotation, Mirror, Filter; **Crop**: Top, Left, Bottom, Right in pixels.
- **Color**: Saturation, Multiply, Multiply Alpha, **Convert to Float**.
- **Source**: directory, filename, Color Space, Alpha Mode, Stream Index, Deinterlace, source information (resolution, FPS).
- **Modifiers** live in the Properties Editor > Strip Modifiers panel (see vse-strip-modifiers); Copy to Selected copies a modifier to selected strips.
- Fades: Add > Fades has Fade In and Out, Fade In, Fade Out, From Current Frame, To Current Frame and Clear Fades. They animate opacity (or volume on sound strips).

## Keys you will use

`Home` Frame All, `Numpad 0` centre on the current frame, `PageUp` and `PageDown` jump to the previous or next strip border, `Alt PageUp` and `Alt PageDown` jump to strip centres, `Ctrl Tab` toggles Sequencer and Preview display, `Spacebar` plays.

## Gotchas

- A Movie strip whose FPS differs from the scene frame rate plays at the wrong speed unless you adjust playback rate or speed.
- Image strips are created 25 frames long by default.
- Muted strips and muted channels are not shown or heard in the final video.
- Choose an **Audio Codec** under Output > Encoding > Audio for video files that should contain sound; "No Audio" encodes video only.
- Scene strips are not prefetched and render only the Combined pass.

## Verify

- `K` at the playhead splits the selected strips; dragging the new handle back reveals the hidden frames.
- Sound stays in sync with picture at the end of a long edit (check a clap or the waveform).
- A rendered file matches the Preview at the chosen resolution, with audio.

## Checked

- Date: 2026-10-27. Documentation: Blender 5.2 manual (blender-v5.2-release branch of blender-manual).
- Confirmed: Workspace and editor modes, Add menu behaviour, selection shortcuts, Split and Hold Split, Move, Extend, Slip, Snap, Swap, Gaps, Duplicate, Separate Images, lock and mute shortcuts, meta shortcuts, Time panel offsets, proxy and cache locations, Retiming shortcuts (Ctrl R, R), Video panel Reverse Frames and Strobe, Color panel fields, Fades menu, navigation shortcuts, Scene strip limits. Corrected Lock (Ctrl H, not Shift L), ungroup (Ctrl Alt G, not Alt G), the Fades menu (Add > Fades), cache levels (Raw and Final only), prefetch location, and where Strip Modifiers live. Removed the audio-device, sync, scopes, timecode-mode, Numpad-period, Copy/Paste Modifiers and mixed-fps advice that the manual does not document.
- Method: documentation only; no commands were run.
