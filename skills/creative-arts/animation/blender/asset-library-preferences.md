---
id: creative-arts.animation.blender.asset-library-preferences
name: asset-library-preferences
category: creative-arts
field: animation
product: blender
tags: [blender, asset-library, asset-library-prefs, import-method, asset-import-method, preferences]
level: practitioner
status: docs-checked
description: "Register Blender asset libraries in Preferences (Asset Libraries section) and pick the import method (Link, Append, Pack, Follow Asset or Preferences) per library and browser."
sources:
  - https://docs.blender.org/manual/en/latest/editors/preferences/asset_libraries.html
  - https://docs.blender.org/manual/en/latest/editors/asset_browser.html
  - https://docs.blender.org/api/current/bpy.types.UserAssetLibrary.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# asset-library-preferences

Goal: every artist sees the same studio libraries, and assets come in linked, appended or packed as the pipeline expects.

## Register a library

Preferences > **Asset Libraries** section (in older releases the list lived under File Paths): add an entry to the list.
- **Name:** only used inside Blender to identify the library; can be changed any time.
- **Path:** the directory containing the library (local libraries). Any asset in .blend files in that directory or its subdirectories becomes available in the Asset Browser. Online libraries use a **URL** instead.
- **Import Method:** default method for this library, used unless the Asset Browser overrides it. Not available for built-in libraries.
- **Relative Path:** store the library location relative to the file where possible.
- Registered-in-Preferences libraries are always available; libraries registered in project settings are available only inside that project.

## Import methods

- **Link:** linked, read-only, stays in sync with the library. Not supported for online libraries.
- **Append:** independent copy of the asset and its dependencies; every import is new data.
- **Pack:** imports as linked data and immediately packs it into the file, for self-contained files.
- The Python enum also includes `APPEND_REUSE` (Append (Reuse Data)), which shares nested data such as textures or meshes between imports. The Preferences page of the 5.3 manual does not list it.

## Per-browser override

Asset Browser header (shown when a library other than *Current File* or *Essentials* is selected): **Import Method** with *Follow Asset or Preferences*, Link, Append, Pack. An asset can also state a preferred method (Asset Details > Import > Preferred Method), honoured when *Follow Asset or Preferences* is selected.

## Scripting

```python
lib = bpy.context.preferences.filepaths.asset_libraries.new(name="Studio", directory="/mnt/assets")
lib.import_method = 'LINK'
bpy.ops.wm.save_userpref()
```

`AssetLibraryCollection.new(name='', directory='')` and `UserAssetLibrary.import_method` are documented; per the API reference the default import method is `'PACK'`.

## Gotchas

- First load of a library takes longer; Blender indexes it and stores the index in the local cache directory.
- Each Blender version keeps its own preferences; import them from the previous version on first start.
- Online asset downloads require Online Access to be enabled in Preferences.

## Verify

The Asset Browser lists the library; after a drag, the Outliner shows a chain icon for linked data and none for appended data.

## Checked

Date: 2026-10-27. Documentation: Blender manual 5.3 (editors/preferences/asset_libraries.rst, editors/asset_browser.rst, files/asset_libraries/introduction.rst) and the current Python API (UserAssetLibrary, AssetLibraryCollection.new, Asset Import Method enum).
Confirmed: Asset Libraries preferences section and fields, import method meanings, per-browser override names, scripting calls and the PACK default. Removed unconfirmed claims: network share performance advice, drive-letter relative path claim, "Append (Reuse Data) is the default".
Method: documentation only; no commands were run.
