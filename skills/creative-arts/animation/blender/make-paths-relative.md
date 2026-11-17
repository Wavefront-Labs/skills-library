---
id: creative-arts.animation.blender.make-paths-relative
name: make-paths-relative
category: creative-arts
field: animation
product: blender
tags: [blender, relative-paths, make-paths-relative, make-paths-absolute, external-data, file-management, pipeline]
level: practitioner
status: docs-checked
description: "Keep Blender projects portable: the // prefix, Default To Relative Paths, External Data > Make Paths Relative/Absolute, Remap Relative on Save As, and bpy.path helpers."
sources:
  - https://docs.blender.org/manual/en/latest/files/blend/open_save.html
  - https://docs.blender.org/manual/en/latest/editors/preferences/save_load.html
  - https://docs.blender.org/api/current/bpy.path.html
  - https://docs.blender.org/api/current/bpy.ops.file.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# make-paths-relative

Goal: a project folder that opens correctly on any machine.

## The `//` prefix

A relative path is stored as a partial path evaluated against the directory of the referencing .blend. When typing a path in a text field, a double-slash prefix `//` makes it relative; the File Browser has a *Relative Path* checkbox where supported. `//` as a default path means the folder of the open .blend. You cannot use relative paths in a new untitled file; save it first.

With relative paths you can move the .blend as long as the external files move along with it (for example send a folder holding the .blend and a subfolder of images).

## Settings and commands

- **Preferences > Save & Load > Default To > Relative Paths:** default for the Relative Path option when loading external files such as images, sounds and linked libraries; ignored if a path is already set. Python: `preferences.filepaths.use_relative_paths` (default True).
- `File > External Data > Make Paths Relative` (`file.make_paths_relative`): make all paths to external files relative to the current .blend.
- `File > External Data > Make Paths Absolute` (`file.make_paths_absolute`): make them absolute.
- **Remap Relative** (Save As option): when saving to a new location, relative paths such as linked libraries and images are remapped. The manual's tip: to relocate a .blend relative to its linked resources, use File > Save As with Remap Relative.

## Scripting

```python
bpy.ops.file.make_paths_relative()
p = bpy.path.abspath(img.filepath)    # resolve the // prefix for os calls
img.filepath = bpy.path.relpath(p)
```

`bpy.path.abspath(path, *, start=None, library=None)` resolves `//` against the current .blend (or the library's path when `library` is given); `bpy.path.relpath(path, *, start=None)` goes the other way.

## Gotchas

- Unsaved files cannot hold relative paths; save first.
- Moving the .blend without its external files breaks relative references; move them together or use Save As with Remap Relative.

## Verify

After copying the project to another location, `File > External Data > Report Missing Files` reports nothing.

## Checked

Date: 2026-10-27. Documentation: Blender manual 5.3 (files/blend/open_save.rst, editors/preferences/save_load.rst), the current Python API (bpy.path, bpy.ops.file, PreferencesFilePaths.use_relative_paths) and the 5.3 release source (space_topbar.py External Data menu).
Confirmed: `//` semantics, untitled-file limit, preference location and wording, menu entries and operator descriptions, Remap Relative, bpy.path signatures. Removed unconfirmed claims: the preference living under File Paths (it is Save & Load > Default To), the Remap Relative default being on, cross-drive and Windows behaviour, and which output, cache or compositor paths the command covers.
Method: documentation only; no commands were run.
