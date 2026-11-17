---
id: creative-arts.animation.blender.collection-color-tags
name: collection-color-tags
category: creative-arts
field: animation
product: blender
tags: [blender, collections, outliner, collection-color-tags, color-tags, collection-manager, scene-organisation]
level: practitioner
status: docs-checked
description: "Organise Blender scenes with collection colour tags (Set Color Tag, Color 01-08), naming conventions and the Collection Manager extension for visibility switching."
sources:
  - https://docs.blender.org/manual/en/latest/scene_layout/collections/introduction.html
  - https://docs.blender.org/manual/en/latest/editors/outliner/editing.html
  - https://docs.blender.org/api/current/bpy_types_enum_items/collection_color_items.html
  - https://extensions.blender.org/add-ons/collection-manager/
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# collection-color-tags

Goal: a scene a stranger can read, with colour by purpose and consistent names.

## Colour tags

- Outliner: right-click a collection > **Set Color Tag** (`outliner.collection_color_tag_set`) to assign or clear the tag for the selected collection(s).
- The tag is shown as part of the collection icon in the Outliner and in various other menus. The available colours are defined by the interface theme.
- Python: `collection.color_tag` is an enum with `NONE` and `COLOR_01` to `COLOR_08`, for example `[c.name for c in bpy.data.collections if c.color_tag == 'COLOR_01']`.
- Pick a convention (for example one colour for "do not render" helpers) and write it down in a text block in the file; colours carry no built-in meaning.

## Naming

- Prefix by type and keep it shot-agnostic: `CH_hero`, `SET_kitchen`, `LGT_key`, `FX_dust`, `CAM`.
- Collections nest like folders, so a character can be one top collection with `rig` and `mesh` children.

## Collection Manager (extension)

- Published on extensions.blender.org as "Collection Manager" by Imaginer ("Manage collections and their objects"); it was one of the add-ons bundled with Blender 4.1 and is now installed from Get Extensions. The listing gives its location as 3D Viewport, Object Mode, with shortcut `M`.
- For its features, keys and settings, follow the Documentation link on the extension's page rather than relying on a summary here.

## Gotchas

- A colour tag is stored per collection; set it on each collection you want coloured.

## Verify

The Python one-liner above lists exactly the collections you tagged, and the Outliner icons show the colour.

## Checked

Date: 2026-10-27. Documentation: Blender manual 5.3 (scene_layout/collections/introduction.rst, editors/outliner/editing.rst), the current Python API enum Collection Color Items, and the Collection Manager listing on extensions.blender.org.
Confirmed: Set Color Tag operator and behaviour, theme-defined colours, NONE and COLOR_01 to COLOR_08, extension author, bundling history and location. Removed unconfirmed claims: the theme path "Collection Color", multi-select behaviour, inheritance of tags, and QCD slot and key details.
Method: documentation only; no commands were run.
