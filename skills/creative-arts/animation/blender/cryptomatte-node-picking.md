---
id: creative-arts.animation.blender.cryptomatte-node-picking
name: cryptomatte-node-picking
category: creative-arts
field: animation
product: blender
tags: [blender, cryptomatte, cryptomatte-node, cryptomatte-picker, mattes, compositor]
level: practitioner
status: docs-checked
description: "Extract mattes with the Blender compositor Cryptomatte node: Source Render or Image, Cryptomatte Layer, + and - picking, Matte ID, and the Image, Matte and Pick outputs."
sources:
  - https://docs.blender.org/manual/en/latest/compositing/types/mask/cryptomatte.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# cryptomatte-node-picking

Goal: isolate any object or material for grading after rendering.

## Node (Add > Mask > Cryptomatte)

The menu also lists the deprecated *Cryptomatte (Legacy)* node after the current one.

- **Image** input: a colour render of the scene, only needed for the *Image* output; if only the grayscale mask is needed it can stay unconnected.
- **Source**: *Render* uses the Cryptomatte render passes of a View Layer in the chosen **Scene**; *Image* uses a Cryptomatte image from a multilayer OpenEXR file (the **Image** field).
- **Cryptomatte Layer**: the image layer to use, typically a combination of a View Layer and a type (Object, Material or Asset).
- **Matte ID**: comma-separated names of the objects or materials to mask. The `+` and `-` buttons next to it add or remove items by picking.
- Outputs: **Image** (the input with the mask applied; everything else transparent), **Matte** (grayscale mask) and **Pick** (a coloured representation used for picking).

## Typical usage (from the manual)

1. Enable the Cryptomatte Object pass in View Layer > Passes and render.
2. In the Compositor add a Cryptomatte node and a Viewer node.
3. Connect the Render Layers Image output (or the node's Pick output) to the Viewer; make sure *Backdrop* is on if nothing appears.
4. Click `+` in the node, then click objects in the backdrop. Repeat for more.
5. Use the Matte output as the mask, or connect the render to the node's Image input and use its Image output for a masked render.

Use Matte as the factor of a grade node to adjust only that object (practice).

## Reuse

Matte IDs are names, so the same list works on other shots with the same object or material names (practice).

## Gotchas

- Picking does nothing when Source, Scene or Cryptomatte Layer point at a different image than the one in the backdrop.
- The Cryptomatte node cannot be used in node groups, so keep it in the scene compositing tree.
- Cryptomatte sidecar files and volume objects are not supported.
- The old Legacy node needs CryptoObject passes connected to its inputs and is deprecated; the current node does not need them connected.

## Verify

View the Matte output: the selected objects are white with antialiased edges and everything else is black.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release branch: compositing/types/mask/cryptomatte and cryptomatte_legacy) and the 5.2 source (node_add_menu_compositor.py). Fixed: the property names are Cryptomatte Layer and Matte ID with +/- buttons (not Add/Remove eyedroppers), the manual lists the node-group limitation, and the Legacy node is deprecated rather than "still works". Removed the unconfirmed claim about stair-stepped edges from low levels.
Method: documentation only; no commands were run.
