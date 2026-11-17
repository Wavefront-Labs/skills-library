---
id: creative-arts.animation.blender.hide-reveal
name: hide-reveal
category: creative-arts
field: animation
product: blender
tags: [blender, selection, hide-reveal, hide-unselected, selection-history, local-view, edit-mode]
level: practitioner
status: gated
description: "Isolate work in Blender Edit mode: Hide (H), Hide Unselected (Shift H), Reveal (Alt H with select option), local view (Numpad /), and selection history for order-dependent tools."
sources:
  - https://docs.blender.org/manual/en/latest/editors/3dview/navigate/local_view.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/selecting/introduction.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# hide-reveal

Goal: clear the view to reach inner geometry, and control the element order that some tools use.

## Hide / reveal

- Object Mode (Object > Show/Hide): `H` hides selected objects, `Shift H` hides all unselected objects of the scene, `Alt H` reveals all hidden objects.
- The same keys are commonly used for mesh elements in Edit Mode, but the manual pages checked for this review do not cover Edit Mode hide and reveal, so check that behaviour (including whether revealed elements are selected) in your Blender version. (gated: unconfirmed, source is paywalled or blocked)

## Local view

*View > Local View > Toggle Local View* (`Numpad /` or `/`) toggles between Global and Local View for the selected objects; *Remove from Local View* is `Alt Numpad /`. The manual warns that pressing it by accident can make objects seem to vanish; press it again to exit.

## Selection history

- In Edit Mode the active vertex is drawn white, the active edge white, and the active face has a white border (manual, mesh selection introduction).
- Whether and how selection order is recorded for tools such as Merge At First / At Last or Select Next/Previous Active is not covered by the pages checked; test on a small mesh before relying on it. (gated: unconfirmed, source is paywalled or blocked)

## Gotchas

- Hiding is not deletion; reveal everything before handing a file on (practice).

## Verify

`Alt H` in Object Mode reveals all hidden objects.

## Checked

2026-10-27, Blender manual, branch blender-v5.2-release (raw RST, projects.blender.org/blender/blender-manual). Confirmed against scene_layout/object/editing/show_hide.rst (H, Shift H, Alt H in Object Mode), editors/3dview/navigate/local_view.rst (Toggle Local View and Remove from Local View shortcuts) and modeling/meshes/selecting/introduction.rst (active element colours). Edit Mode hide/reveal and selection-history behaviour could not be confirmed in the manual and carry gated markers; the unconfirmed export, modifier and Select Next/Previous claims were removed.

Method: documentation only; no commands were run.
