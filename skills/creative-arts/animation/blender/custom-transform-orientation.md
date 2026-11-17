---
id: creative-arts.animation.blender.custom-transform-orientation
name: custom-transform-orientation
category: creative-arts
field: animation
product: blender
tags: [blender, transform-orientations, custom-orientation, custom-transform-orientation, normal-orientation, gimbal, cursor-orientation]
level: practitioner
status: docs-checked
description: "Work along arbitrary axes in Blender: Global/Local/Normal/Gimbal/View/Cursor/Parent orientations, creating named custom orientations from faces or edges, and double-tap axis keys."
sources:
  - https://docs.blender.org/manual/en/latest/editors/3dview/controls/orientation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# custom-transform-orientation

Goal: move, extrude or rotate along a tilted face or edge as easily as along world X.

## Built-in orientations (`,` pie or header dropdown)

- The header selector (shortcut `,`) offers **Global**, **Local**, **Normal**, **Gimbal**, **View**, **Cursor** and **Parent** (see the manual's Orientations section for each). The orientation sets the orientation of the Object Gizmo.
- Axis locking during a hotkey transform: press the axis key once to lock to the current orientation's axis, then a second time to get an alternative lock: Local if the orientation was Global, otherwise Global (for example `G Z Z` with Normal orientation locks to the normal first, then to Global Z).

## Create a custom orientation

1. Select an object, or mesh elements (vertices, edges, faces) in Edit Mode.
2. Header Transform Orientation panel, click `+` (*Create Orientation*).
3. Redo panel: *Name*, *Use View* (align to view space), *Use After Creation* (stays selected), *Overwrite Previous* (otherwise a suffix is added to a duplicate name).
Orientations from an object use that object's Local orientation; those from mesh elements use the average Normal orientation of the elements. The default name comes from the selection (object name, "Edge", and so on).

## Uses

- Extrude a panel along a slanted wall's normal; slide a bolt along a diagonal strut.
- The **Cursor** orientation uses the 3D cursor's rotation, a way to get an arbitrary frame without adding to the list (practice).

## Gotchas

- Delete stale custom orientations with the x button in the Transform Orientation panel to keep the list short.
- An orientation built from a single edge may leave the roll about that edge ambiguous (practice); check the gizmo before rotating.

## Verify

Enable the move gizmo with the custom orientation selected and confirm the axes sit where you expect.

## Checked

2026-10-27, Blender manual, branch blender-v5.2-release (raw RST, projects.blender.org/blender/blender-manual). Confirmed against editors/3dview/controls/orientation.rst: orientation list and shortcut (comma), axis double-tap behaviour, custom orientation creation and redo-panel options, source of axes for object versus mesh-element orientations, delete button. Wrong claims fixed: double-tap order (first press uses the current orientation, second the alternative), and the face-Z / edge-Y rule and Ctrl Alt Space shortcut were not in the manual and were removed.

Method: documentation only; no commands were run.
