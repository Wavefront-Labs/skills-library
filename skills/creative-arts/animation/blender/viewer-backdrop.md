---
id: creative-arts.animation.blender.viewer-backdrop
name: viewer-backdrop
category: creative-arts
field: animation
product: blender
tags: [blender, compositor, viewer-backdrop, backdrop, viewer-node, compositing]
level: practitioner
status: docs-checked
description: "Inspect the compositor with the Viewer node and backdrop: Ctrl Shift click previews, zoom and pan, sampling pixel values, the Viewer Node image and region of interest."
sources:
  - https://docs.blender.org/manual/en/latest/compositing/types/output/viewer.html
  - https://docs.blender.org/manual/en/latest/compositing/sidebar.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# viewer-backdrop

Goal: see any point of the comp tree quickly while working.

## Viewer node

Add the **Viewer** node (Output section). Its *Image* input is previewed in:
- The **Backdrop** behind the node tree: turn it on with the *Backdrop* button in the Compositor header or the checkbox in the sidebar View tab, Backdrop panel.
- The Image Editor, by choosing *Viewer Node* in the Image data-block menu in the header.
- `Shift-Ctrl-LMB` on a node connects it to the Viewer (built in). Only the active Viewer node (eye icon in its header) is displayed; select another with `LMB` to switch. `Ctrl-1` to `Ctrl-9` assign a viewer shortcut to the selected node (creating a Viewer if none is attached) and `1` to `9` activate it.
- With no Viewer node the Group Output node is used for interactive previews.

## Backdrop controls

- Sidebar View tab, Backdrop panel: *Channels*, *Zoom* (`V`, `Alt-V`), *Offset X/Y*, *Move* (`Alt-MMB`) and *Fit* (scales the backdrop to the compositor view).
- With the Viewer node selected, a gizmo in the backdrop moves and scales the displayed image (if *Show Gizmo* for the active node is enabled). These only change the display, not the compositor output.

## Sampling values

In the Image Editor showing the Viewer Node, click and hold in the image to sample its values. The Image Editor header also has options to view the image with or without alpha, or to view alpha or Z itself. Use `Image > Save As` (`Alt-S`) to save the viewed image.

## Gotchas

- The viewer shows what you connect, not the final output. Before rendering, make sure the Composite (or Group Output) has the final result.
- Several Viewer nodes: only the active one (eye icon) shows in the backdrop or Image Editor.
- The Viewer region (area of interest) option with `Ctrl-B` is commented out in the manual as currently removed from the UI.

## Verify

`Shift-Ctrl-LMB` a matte node. The backdrop shows it, and values sampled in the Image Editor read 0 outside and 1 inside.

## Checked

2026-10-27, against the Blender 5.3 manual (branch blender-v5.3-release). Confirmed on the Compositor Viewer node and Sidebar pages: Shift-Ctrl-LMB without add-ons, active Viewer node, number shortcuts, Backdrop toggles and controls (Channels, Zoom, Offset, Move, Fit), Image Editor Viewer Node data-block, sampling by click-and-hold, Group Output fallback. Removed unconfirmed claims: Node Wrangler requirement, output cycling, Home key behaviour, separate backdrop right-click sampling, region of interest and Scopes tab details.

Method: documentation only; no commands were run.
