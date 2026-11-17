---
id: creative-arts.animation.blender.file-management
name: file-management
category: creative-arts
field: animation
product: blender
tags: [blender, blend-file, relative-paths, pack-resources, file-recovery, autosave, external-data, versioning, missing-files, save-versions, compress, recover-last-session]
level: practitioner
status: docs-checked
description: "Keep .blend files portable and recoverable: relative paths, pack/unpack, autosave and .blend1 recovery, versioning, compression, and what travels with a file."
sources:
  - https://docs.blender.org/manual/en/latest/files/blend/open_save.html
  - https://docs.blender.org/manual/en/latest/files/blend/packed_data.html
  - https://docs.blender.org/manual/en/latest/troubleshooting/recover.html
  - https://docs.blender.org/manual/en/latest/editors/preferences/save_load.html
  - https://docs.blender.org/manual/en/latest/editors/preferences/file_paths.html
  - https://docs.blender.org/api/current/bpy.path.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# file-management

Goal: a .blend that opens on any machine with every texture, cache and library found, and that you can get back after a crash.

## What is inside a .blend and what is not

Inside: the file's data-blocks and anything you have packed. **Outside**, referenced by path: external images, sounds, fonts and linked blend-files, plus videos from the Sequence Editor and Movie Clips, which cannot be packed.

Before every handoff, open the file from a copy of the project folder on another machine or drive and check that nothing is missing.

## Relative vs absolute paths

- Default is **relative** (`//textures/wood.png` — `//` means "folder of this .blend"). The *Default To - Relative Paths* option (Preferences, Save & Load) should stay on; absolute paths (a drive letter or `/home/...` root) break on every other machine.
- An **unsaved** file cannot use relative paths — save it before linking to external files.
- Moving a .blend relative to its linked resources: use `Save As` with *Remap Relative*, which remaps relative paths (images, linked libraries) when saving in a new location.
- The File menu's *External Data* submenu holds the pack and unpack commands.
- Python: `bpy.path.abspath(img.filepath)` resolves `//`; `bpy.path.relpath(p)` converts.

## Packing

- `File → External Data → Pack Resources` marks all eligible external files as packed; the actual packing happens on the next save. **Unpack Resources** writes them back out (*Use files in current directory (create when necessary)* reuses a file that already exists; the *Write files ...* options overwrite existing files). A single file can be packed or unpacked with the gift-box icon beside its path.
- Pack when: sending a single file to a client, archiving, or working on a laptop off the NAS. Don't pack on a shared pipeline — a packed file silently diverges from the texture on disk and Git/LFS diffs become useless.
- *Pack Linked Libraries* marks linked blend-files as packed on the next save. *Automatically Pack Resources* marks all eligible external files, existing or added later, as packed.
- Packed data shows a gift-box icon next to its path.

## Save behaviour

- `Ctrl S` saves; `Shift Ctrl S` Save As; `Ctrl Alt S` Save Incremental (a numerically incremented name that does not overwrite existing files); File → Save Copy saves a copy but returns to editing the original file (for sending snapshots).
- Save As options: **Compress** (Zstandard since 3.0, Gzip before; slower to save and load, so it can slow auto-saves), **Remap Relative**, **Save Copy**.
- `Save Versions` preference (default 2): saving renames the previous file to `file.blend1`, then `.blend2`; older files get higher numbers. Open the `.blend1` to return to that state.
- Numbered versioning by hand: in Save As, the plus/minus buttons (or Numpad +/-) beside the file name change the trailing number. Common convention: `<asset>_<task>_v###.blend` with a `publish/` folder holding the latest approved version.

## Autosave and crash recovery

- Preferences → Save & Load: *Auto Save* with a *Timer (Minutes)* writes a temporary backup (named like `<filename>_autosave.blend`) to the Temporary Directory (Preferences → File Paths → *Temporary Files*; it must be an existing directory, else the system temp directory is used). Recover via `File → Recover → Auto Save`, then immediately Save As.
- `File → Recover → Last Session` opens `quit.blend`, saved into the Temporary Directory when you quit under normal operation. After a crash, try Recover → Auto Save.
- Auto save does not save changes made in Sculpt, Texture Paint and Edit mode, and only one auto-saved file is kept per project, so save manually in those modes.
- Files in the temporary directory may be deleted on reboot or by disk-cleanup tools; set *Temporary Files* to a persistent folder.

## External caches and output

- Caches and render output are external files, not packed: check the *Render Output* and *Render Cache* paths (Preferences → File Paths) and copy cache folders with the project.
- Linked libraries: see `creative-arts.animation.blender.linking-appending`.

## Reducing file size

1. Delete unused data (see `creative-arts.animation.blender.outliner-collections`).
2. Unpack images that should live on disk.
3. Save with Compress.

## Gotchas

- Texture paths with `//../` outside the project root break when the project is moved alone. Keep assets under the project root.
- Save As to a new folder **without** Remap Relative = every path breaks.
- `Save Copy` doesn't change the current file's path; subsequent `Ctrl S` goes to the original — intentional.
- Unpack during production, pack at archive.

## Verify

- Copy the project folder to another drive/machine; open the file: textures appear, libraries resolve, caches play.
- After a forced kill of Blender, `File → Recover → Auto Save` lists the most recent auto-saved file.
- The `.blend1` opens to the previous saved state.

## Checked

2026-10-28. Confirmed against the Blender manual pages Opening & Saving, Packed Data, Recovering Data, Preferences Save & Load and File Paths, and the `bpy.path` API page: Save Incremental on `Ctrl Alt S` (the draft wrongly gave it to Save Copy), Save Versions default of 2, auto-save file naming, location and sculpt/texture paint/edit mode limitation, one auto-save kept, `quit.blend` on normal exit only, Zstandard since 3.0, Remap Relative, Pack/Unpack options, gift-box icon, unsaved files cannot use relative paths, `bpy.path.abspath` and `relpath`. Removed: the claim that quit.blend is written on crash, size-ratio figures, the Legacy Mesh Format and 4.2 version claims, factory-startup and command-line repair steps, cache folder and frame-number placeholder claims, and File menu commands the pages do not document (Report/Find Missing Files, Make Paths Relative/Absolute, Purge Unused Data).
Method: documentation only; no commands were run.

