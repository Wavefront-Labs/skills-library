---
id: creative-arts.animation.blender.composite-output-node
name: composite-output-node
category: creative-arts
field: animation
product: blender
tags: [blender, compositor, composite-node, composite-output, group-output, post-processing]
level: practitioner
status: docs-checked
description: "Where the compositor result goes in Blender 5.2: the Group Output node (active output, first image input), the Compositing Pipeline option in Post Processing, and checks."
sources:
  - https://docs.blender.org/manual/en/latest/compositing/types/output/group_output.html
  - https://docs.blender.org/manual/en/latest/compositing/introduction.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---
# composite-output-node

Goal: the compositor result is what gets rendered and saved.

## Blender 5.2

The scene compositor is a node tree data-block: open the Compositor and click **New** in the header to create one. The final image goes to the **Group Output** node, which defines the image result sent to the renderer or to image output after rendering.
- If several Group Output nodes exist, only the **active** one is used; the others show an "Unused Output" warning. The active output can be changed in the node header.
- The node starts with no input sockets; sockets appear when outputs are defined in the Group tab of the sidebar, or by dragging a link onto the blank socket.
- In the Compositor only the **first image input** is used as the final render result; additional sockets are ignored.
- The node updates after each evaluation or render, and interactively when connected inputs change, provided all inputs are fully evaluated.

## Required setting

The **Compositing Pipeline** option in the Output properties > **Post Processing** panel must be enabled for the renderer to use the compositing node tree (or disabled to skip it).

## Typical end of tree

`... grade -> (optional) Alpha Convert -> Group Output`, with File Output nodes in parallel for passes (see the compositor file output skills).

## Gotchas

- "My render looks the same with nodes": check that Compositing Pipeline is on and that the Group Output has an image connected.
- The Viewer node is not the output (see viewer-backdrop).
- Files made in earlier releases that used a Composite node: check which socket ends up connected to the Group Output after opening them in 5.2.

## Verify

Add an obvious effect (invert) before the output, render one frame and check the saved file shows it. Remove it after.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch).
Confirmed: node tree creation with New, Group Output behaviour (active output, no initial sockets, only the first image input used) and the Compositing Pipeline option under Post Processing. Removed the Blender 4.x Composite node section, Use Alpha, the Use Nodes remark and the command-line override, because the 5.2 manual no longer documents them.
Method: documentation only; no commands were run.
