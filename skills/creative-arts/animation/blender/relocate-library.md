---
id: creative-arts.animation.blender.relocate-library
name: relocate-library
category: creative-arts
field: animation
product: blender
tags: [blender, linked-libraries, relocate-library, reload-library, missing-libraries, external-data, pipeline]
level: practitioner
status: docs-checked
description: "Repair and swap linked libraries in Blender: Outliner Blender File mode, Reload, Relocate, Relocate Linked ID, Delete, broken-library placeholders, and Library.filepath in Python."
sources:
  - https://docs.blender.org/manual/en/latest/files/linked_libraries/link_append.html
  - https://docs.blender.org/manual/en/latest/editors/outliner/interface.html
  - https://docs.blender.org/api/current/bpy.types.Library.html
  - https://docs.blender.org/api/current/bpy.ops.outliner.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# relocate-library

Goal: a moved or renamed asset file does not kill a shot; repoint it in one step.

## Where libraries live

Outliner display mode **Blender File** lists linked data-blocks together with the path of the blend-file they come from (linked data carries a chain icon). Right-click a linked blend-file there to get the library operations.

## Operations (context menu on the library)

- **Reload:** immediately update the current file with the latest version of the linked data-blocks, without reopening the file.
- **Relocate:** replace the library by a different file. Use it to fix a broken library (file moved or renamed) or to switch to a variation of the same data in another file. The operator (`outliner.lib_operation` with `RELOCATE`) selects a new path and reloads all of the library's data.
- **Delete:** deletes the library and all its items (`DELETE`).
- **Relocate Linked ID:** right-click a *directly* linked data-block > `Data-block > Relocate` to replace it by another ID from the same or a different library, for example after the ID was renamed. Only available for directly linked data-blocks that are not dependencies of other linked data.

## Broken libraries

If Blender cannot find a library when loading, it creates placeholder data-blocks in place of the missing linked ones, so references are not lost. Relocating the missing library restores the data automatically.

## Bulk fixes

`File > External Data > Find Missing Files...` is for external files (the operator `file.find_missing_files` tries to find missing external files); use Relocate for libraries. A script for a moved project root:

```python
import bpy
for lib in bpy.data.libraries:
    lib.filepath = lib.filepath.replace("//../old_assets/", "//../assets/")
    lib.reload()
```

`Library.filepath` and `Library.reload()` are documented members of the Library type.

## Gotchas

- Relative paths survive moving a project folder; see `creative-arts.animation.blender.make-paths-relative` (library paths follow the same relative-path rules).
- Circular dependencies between files tend to give missing links; keep links one-directional.

## Verify

The Blender File mode shows no placeholder items, and in Python `[l.filepath for l in bpy.data.libraries if not os.path.exists(bpy.path.abspath(l.filepath))]` returns an empty list (import `os` first).

## Checked

Date: 2026-10-27. Documentation: Blender manual 5.3 (files/linked_libraries/link_append.rst), the current Python API (Library.filepath, Library.reload, bpy.ops.outliner.lib_operation, id_linked_relocate, bpy.ops.file.find_missing_files) and the 5.3 release source (space_topbar.py External Data menu).
Confirmed: Reload and Relocate behaviour and menu paths, Relocate Linked ID rules, broken-library placeholders, Delete semantics, script attributes. Removed unconfirmed claims: "datablocks re-link by name", "Info editor lists LIB: ... missing", `Make Paths Relative` applying to libraries, and where nested libraries are relocated.
Method: documentation only; no commands were run.
