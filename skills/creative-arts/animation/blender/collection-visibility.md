---
id: creative-arts.animation.blender.collection-visibility
name: collection-visibility
category: creative-arts
field: animation
product: blender
tags: [blender, collections, view-layers, collection-visibility, exclude-from-view-layer, hide-in-viewport, disable-in-renders, holdout, indirect-only]
level: practitioner
status: docs-checked
description: "Know which Blender visibility switch to use: Exclude, Hide in Viewports, Disable in Viewports, Disable in Renders, Disable Selection, Holdout and Indirect Only, and their scope."
sources:
  - https://docs.blender.org/manual/en/latest/editors/outliner/interface.html
  - https://docs.blender.org/manual/en/latest/scene_layout/collections/collections.html
  - https://docs.blender.org/manual/en/latest/editors/outliner/editing.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# collection-visibility

Goal: hide things for speed, for render passes, or for compositing without accidentally dropping them from a render.

## The switches and their scope

Only a few columns show by default; enable the rest from the Outliner filter popover (Restriction Toggles).

| Switch | Scope | Effect |
|---|---|---|
| Exclude from View Layer (checkbox) | per view layer | Contents hidden in the 3D Viewport, the render and the Outliner for that layer. |
| Disable Selection (arrow) | collection/object | Cannot be selected in the 3D Viewport; handy for reference images. |
| Hide in Viewports (eye) | per view layer | Viewport only; render not affected. Still part of the view layer, so still evaluated. |
| Disable in Viewports (screen) | all view layers | Viewport only; render not affected. No longer part of the view layer: not evaluated, no playback cost. |
| Disable in Renders (camera) | all view layers | Render only; viewport not affected. |
| Holdout (collections) | per view layer | Objects cut a fully transparent hole into the layer's render output. |
| Indirect Only (collections, Cycles) | per view layer | Objects contribute only through shadows and reflections. |

## Shortcuts and gestures

- `Shift-LMB` on an icon toggles it for the item and all its children.
- `Ctrl-LMB` on a collection's icon enables it for that collection (and its parents and children) and disables it for all others; click again to restore.
- In the 3D Viewport: `H` hides selected, `Shift-H` hides unselected, `Alt-H` unhides all; `Ctrl-H` is *Object > Collection > Hide Other Collections*.
- Outliner context menu > Visibility: Isolate, Show/Hide, Show/Hide Inside, Enable/Disable in Viewports, Enable/Disable in Renders.

## Using them

- An object needs both *Hide in Viewports* and *Disable in Viewports* off to be visible, so *Disable in Viewports* is the one for long-term invisibility that survives `Alt-H`.
- Heavy sets while animating: use *Disable in Viewports* to remove them from evaluation; leave *Disable in Renders* off so they still render.
- Helper objects that should never render: *Disable in Renders*.
- Per-layer matte and shadow setups: Holdout and Indirect Only on separate view layers.

## Gotchas

- Eye-hidden objects still render. Check the camera icon when something unexpected shows in a render.
- Hide in Viewports is not carried when you Link or Append: everything is visible in the other file. Disable in Viewports and Disable in Renders carry over.
- *Disable in Renders* and *Disable in Viewports* are not per view layer; use Exclude for per-layer control.

## Verify

Render the view layer and confirm the expected collections appear; compare with the Outliner columns.

## Checked

Date: 2026-10-27. Documentation: Blender manual 5.3 (editors/outliner/interface.rst, editors/outliner/editing.rst, scene_layout/collections/collections.rst).
Confirmed: every toggle's name, scope and effect, evaluation note, Shift-LMB and Ctrl-LMB behaviour, H, Shift-H, Alt-H, Ctrl-H, context menu entries, linking behaviour. Removed unconfirmed claims: keyframable toggles, number-key collection toggles, Exclude resetting per-object hide state, and the shadow catcher recipe.
Method: documentation only; no commands were run.
