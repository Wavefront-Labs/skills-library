---
id: creative-arts.animation.blender.markers-motion-paths
name: markers-motion-paths
category: creative-arts
field: animation
product: blender
tags: [blender, markers, motion-paths, motion-path, camera-binding, timeline, arcs, pose-markers, shot-markers, animation-review, onion-skinning-3d]
level: practitioner
status: docs-checked
description: "Timeline markers and motion paths in Blender: naming and navigating markers, binding cameras to markers, pose markers, and motion paths to check arcs and spacing."
sources:
  - https://docs.blender.org/manual/en/latest/animation/markers.html
  - https://docs.blender.org/manual/en/latest/animation/motion_paths.html
  - https://docs.blender.org/manual/en/latest/editors/timeline.html
  - https://docs.blender.org/api/current/bpy.types.TimelineMarkers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# markers-motion-paths

Goal: label time so the whole team talks about the same frames, switch cameras without a sequencer, and see arcs and spacing as curves in the viewport.

## Markers

- Add: `M` (*Marker → Add Marker*) in the Timeline/Dope Sheet/Graph Editor/NLA/Sequencer at the current frame; markers can also be added during playback. Rename: `F2` (*Marker → Rename Marker*) → markers named like `sc010_sh020_start`, `anticipation`, `contact`, `beat_music` (naming is practice). Select: click the triangle, `Shift` click extends, `A` over the marker row selects all, `[` / `]` select before/after the current frame. Move: `G` with the mouse over the marker bar (`Ctrl` moves in steps of 1 second). Delete: `X`. Duplicate: `Shift D` (names are not altered). *Marker → Jump to Next/Previous Marker* moves the playhead between markers.
- Markers are shown in every editor that supports them; markers sit on whole frames only. `View → Show Markers` toggles the marker row per editor (the Marker menu is hidden while it is off). The 3D Viewport only displays a marker's name in the Object Info text on its frame.
- *Marker → Duplicate Marker to Scene...* copies the selected markers into another scene.
- **Sound sync:** practice is to load the audio in the Sequencer (or a Speaker) and place markers on beats/phonemes while it plays. Playback Sync mode options include Play Every Frame, Frame Dropping and Sync to Audio. Lip-sync: markers named with phonemes then animate to them (`creative-arts.animation.blender.lip-sync`).
- **Pose markers** (Dope Sheet in Action Editor or Shape Keys Editor mode → *Marker → Show Pose Markers*): markers belonging to the **action**, not the scene (shown as diamonds in the Dope Sheet), useful to label key poses in a cycle (`contact`, `down`, `passing`, `up`); `Marker → Make Markers Local` converts standard markers into pose markers and removes the originals.
- Markers from a shot list: Python
  ```python
  for name, frame in [("sh010", 1001), ("sh020", 1073)]:
      bpy.context.scene.timeline_markers.new(name, frame=frame)
  ```

## Camera binding (multi-camera in one scene)

Select the camera object and a marker, then `Ctrl B` (*Marker → Bind Camera to Markers*). If no marker is selected a marker is added; the marker is renamed to the object's name and shows a camera icon. Moving the marker changes the frame at which that object becomes the active camera. Steps for a shot sequence:
1. One camera per shot (`CAM_sh010`, …), framing done.
2. Markers at each shot's first frame.
3. Select camera A and its marker, `Ctrl B`; repeat.
4. Render the whole range: the active camera follows the bound markers.
Unbind (practice): delete the marker or rebind another camera. Scene → *Camera* field shows the current camera. In the Sequencer, scene strips have their own *Camera* setting for per-strip cameras instead (`creative-arts.animation.blender.scene-strips-render`).

## Motion paths

Object Properties → *Motion Paths* (objects) or Armature → *Motion Paths* (bones, in Pose mode — per selected bone):
- *Paths Type*: **Around Frame** (a number of frames *Before* and *After* the current frame; practice: the animator's default while polishing) or **In Range** (a specified range).
- *Calculation Range* (only for In Range; takes effect on Update Path / Update All Paths): *All Keys*, *Selected Keys*, *Scene Frame Range* (or the preview range) or *Manual Range*. *Step* shows one point per n frames.
- *Bake Location* (bones in Pose Mode): **Heads** or **Tails** (practice: tails for a hand/finger tip, since the tail of the hand bone is the wrist arc you actually judge).
- **Calculate** (Pose Mode: *Pose → Motion Paths*) creates the path for the selected bones; the manual says paths are updated automatically when you edit poses/keyframes and are also active during playback (playing affects the paths only with *Around Frame*). *Update Paths* refreshes an existing path (the frame range is changed only by clearing and recalculating), *Update All Paths* recalculates all visible objects and poses, and *Clear Paths* removes them (hold `Shift` to clear only the selected ones). *Bake to Active Camera* bakes in screen space for the active camera only.
- Display: *Frame Numbers*, *Keyframes*, *Keyframe Numbers*, *Lines*, *Thickness*, *Custom Color*; the paths are red for the past and green for the future.
- Read it: evenly spaced dots = constant speed; bunching = slow-in/out; a kink = a broken arc or a bad spacing at a key. Edit keys in the Graph Editor and *Update Paths* until the arc is clean (`creative-arts.animation.blender.graph-editor-polish`).
- Practice: paths follow the evaluated motion (constraints, parents), which makes them good for checking a hand following an IK target through a parent switch.
- Only selected bones are affected by Calculate and Clear; paths are stored in the file, so clear them before publishing (practice).

## Related review aids

- Grease Pencil has real onion skins (`creative-arts.animation.blender.grease-pencil-animation`).
- Timeline *Use Timecode* (`Ctrl T`) swaps frame numbers for timecode when discussing with editors.
- Timeline *Auto Keying* lives in the header; markers don't key anything.

## Gotchas

- Moving markers with `G` requires the mouse over the marker bar; otherwise you move keyframes.
- One scene = one active camera per frame, so the render shows what the bound camera sees.
- Practice: motion paths with a large *In Range* span on a dense rig are slow; use *Around Frame* while polishing.
- The frame range of an existing path changes only after clearing and recalculating; changing Heads/Tails likewise means recalculating (practice).

## Verify

- *Marker → Jump to Next/Previous Marker* lands on your named markers.
- Scrubbing across a camera-bound marker switches the active camera and the Scene → Camera field changes.
- A bone's motion path shows dots spaced as intended (bunched at the ends of an ease) and lines up with the actual bone tail/head during playback.
- Editing a key visibly changes the path.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release RST) and current Python API docs.
Confirmed: marker shortcuts (`M`, `F2`, `G`, `X`, `Shift D`, `Ctrl B`, selection keys), Show Markers, Duplicate Marker to Scene, Show Pose Markers and Make Markers Local, Bind Camera to Markers behaviour; Motion Paths options (Paths Type, Calculation Range, Before/After, Step, Bake Location, Update Paths, Update All Paths, Clear Paths, Bake to Active Camera, display options); Timeline Use Timecode `Ctrl T`; `scene.timeline_markers.new(name, frame=)` signature. Fixed: motion paths DO update automatically (the skill said they did not); Calculation Range options are All Keys/Selected Keys/Scene Frame Range/Manual Range; "Make Links to Scene" is Duplicate Marker to Scene; "Show Seconds" is Use Timecode; Ctrl M, Lock Markers and "no default key" claims removed. Removed: version gates, Motion Trail extension and FBX/Alembic marker claims (no doc coverage).
Method: documentation only; no commands were run.
