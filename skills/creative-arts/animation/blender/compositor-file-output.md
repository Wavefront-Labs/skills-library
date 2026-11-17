---
id: creative-arts.animation.blender.compositor-file-output
name: compositor-file-output
category: creative-arts
field: animation
product: blender
tags: [blender, file-output, exr-handoff, comp-handoff, nuke-handoff, compositor, multilayer-exr, render-passes, aov, cryptomatte, data-window, half-float, dwaa, pipeline]
level: advanced
status: docs-checked
description: "Write several files from one Blender render with the File Output node: Directory, File Name, Media Type (Image or Multi-Layer EXR), per-item formats and EXR depth and codec."
sources:
  - https://docs.blender.org/manual/en/latest/compositing/types/output/file_output.html
  - https://docs.blender.org/manual/en/latest/files/media/image_formats.html
  - https://docs.blender.org/manual/en/latest/render/layers/passes.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# compositor-file-output

Goal: hand renders to an external compositor with the layers, names and EXR options you intend, and write several deliverables from one render.

## File Output node (Add > Output > File Output)

The node writes one or more images to disk during rendering or compositing. The path is `{Directory}/{File Name}{Socket Name}{frame number}.{extension}`. This describes the Blender 5.2 layout; the 4.5 manual describes a single Base Path instead (see `creative-arts.animation.blender.file-output-slots`).

- **Inputs**: drag an output onto the blank socket area, or add items in the *Images/Layers* panel (Sidebar > Node > Properties). Each input is one image, or one layer of a multi-layer file. Input names are part of the file name.
- **Directory** and **File Name**: the base output location and the base file name. A `####` in the File Name or in an image name forces where the frame number appears and sets the padding.
- **Media Type**: *Image* writes each input as a separate file (each can have its own format), *Multi-Layer EXR* writes all inputs as layers of one multi-layer OpenEXR file.
- **Node Format** panel: the default format for all outputs (Image), or the EXR options (Multi-Layer EXR). For a single input, tick **Override Node Format** in the Images/Layers panel to use an *Item Format* instead.
- **Output Paths** panel shows the final path and extension for each input; **File Extensions** adds the format extension to the name.
- When Media Type is Image, a slash in an input name makes subfolders, and missing directories are created.
- The node has no output sockets, so it cannot be previewed; use a Viewer node to inspect results.
- In the 5.2 Add menu File Output is offered only in the scene's own compositing tree, not while editing a compositor node group.

## OpenEXR options (Node Format, Multi-Layer EXR)

- **Color Depth**: *Float (Half)* is 16-bit floating point per channel; *Float (Full)* is 32-bit.
- **Codec**: None, ZIP (lossless), PIZ (lossless, effective for noisy images), DWAA and DWAB (lossy, JPEG-like), HTJ2K (lossless, newer and not widely supported), ZIPS, RLE, Pxr24 (lossy for 32-bit float), B44 and B44A (lossy, for 16-bit float).
- **Quality** applies to DWAA and DWAB (0 percent smallest, 100 percent no compression).
- **Interleave**: legacy interleaved storage of views, layers and passes, for applications that do not support multi-part OpenEXR files.
- **Preview**: saves a JPEG copy when rendering animations or from the command line.
- **Save as Render**: for formats such as PNG applies the view and display transform; for intermediate formats such as OpenEXR it uses the default render output colour space. OpenEXR defaults to a linear colour space.
- Metadata written to files is controlled in Output Properties > Metadata (see `creative-arts.animation.blender.stamp-metadata`).

## Practical rules (practice, not from the manual)

- Use one node for colour passes (Half is usually enough) and another for data passes such as depth, position, normal, vector and Cryptomatte IDs (Full), because lossy codecs and half precision damage data. Cryptomatte IDs are float32 bit patterns (metadata conversion `uint32_to_float32`), so they cannot be held in 16 bits.
- Agree pass and layer names with whoever receives the files, and do not rename Cryptomatte layers.

## Cryptomatte

The Render Layers node outputs the CryptoObject, CryptoMaterial and CryptoAsset images (half as many images as the Levels value). The manual's File Output page suggests combining the node with Cryptomatte or other utility passes for pipelines. It does not say whether File Output preserves the Cryptomatte metadata, so inspect the header of a written file before delivering (see `creative-arts.animation.blender.cryptomatte-handoff`).

## Reading files back

Load a multi-layer EXR with the compositor Image node: each layer in the file becomes available as a socket (see `creative-arts.animation.blender.comp-image-movieclip-input`). The Image Editor also opens multi-layer EXRs.

## Verify

- The Output Paths panel shows the names and extensions you planned.
- Render one frame: the expected files exist and the EXR layers, depth and codec match the Node Format settings.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release branch: compositing/types/output/file_output, files/media/image_formats, render/layers/passes) and the 5.2 source (rna_nodetree.cc File Output properties, rna_scene.cc media types, bl_ui space and node menus). Fixed: the 5.2 node has Directory, File Name, Media Type, Node Format, Images/Layers and Override Node Format (not Base Path, Add Input, Use Node Format or OpenEXR MultiLayer format); the old text on overwrite, placeholders, padding without hashes, premultiplied alpha, EXR header and data-window behaviour, DWAA ratios and quality figures, codec speed claims, Nuke, Fusion, Resolve and After Effects behaviour, pass-name and vector conventions was removed because the manual does not state it.
Method: documentation only; no commands were run.
