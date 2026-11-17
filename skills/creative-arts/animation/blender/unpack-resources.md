---
id: creative-arts.animation.blender.unpack-resources
name: unpack-resources
category: creative-arts
field: animation
product: blender
tags: [blender, pack-resources, unpack-resources, unpack-item, external-data, file-management, textures]
level: practitioner
status: docs-checked
description: "Unpack Blender's packed external files: Unpack Resources methods, per-file unpack from the gift-box icon, Disable AutoPack, and unpack_all in Python."
sources:
  - https://docs.blender.org/manual/en/latest/files/blend/packed_data.html
  - https://docs.blender.org/api/current/bpy.ops.file.html
  - https://docs.blender.org/api/current/bpy.types.Image.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# unpack-resources

Goal: turn a self-contained (packed) .blend back into a normal project with files on disk, for example a downloaded asset whose textures you will edit externally.

## Know what is packed

Packed data is external files stored inside the .blend. You can tell by the small "gift box" icon next to its path. Some heavy files cannot be packed at all, such as videos from the Sequence Editor or Movie Clips. `File > External Data > Pack Resources` marks all eligible files as packed (actual packing happens on the next save); **Automatically Pack Resources** keeps doing so for files added later.

## Unpack everything

`File > External Data > Unpack Resources` (`file.unpack_all`), then choose:
- **Use files in current directory (create when necessary):** unpacks into the folder of the .blend (`//`), grouped into proper folders such as `textures`; if the target file already exists, that file is used instead of unpacking. The usual choice.
- **Write files to current directory (overwrite existing files):** same, but overwrites existing files.
- **Use files in original location (create when necessary):** unpacks to the original paths; an existing file is used instead.
- **Write files to original location (overwrite existing files):** same, but overwrites.
- **Disable AutoPack, keep all packed files:** only turns off *Automatically Pack Resources*.
The original location is the path stored when the file was packed, so it may not exist on your machine.

## Unpack one file

Click the gift-box icon left of the file path widget. Options: **Remove Pack** (mark as unpacked without writing or reloading), **Create <local file path>**, **Use <original file path>** (shown with *(differs)* or *(identical)* compared to the on-disk file; the file is not reloaded automatically), **Overwrite <original file path>**, **Create <original file path>**.

## Libraries

`File > External Data > Pack Linked Libraries` and `Unpack Linked Libraries` do the same for linked library files.

## Scripted

```python
bpy.ops.file.unpack_all(method='USE_LOCAL')
for img in bpy.data.images:
    if img.packed_file:
        img.unpack(method='WRITE_LOCAL')
```

`file.unpack_all` accepts `USE_LOCAL`, `WRITE_LOCAL`, `USE_ORIGINAL`, `WRITE_ORIGINAL`, `KEEP` and `REMOVE`; `Image.unpack(method='USE_LOCAL')` saves a packed image to disk.

## Gotchas

- With *Automatically Pack Resources* enabled, new external files keep being marked as packed; the unpack menu items are inactive while it is on, so turn it off first (Disable AutoPack option, or the File > External Data toggle).
- Save the .blend before unpacking to relative paths; relative paths need a saved file.

## Verify

`[i.name for i in bpy.data.images if i.packed_file]` is empty and `File > External Data > Report Missing Files` is clean.

## Checked

Date: 2026-10-27. Documentation: Blender manual 5.3 (files/blend/packed_data.rst), the current Python API (bpy.ops.file.unpack_all, Image.unpack) and the 5.3 release source (space_topbar.py External Data menu, where Pack Resources and Unpack Resources are inactive while auto-pack is on).
Confirmed: menu paths, all unpack method names and meanings, selective unpack options, un-packable file types, library pack and unpack entries, method enums. Removed unconfirmed claims: separate sounds and fonts folders, an Image Editor > Image > Unpack menu, generated images packing as PNG, and a list that put "Remove Pack" among the bulk options.
Method: documentation only; no commands were run.
