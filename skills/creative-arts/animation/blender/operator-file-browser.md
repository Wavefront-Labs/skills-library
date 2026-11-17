---
id: creative-arts.animation.blender.operator-file-browser
name: operator-file-browser
category: creative-arts
field: animation
product: blender
tags: [blender, operator-file-browser, importhelper, exporthelper, fileselect-add, file-handler, addon-development]
level: practitioner
status: docs-checked
description: "Write import/export operators with a file browser: ImportHelper and ExportHelper, filter_glob, multiple files and directory, menu entries, and drag-and-drop FileHandler."
sources:
  - https://docs.blender.org/api/current/bpy_extras.io_utils.html
  - https://docs.blender.org/api/current/bpy.types.FileHandler.html
  - https://docs.blender.org/api/current/bpy.types.WindowManager.html#bpy.types.WindowManager.fileselect_add
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# operator-file-browser

Goal: File → Import → My Format that opens Blender's file browser, filters by extension and receives one or many paths.

## Import operator

```python
import bpy, os
from bpy.props import StringProperty, CollectionProperty, BoolProperty
from bpy_extras.io_utils import ImportHelper

class IMPORT_OT_points_csv(bpy.types.Operator, ImportHelper):
    bl_idname = "import_scene.points_csv"
    bl_label = "Import Points CSV"
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = ".csv"
    filter_glob: StringProperty(default="*.csv;*.txt", options={'HIDDEN'})
    files: CollectionProperty(type=bpy.types.OperatorFileListElement, options={'HIDDEN', 'SKIP_SAVE'})
    directory: StringProperty(subtype='DIR_PATH', options={'HIDDEN', 'SKIP_SAVE'})
    center: BoolProperty(name="Center", default=True)     # shows in the browser sidebar

    def execute(self, context):
        paths = [os.path.join(self.directory, f.name) for f in self.files] or [self.filepath]
        for p in paths:
            ...  # parse and build
        return {'FINISHED'}

def menu_import(self, context):
    self.layout.operator(IMPORT_OT_points_csv.bl_idname, text="Points (.csv)")

# register: bpy.types.TOPBAR_MT_file_import.append(menu_import)
# unregister: bpy.types.TOPBAR_MT_file_import.remove(menu_import)
```

`ImportHelper.invoke` opens the file selector for importing (`ImportHelper.invoke_popup` shows a confirmation popup when `filepath` is already set). Without the helper, call `context.window_manager.fileselect_add(self)` in your own `invoke` and return `{'RUNNING_MODAL'}`. `filename_ext` and `filter_glob` follow Blender's own templates (practice); the API pages do not list them.

## Export

`ExportHelper.invoke` opens the file selector with a default `filepath` based on the current .blend file name, and `check(context)` validates the filepath. Options draw in the sidebar via `draw(self, context)`.

## Drag and drop

```python
class IO_FH_points_csv(bpy.types.FileHandler):
    bl_idname = "IO_FH_points_csv"
    bl_label = "Points CSV"
    bl_import_operator = "import_scene.points_csv"
    bl_file_extensions = ".csv;.txt"
    @classmethod
    def poll_drop(cls, context):
        return context.area and context.area.type == 'VIEW_3D'
```
An operator that takes one dropped file needs `filepath: StringProperty(subtype='FILE_PATH', options={'SKIP_SAVE'})`; one that takes several needs `directory` (`DIR_PATH`) and `files` (a `CollectionProperty` of `OperatorFileListElement`), both with `SKIP_SAVE` and `HIDDEN`.

## Gotchas

- Mark `filter_glob` as a `HIDDEN` StringProperty (the convention in Blender's templates).
- `SKIP_SAVE` means the value is not remembered between invocations, so `files` does not keep the previous selection.
- Paths are absolute OS paths; convert with `bpy.path.relpath` before storing in the .blend.

## Verify

Import two CSVs at once by shift-selecting in the browser; drag a CSV into the viewport; the Adjust Last Operation panel changes Center and re-runs.

## Checked

Blender Python API 5.2 (docs.blender.org/api/current), read 2026-10-27.
- `bpy_extras.io_utils.ImportHelper` (invoke, invoke_popup, check) and `ExportHelper` (invoke with default filepath from the .blend name, check); `bpy.types.FileHandler` with `bl_import_operator`, `bl_file_extensions`, `poll_drop`; the required `filepath` property for single-file drops and `directory` + `files` (OperatorFileListElement) for multi-file drops; property flags HIDDEN and SKIP_SAVE meaning.
- Removed as unconfirmed: the 4.1 version tag and the claim that ExportHelper auto-appends the extension. `filename_ext` / `filter_glob` are kept as template conventions, labelled practice.

Method: documentation only; no commands were run.
