---
id: creative-arts.animation.blender.output-path-tokens
name: output-path-tokens
category: creative-arts
field: animation
product: blender
tags: [blender, output-settings, output-path-tokens, frame-padding, output-path, render-output]
level: practitioner
status: docs-checked
description: "Write Blender render output paths: relative // paths, # frame padding, path templates with {variables}, Overwrite and Placeholders for simple farms."
sources:
  - https://docs.blender.org/manual/en/latest/render/output/properties/output.html
  - https://docs.blender.org/manual/en/latest/files/file_paths.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---
# output-path-tokens

Goal: frames land in the right folder with correct names on every machine.

## Path rules (Output Properties > Output > File Path)
- A `//` prefix means the directory of the current blend file, so `//render/sh010_` is relative to the project and survives moving it.
- When rendering an animation, the frame number is appended at the end of the file name with four padded zeros (for example `image0001.png`). Adding `#` characters anywhere in the name sets the padding: `image_##_test.png` becomes `image_01_test.png`.
- **File Extensions** adds the correct extension per file type.
- **Overwrite** and **Placeholders** (Image and Multi-Layer EXR image sequences): the manual's primitive render farm hint is a shared network directory with Overwrite off and Placeholders on, then several machines rendering to it.
- The panel header checkbox toggles automatic saving; animation renders (Ctrl-F12) write to the output path and still renders (F12) are not saved automatically.

## Path templates
Template expressions are written `{variable}` and substituted when the path is used, for example `//my_render_dir/{blend_name}.png`; the path field keeps the template text. They are currently supported only for the render output path in Scene properties and the Compositor File Output node paths.
- All template-capable paths: `blend_name`, `blend_dir`, `blend_name_lib`, `blend_dir_lib`.
- Render output paths only: `fps`, `resolution_x`, `resolution_y` (includes the resolution scale), `scene_name`, `camera_name`.
- File Output node path properties only: `node_name`.
- Format specifiers: `{fps:###}` gives at least 3 integer digits (`dance_030.png`), `{fps:.###}` gives exactly 3 decimals (`dance_29.970.png`).
- A literal brace is written `{{` or `}}`. A malformed expression (for example an unclosed brace) highlights the path field red and can block actions.

## Gotchas
- Variable names are fixed; anything else (for example a shot or version name) is not a template variable, so set those parts of the path from a script.

## Verify
Render frame 1 and check the file appears in the expected folder with the expected name.

## Checked
Date: 2026-10-27. Documentation: Blender manual, Render Output panel and File Paths (Path Templates) pages, branch blender-v5.2-release. Confirmed: // prefix, frame appending and # padding, File Extensions, Overwrite and Placeholders, template syntax, variable list, format specifiers, brace escaping, error highlighting, supported path types. Removed unconfirmed or wrong claims: the {shot}, {version} and {layer} template example (not variables), the 5.0+ version gate, folder creation on render, Windows drive-letter and command-line farm advice, and the working-directory remark.
Method: documentation only; no commands were run.
