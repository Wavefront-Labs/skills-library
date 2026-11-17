---
id: creative-arts.animation.blender.scene-units-setup
name: scene-units-setup
category: creative-arts
field: animation
product: blender
tags: [blender, scene-settings, scene-units, unit-scale, frame-rate, fps, frame-range, time-stretching, gravity, multiple-scenes, scene-linking, startup-scene, resolution]
level: practitioner
status: verified
description: "Configure a Blender scene correctly before work starts: units and unit scale, frame rate and ranges, resolution and aspect, gravity, multiple scenes and when to use them."
sources:
  - https://docs.blender.org/manual/en/latest/scene_layout/scene/properties.html
  - https://docs.blender.org/manual/en/latest/scene_layout/scene/introduction.html
  - https://docs.blender.org/manual/en/latest/render/output/properties/frame_range.html
  - https://docs.blender.org/manual/en/latest/render/output/properties/format.html
  - https://docs.blender.org/manual/en/latest/animation/animation_editors.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# scene-units-setup

Goal: a scene whose units, time base and output format are decided once, saved in the startup file, and never argued about mid-production.

## Units (Scene Properties → Units)

- **Unit System:** Metric (default) or Imperial; *None* for abstract work. **Unit Scale** is the factor between internal units and the values displayed: `1.0` = 1 BU is 1 m. The manual states it only influences displayed values, not how things behave internally; physics simulations do not take it into account. Keeping **Unit Scale 1.0** and modelling in metres is the simplest convention (practice); type `2cm`, `3ft` in fields and Blender converts.
- *Length/Mass/Time/Temperature* only change the displayed unit (Length can be Adaptive or a fixed unit).
- *Separate Units* shows `2.285m` as `2m 28.5cm`. *Rotation* is Degrees or Radians for display and editing.
- Default cube is 2 m. Build to real-world size (a human is about 1.8 m, a door about 2.1 m) so depth of field, lights and physics behave plausibly (practice).

## Time (Output Properties → Format / Frame Range)

- **Frame Rate** presets: 6, 8, 12, 23.98, 24, 25, 29.97, 30, 50, 59.94, 60, 120, 240, *Custom* (FPS divided by Base, e.g. FPS 30 with Base 1.001 for 29.97; the manual notes NTSC needs the more precise rate). Set before animating; changing later does not retime keys (use the Dope Sheet `S` scale around frame 0, or `Time Stretching` below).
- **Frame Start / End / Step** (Output Properties > Frame Range, or the Timeline header; defaults 1 to 250). The Timeline's Set Start/End Frame changes the Preview Range instead if it is active. *Use Preview Range* (clock icon in the Timeline header) is an alternative frame range for focusing on part of the animation.
- **Time Stretching (Old/New):** Output → Frame Range remaps the length of the animation (Old 2 and New 1 runs it twice as fast); it does not change Start or End, so check the animation is not cut off. For a permanent retime select all keys in the Dope Sheet, pivot *2D Cursor* at frame 1 (or frame 0), `S 1.25` (practice).
- Common frame rates by use (practice): 24 fps film, 25 PAL broadcast, 30/60 web/game capture; set once in the startup file.
- Playback popover → *Sync: Play Every Frame / Frame Dropping / Sync to Audio* — Sync to Audio drops frames if playback is too slow to stay in sync with audio, so it is a common choice when checking timing; Play Every Frame plays slower than intended rather than dropping frames. *Audio → Scrubbing* is in the same popover.
- Transport shortcuts: `Shift-Left` / `Shift-Right` jump to start / end; `Up` / `Down` jump to the previous / next keyframe.

## Resolution and aspect

- Format → Resolution X/Y and **%** (render at 50% for tests; the % applies to the output size). Pixel Aspect X/Y 1:1 for everything digital; anamorphic only with an explicit delivery spec. *Render Region* renders just a portion of the view; *Crop to Render Region* crops the output to it instead of leaving a transparent background.
- Common: 1920×1080, 3840×2160 (UHD), 4096×2160 (DCI 4K, aspect 1.896), 1080×1920 vertical, 2048×858 (2.39:1 scope). The camera frame in the viewport reflects this immediately.
- Metadata (Output → Metadata): *Date, Time, Render Time, Frame, Memory, Camera, Lens, Scene, Strip, Note* → **Burn Into Image** (stamp) for dailies.

## Gravity and physics scene settings

- Scene → Gravity (default -9.81 m/s² on Z). Scene → *Rigid Body World* holds settings that apply to all rigid bodies. Scene → *Audio*: Volume, Distance Model, Doppler Speed and Doppler Factor.
- *Simplify* (Render tab) reduces scene complexity for viewport and render; the specific limits you set are a per-project choice (practice).

## Scenes: when to use more than one

A .blend can hold many **scenes** (top bar scene selector). Each has its own objects/collections (or shared via linking), world, render settings, frame range, timeline, compositor tree. Use them for:
- Multiple shots in one file (previs, short films): `scene_010`, `scene_020`, each with its own camera and range; render each via `-S scene_020` on the command line (`creative-arts.animation.blender.blendercraft-headless`).
- Separate render passes/variants with different engines or resolutions (a Workbench scene for playblasts, see `creative-arts.animation.blender.workbench`).
- Video editing: an *Edit* scene holding the Sequencer with **scene strips** referencing the shot scenes (`creative-arts.animation.blender.scene-strips-render`).
- Shared assets: Topbar Scene menu → Add: *New* (empty scene), *Copy Settings* (empty scene with render and world settings copied), *Linked Copy* (shares all data, so edits in one scene affect the other), *Full Copy* (independent copies of all objects and data).

A scene has its own **Scene → Camera** (also set with `Ctrl-Numpad0` in the 3D Viewport).

## Setting it in the startup file

Set units, fps, resolution, colour management, render engine, output path (a `//` prefix is relative to the blend-file), file format (for example OpenEXR Multilayer for comp, PNG 16-bit for review — practice), then `File → Defaults → Save Startup File`. Studio template: `bpy.context.scene.render.fps = 25` etc. in a `scripts/startup/` file keyed to a `load_post` handler so even inherited files get corrected (see `creative-arts.animation.blender.handlers-timers`).

```python
s = bpy.context.scene
s.unit_settings.system = 'METRIC'; s.unit_settings.scale_length = 1.0
s.render.fps = 24; s.render.fps_base = 1.0
s.render.resolution_x, s.render.resolution_y, s.render.resolution_percentage = 1920, 1080, 100
s.frame_start, s.frame_end = 1001, 1100
```

## Gotchas

- Check Scene → Units when a scene "looks small but reads big" after an import; the importer's own scale options also apply.
- Frame Start 1 vs 1001: some VFX pipelines start at 1001 so pre-roll frames keep positive numbers (practice); set it per project in the startup file.
- Pixel Aspect X/Y pre-distorts the image (it looks stretched on a computer screen and is correct on the intended display), so keep it at 1:1 unless a delivery spec says otherwise, and check the Format panel before a long render.
- A forgotten *Simplify* limit can lower the quality of the final render; check the Render tab before a long render (practice).

## Verify

- `N` panel on the default cube reads 2 m × 2 m × 2 m with Unit Scale 1.
- Output Properties > Format shows the agreed frame rate and the Timeline stops at Frame End.
- A test render's metadata stamp shows the right frame, camera and resolution; aspect looks identical in viewport and output.
- Opening a new file from the startup shows these settings without touching anything.

## Checked

2026-10-27. Documentation release: Blender manual 5.2 (branch blender-v5.2-release), with the frame rate preset folder from the same branch. Confirmed: Unit Scale is display-only and physics ignores it, Separate Units example, Rotation and Length options (scene_layout/scene/properties.rst); Add Scene options New, Copy Settings, Linked Copy, Full Copy (scene_layout/scene/introduction.rst); Frame Range defaults 1 to 250, Step and Time Stretching Old/New (editors/timeline.rst and render/output/properties/frame_range.rst); Frame Rate FPS and Base, Pixel Aspect, Render Region and Crop (render/output/properties/format.rst); Playback Sync modes, Audio Scrubbing, Preview Range and transport shortcuts (animation/animation_editors.rst); default gravity -9.81 on Z (physics/forces/gravity.rst); command-line -S scene option (advanced/command_line/arguments.rst). Wrong in the old text: physics does not misbehave at non-1 unit scale because it ignores it; Ctrl Home/Ctrl End, Ctrl Shift arrows and the up/down marker jump are not documented (Up/Down jump keyframes); the frame rate presets also include 6, 8 and 12. Removed unconfirmed Outliner drag-to-link, Render Layers node, grid, FBX-unit-scale and Sync-to-Audio claims. Python property names in the snippet exist in the UnitSettings and Scene RNA definitions.

Run check, 2026-11-01, Blender 4.5.14 LTS headless: defaults of 24 fps, base 1.0, frames 1 to 250, step 1, 1920x1080 at 100 percent, gravity (0, 0, -9.81), METRIC at scale 1.0 with DEGREES; `unit_settings` has system, system_rotation, scale_length, use_separate, length/mass/time/temperature units; the system items are NONE, METRIC, IMPERIAL; changing `scale_length` left cube dimensions at 2 m; fps 30 over base 1.001 is 29.97; the shipped framerate presets are 6, 8, 12, 23.98, 24, 25, 29.97, 30, 50, 59.94, 60, 120, 240 and Custom; `bpy.utils.units.to_string('METRIC', 'LENGTH', 2.285, precision=3, split_unit=True)` gave `2 m 29 cm`, and `to_value` converted `2cm` and `3ft`; `scene.new` types are NEW, EMPTY, LINK_COPY, FULL_COPY; time stretching (old/new 100), preview range, Simplify, metadata stamp, audio and rigid body world properties exist. Unrun: all UI wording (panels, popovers, shortcuts, Sync modes), render behaviour of Simplify and stamps.

Method: documentation checked against the manual and API pages; the code was run headless in Blender 4.5.14.
