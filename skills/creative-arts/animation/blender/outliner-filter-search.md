---
id: creative-arts.animation.blender.outliner-filter-search
name: outliner-filter-search
category: creative-arts
field: animation
product: blender
tags: [blender, outliner, outliner-filter, outliner-search, restriction-toggles, scene-organisation]
level: practitioner
status: docs-checked
description: "Tame big Blender scenes in the Outliner: filter popover (types, children, contents, state), restriction toggle columns, substring search with Exact Match and Case Sensitive."
sources:
  - https://docs.blender.org/manual/en/latest/editors/outliner/interface.html
  - https://docs.blender.org/manual/en/latest/editors/outliner/selecting.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# outliner-filter-search

Goal: find any object in a big scene quickly and show only the columns you need.

## Filter popover (funnel icon in the header)

Options depend on the Display Mode. In View Layer mode:

- **Restriction Toggles:** choose which columns show: Exclude from View Layer, Disable Selection (arrow), Hide in Viewports (eye), Disable in Viewports (screen), Disable in Renders (camera), Holdout, Indirect Only. Only a few are shown by default.
- **Sort Alphabetically**, **Sync Selection**, **Scroll to Active**, **Expand on Focus**, **Show Mode Column**.
- **Search:** *Exact Match* (name must match fully rather than contain the text) and *Case Sensitive*.
- **Filter:** *All View Layers* (with Objects off gives an overview of collections against view layers), *Collections*, *Objects*, *Object State*, *Object Contents* (materials, modifiers, mesh data as children), *Object Children*, and per-type toggles (Meshes, Lights, Cameras, Grease Pencil, Empties, Others).
- **Object State:** All, Visible, Selected, Active, Selectable, with an *Invert* toggle. *Visible* takes both Hide in Viewports and Disable in Viewports into account.

## Search field

- Type a substring to filter the tree; `Ctrl-F` focuses the box and `Alt-F` clears it.
- The manual describes substring matching only. Wildcard patterns are not documented, so do not rely on them.

## Tips

- Turning off *Object Children* shows child objects as siblings (unless they sit in a different collection from the parent, in which case they are not shown in the parent's collection at all).
- Turning off *Objects* shows only collections; turning off *Collections* hides only the collection rows, the objects remain.
- Each Outliner editor has its own filters, so a second Outliner with different filters is a valid layout choice.

## Verify

Set Object State to Selected and confirm the tree lists exactly the viewport selection.

## Checked

Date: 2026-10-27. Documentation: Blender manual 5.3 (editors/outliner/interface.rst).
Confirmed: filter popover options and names, Object State values, Exact Match and Case Sensitive, Ctrl-F and Alt-F, Object Children and Collections behaviour. Removed unconfirmed claims: `*` and `?` wildcard matching and a pattern example, a Selectable-plus-monitor "can't click" fix, claims about search and rendering with filters on, and the 5,000-object example.
Method: documentation only; no commands were run.
