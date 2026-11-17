---
id: creative-arts.animation.blender.file-output-base-path
name: file-output-base-path
category: creative-arts
field: animation
product: blender
tags: [blender, file-output, file-output-base-path, base-path, output-path]
level: practitioner
status: docs-checked
description: "Organise File Output node paths in Blender 5.x: Directory and File Name, relative // paths, subfolders from item names with slashes, #### frame padding and Python names."
sources:
  - https://docs.blender.org/manual/en/latest/compositing/types/output/file_output.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# file-output-base-path

Goal: compositor outputs land in a predictable folder structure on every machine.

## Directory and File Name (Blender 5.2)

The File Output node builds each path as `{Directory}/{File Name}{Socket Name}{frame number}.{extension}`.

- **Directory**: the base output directory. Blender path properties allow `//` blend-relative paths (the 5.2 `directory` property is flagged as supporting blend-relative paths and path templates).
- **File Name**: the base name; the final name can also include frame numbers or layer names depending on settings.
- With **Media Type** *Image*, an input name containing `/` or `\` is read as a directory hierarchy (for example `passes/diffuse` or `masks/object_01`), and missing directories are created automatically.
- `####` in the File Name or in an image name forces where the frame number appears, padded with zeros to the number of `#` characters. It also makes a single render carry the frame number.
- **Output Paths** panel (Sidebar > Node > Properties) shows the final path and extension for each input, so you can verify the structure. **File Extensions** controls whether the extension is added.

The 4.5 manual describes a single **Base Path** setting, composed as `{base path}/{file name}{frame number}.{extension}`. The 5.2 manual does not describe how older files are converted, so re-check Directory, File Name and the input names after opening an older file.

## Example structure

```
render/<shot>/<version>/
    beauty/<shot>_beauty.####.exr
    passes/<shot>_passes.####.exr
    review/<shot>.####.jpg
```

The dot before the frame number is a naming convention that many sequence readers expect; it is not a Blender requirement.

## Setting from a script

The 5.2 node exposes `directory`, `file_name`, `format` (an ImageFormatSettings with `media_type`), `file_output_items` and `use_file_extension`. The scene's compositor tree is `scene.compositing_node_group`. Check the Python API reference for your version before scripting, since the layout changed in 5.0.

```python
node = scene.compositing_node_group.nodes["File Output"]
node.directory = f"//../render/{shot}/v{ver:03d}/comp/"
node.file_name = f"{shot}_beauty"
```

## Gotchas

- Use blend-relative `//` paths rather than absolute Windows paths when the file is rendered on other machines.
- The scene's main Output path also writes the render result; File Output nodes write in addition to it.

## Verify

Render one frame and compare the Output Paths panel and the folder tree on disk with the structure you planned.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release branch, compositing/types/output/file_output) and the 5.2 source (rna_nodetree.cc File Output properties; bl_operators/clip.py for scene.compositing_node_group). Fixed: Directory and File Name are the 5.2 fields; the old 4.x file_slots snippet and the node_tree attribute were replaced. Removed unconfirmed claims about farm behaviour and automatic version folders.
Method: documentation only; no commands were run.
