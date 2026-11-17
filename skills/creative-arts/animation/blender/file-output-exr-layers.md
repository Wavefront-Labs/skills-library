---
id: creative-arts.animation.blender.file-output-exr-layers
name: file-output-exr-layers
category: creative-arts
field: animation
product: blender
tags: [blender, file-output, file-output-exr-layers, exr-layer-naming, multilayer-exr, exr]
level: practitioner
status: docs-checked
description: "Write multi-layer EXR from the Blender File Output node: Media Type Multi-Layer EXR, items become layers, depth and codec options, and how it differs from the scene render output."
sources:
  - https://docs.blender.org/manual/en/latest/compositing/types/output/file_output.html
  - https://docs.blender.org/manual/en/latest/files/media/image_formats.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# file-output-exr-layers

Goal: one EXR per frame with custom, well-named layers (for example a graded beauty plus chosen passes).

## Setup

File Output node > **Media Type** > *Multi-Layer EXR*. All inputs are saved together in a single multi-layer OpenEXR file and each input is stored as a separate layer in it. The input names become the layer names (the manual says the input name is used to construct the file name, and with Multi-Layer EXR each input is a layer). The EXR settings are in the node's *Node Format* panel.

## EXR options

- **Color Depth**: *Float (Half)* (16-bit) or *Float (Full)* (32-bit).
- **Codec**: ZIP and PIZ are lossless, DWAA and DWAB are lossy (with a Quality percentage), and others are listed in `creative-arts.animation.blender.compositor-file-output`.
- Practice, not from the manual: keep data such as depth, position, normals and Cryptomatte IDs at Full float and use lossless codecs for them, because half precision and lossy compression damage data. If you need Half for colour and Full for data, use two File Output nodes.

## Versus the scene render output

Output Properties can also write EXR. The File Output node writes only the inputs you connect, after compositing, under the names you give them; the scene output writes the render result.

## Gotchas

- Renaming an input renames the layer, so any downstream script that expects the old name breaks. Agree on names per project.
- The manual does not describe the exact channel naming or whether view-layer prefixes are added; check the written file with the receiving application's channel list.
- Cryptomatte metadata survival is not documented for File Output; check a written file (see `creative-arts.animation.blender.cryptomatte-handoff`).

## Verify

Open the written file in the Image Editor or the receiving compositor and confirm the layer names and that data layers read as expected.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release branch: compositing/types/output/file_output, files/media/image_formats) and the 5.2 source (rna_scene.cc media types). Fixed: use Media Type Multi-Layer EXR (there is no OpenEXR MultiLayer format entry in 5.2), and removed the single-depth-per-file claim, the channel-suffix naming (`beauty.R`) claim and the oiiotool check, which the manual does not document. The OpenEXR link in sources was dropped.
Method: documentation only; no commands were run.
