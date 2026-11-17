---
id: creative-arts.animation.blender.marker-camera-binding
name: marker-camera-binding
category: creative-arts
field: animation
product: blender
tags: [blender, markers, marker-camera-binding, bind-camera-to-markers, camera-switching, marker-naming, jump-to-marker, move-marker]
level: practitioner
status: docs-checked
description: "Use Blender timeline markers: add/rename/move markers, jump between them, and bind cameras to markers (Ctrl B) to cut between cameras in one scene."
sources:
  - https://docs.blender.org/manual/en/latest/animation/markers.html
  - https://docs.blender.org/manual/en/latest/editors/3dview/navigate/camera_view.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# marker-camera-binding

Goal: annotate the timeline (beats, dialogue lines, shot boundaries) and cut between cameras without the VSE.

## Marker basics (Timeline / Dope Sheet / Graph / NLA / VSE)

- **M** add marker at the current frame; **F2** rename; **G** move selected markers (hold Ctrl to move in one-second steps); **Shift D** duplicate; **X** delete.
- Click a marker to select, Shift-click to select several; **A** selects all while hovering the marker row.
- Jump: Marker > **Jump to Next/Previous Marker**.
- The marker row can be hidden per editor via View > **Show Markers**.
- Scene markers belong to the scene; Marker > **Duplicate Marker to Scene** copies them to another scene.

## Camera binding

1. Go to the frame where a camera should become active.
2. Select the camera object, select a marker (if none is selected a marker is added), then use **Marker > Bind Camera to Markers** (Ctrl B). The marker is renamed to the camera's name and shows a camera icon.
3. Repeat for each cut. Bound markers can be moved to change the frame at which the active camera switches.

## Uses

- Previs/layout: one scene, several cameras, cuts by marker (see `previsualization`). Later convert to VSE scene strips if editorial needs handles.
- Dialogue: name markers with line text for lip sync reference.

## Gotchas

- Pose markers belong to the active action instead of the scene (Marker > Show Pose Markers in the Action Editor); Make Markers Local converts scene markers to pose markers and removes the originals.

## Verify

Scrub across bound markers: the viewport camera view (Numpad 0) switches; render output shows the cut on the right frame.

## Checked
2026-10-27, Blender 5.2 manual (blender-v5.2-release RST), animation/markers (shortcuts M, F2, G, Shift-D, X, Ctrl-B; Bind Camera to Markers behaviour; Jump to Next/Previous; Show Markers; pose markers; Duplicate Marker to Scene) and editors/3dview/navigate/camera_view (animated camera switching). Removed unconfirmed box-select, Sync Markers, single-frame render and delete behaviour claims.
Method: documentation only; no commands were run.
