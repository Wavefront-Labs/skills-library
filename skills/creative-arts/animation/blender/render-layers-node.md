---
id: creative-arts.animation.blender.render-layers-node
name: render-layers-node
category: creative-arts
field: animation
product: blender
tags: [blender, compositor, render-layers-node, render-layers-input, view-layer, compositing]
level: practitioner
status: docs-checked
description: "Bring render passes into the compositor with the Render Layers node: Scene, View Layer, Image, Alpha and pass sockets, multiple layers, other scenes and viewport limits."
sources:
  - https://docs.blender.org/manual/en/latest/compositing/types/input/scene/render_layers.html
  - https://docs.blender.org/manual/en/latest/render/layers/passes.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# render-layers-node

Goal: bring rendered passes into the compositor correctly.

## Node (Input > Scene > Render Layers)

Renders a view layer and reads its passes into the compositing node graph. It has no input sockets.
- **Scene** and **View Layer**: which view layer to render. The button next to the dropdown re-renders it immediately.
- Outputs: **Image**, **Alpha**, and additional sockets for every render pass enabled on the view layer (enable passes in View Layer properties > Passes; see the passes page for Data, Light and Cryptomatte passes).

## Multiple layers

Add one Render Layers node per view layer and combine them (for example with Alpha Over for background, character and effects layers).

## Other scenes

To use another scene's composited output rather than its raw render, the manual's hint is to render that scene into multilayer images (for example OpenEXR) and load them with an Image node in the current scene's compositor.

## Gotchas

- The viewport compositor only supports render passes when using EEVEE; for other engines the passes are empty.
- If you turn a pass off, its socket disappears from the node and links to it are lost. Check links after changing passes.

## Verify

Connect each Render Layers output to a Viewer in turn. Each pass should show the expected data.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch).
Confirmed: Render Layers Scene and View Layer properties, re-render button, Image, Alpha and pass sockets, the other-scene multilayer EXR hint, and the viewport compositor EEVEE-only pass note. Removed the Add menu path claim, the F12 and Use for Rendering behaviour, the Save Buffers remark and the claim that another scene is rendered by the node.
Method: documentation only; no commands were run.
