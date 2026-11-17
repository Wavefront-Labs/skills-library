---
id: creative-arts.animation.blender.asset-ingest-script
name: asset-ingest-script
category: creative-arts
field: animation
product: blender
tags: [blender, asset-ingest-script, asset-ingest, asset-mark, asset-library, asset-catalogs, pipeline]
level: advanced
status: verified
description: "Ingest models into a Blender asset library from a script: append from files, asset_mark, catalogs and tags, custom previews, and saving library .blend files."
sources:
  - https://docs.blender.org/api/current/bpy.types.ID.html#bpy.types.ID.asset_mark
  - https://docs.blender.org/api/current/bpy.types.AssetMetaData.html
  - https://docs.blender.org/api/current/bpy.types.BlendDataLibraries.html
  - https://docs.blender.org/manual/en/latest/files/asset_libraries/catalogs.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# asset-ingest-script

Goal: turn a folder of source files into a browsable asset library with catalogs, tags and previews, repeatably.

## Steps per source file

```python
import bpy, uuid, pathlib

def ingest(src, catalog_id, tags):
    with bpy.data.libraries.load(str(src), link=False) as (data_from, data_to):
        data_to.objects = list(data_from.objects)
    for ob in data_to.objects:
        if ob is None or ob.type != 'MESH':
            continue
        bpy.context.scene.collection.objects.link(ob)
        ob.asset_mark()
        meta = ob.asset_data
        meta.catalog_id = catalog_id
        meta.description = f"Ingested from {src.name}"
        meta.author = "Studio"
        for t in tags:
            meta.tags.new(t, skip_if_exists=True)
```

For collections as assets (multi-object props), load `data_from.collections`, link them and mark the collection instead.

## Catalogs

Catalogs live in `blender_assets.cats.txt` at the library root:

```
VERSION 1

0f6a1e0e-8b8c-4f55-9a8f-3c4a1d9d7e21:Props/Crates:Props-Crates
```
Format `{UUID}:{path}:{simple name}` per line after a `VERSION 1` line (UTF-8; Blender writes a `blender_assets.cats.txt~` backup when it updates the file). Generate a UUID once per path (`uuid.uuid4()`) and keep a mapping so reruns reuse the same id; assets point to catalogs by UUID.

## Previews

- `ob.asset_generate_preview()` generates the preview image (it may be scheduled in a background thread, so do not save the file straight away; in 4.5.14 background mode `ob.preview` was set with `image_size` (128, 128) right after the call).
- To use your own thumbnail, render it yourself and load it with `bpy.ops.ed.lib_id_load_custom_preview(filepath=png)` (the operator takes a `filepath`; call it with the asset as the context ID).

## Save the library file

`bpy.ops.wm.save_as_mainfile(filepath=str(lib_dir / "props_crates.blend"))`. Register the folder once as an asset library in Preferences; the Asset Browser then lists the marked assets in the .blend files inside it.

## Gotchas

- Keep marked objects linked into a scene while generating previews (practice).
- Re-ingesting the same file twice creates `.001` duplicates (tested: Crate and Crate.001); start each output file from `bpy.ops.wm.read_factory_settings(use_empty=True)`.
- `meta.catalog_id` must be a UUID string: assigning a non-UUID string raised no error and left the previous id in place. `meta.tags.new("wood")` without `skip_if_exists=True` on an existing tag created `wood.001`.
- Texture paths: `bpy.ops.file.make_paths_relative()` before saving, or pack, so the library survives moving.

## Verify

Open a fresh Blender, select the library in the Asset Browser, see assets under the right catalogs with previews and tags; drag one into a scene and check textures resolve.

## Checked

Blender 5.2 manual (blender-v5.2-release) and Python API 5.2 (docs.blender.org/api/current), read 2026-10-27.
- `ID.asset_mark()`, `ID.asset_data`, `ID.asset_generate_preview()` (may run in a background thread), `AssetMetaData.catalog_id/description/author`, `AssetTags.new(name, skip_if_exists=)`, `bpy.data.libraries.load(..., link=)` context manager, `bpy.ops.ed.lib_id_load_custom_preview(filepath=)`, `bpy.ops.file.make_paths_relative()`, `bpy.ops.wm.read_factory_settings(use_empty=)`: API 5.2.
- Catalog file name, `{UUID}:{path}:{simple name}` line format, VERSION line and `~` backup: manual asset catalogs page.
- Removed as unconfirmed: the background-mode GPU preview claim, the fake-user claim, the Preferences menu path for asset libraries.

Run check, 2026-11-01, Blender 4.5.14 LTS headless: the `ingest` function as written ran against a saved .blend (objects loaded by `libraries.load(link=False)` are in no scene until linked; the asset got the catalog UUID, description, author and tags `wood`, `crate` with the duplicate skipped); an object that is already an asset keeps its `asset_data`, catalog and tags after `libraries.load`; `asset_mark`, `asset_clear`, `asset_generate_preview` exist on IDs and take no arguments; `AssetMetaData` has author, description, copyright, license, tags, active_tag, catalog_id, catalog_simple_name; `bpy.ops.ed.lib_id_load_custom_preview` has a `filepath` property; `bpy.ops.file.make_paths_relative()` and `save_as_mainfile` ran; Blender did not write `blender_assets.cats.txt` on save. Unrun: the catalog file format and the `~` backup (documentation only), custom previews, registering the folder in Preferences, the Asset Browser, collections as assets.
Method: documentation checked against the manual and API pages; the code and operators were run headless in Blender 4.5.14.
