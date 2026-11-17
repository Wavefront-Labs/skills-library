---
id: creative-arts.animation.blender.asset-catalogs
name: asset-catalogs
category: creative-arts
field: animation
product: blender
tags: [blender, asset-browser, asset-catalogs, asset-catalog, catalog-definition, blender-assets-cats, asset-library]
level: practitioner
status: docs-checked
description: "Organise Blender asset libraries with catalogs: create, nest, assign and save in the Asset Browser, the blender_assets.cats.txt file and UUIDs, and sharing catalogs across a team."
sources:
  - https://docs.blender.org/manual/en/latest/files/asset_libraries/catalogs.html
  - https://docs.blender.org/manual/en/latest/editors/asset_browser.html
  - https://docs.blender.org/api/current/bpy.types.AssetMetaData.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# asset-catalogs

Goal: a browsable asset tree (`Props/Furniture/Chairs`) that survives renames and works for everyone sharing the library.

## In the Asset Browser

- Create: `Header > Catalog > New Asset Catalog`, or the plus icon at the top of the catalog tree in the Source List region. Double-click a catalog name to rename it. Drag catalogs to re-nest them.
- An asset belongs to one catalog at a time. Assign by selecting assets and dragging them onto the catalog; dragging onto *Unassigned* removes it from any catalog.
- Selecting a catalog shows the assets of that catalog and of all its child catalogs.
- Moving a catalog does not touch the assets in it; they move along.
- **Save:** `Header > Catalog > Save Asset Catalog` or the save icon at the top of the tree writes your edits to the asset library. Catalogs are saved independently of the .blend.

## Menus

Catalogs also extend menus: node-group assets show up in the Add Modifier menu and in the Add menus of the Geometry Nodes editor and Compositor, with the catalog hierarchy defining the submenu. Contents of top-level catalogs named "Geometry Nodes" or "Compositing" go straight into the matching menus, skipping that top-level submenu. Assets placed directly inside those two catalogs appear under *Unassigned* in the menus.

## The definition file

Each library has one catalog definition file, `blender_assets.cats.txt`, in the library root. Blender creates it when catalogs are first saved and keeps a backup of the previous state as `blender_assets.cats.txt~`. It is UTF-8; after the version line each catalog is one line, `{UUID}:{path}:{simple name}`.

```
VERSION 1
313ea471-7c81-4de6-af81-fb04c3535d0e:catalog/without/simple/name:
ee9c7b60-02f1-4058-bed6-539b8d2a6d34:character/Ellie/poselib:character-Ellie-poselib
```

- Lines starting with `#` and empty lines are ignored; the first other line is the version indicator.
- Catalog paths use `/` only, are not empty, have no empty components (`a//b`) and may not contain `:` or `\`.
- Each asset stores the catalog **UUID** (and the simple name for recovery), so renaming or moving a catalog path does not break assignments, and no asset .blend needs changing.
- The UUID and simple name are normally hidden; Developer Extras (and the experimental Asset Debug Info option for UUIDs) reveal them.

## Teams

- Ship the cats file together with the .blend files when sharing a library.
- Keep it in version control; one catalog per line makes line-based merges workable.
- Two people who create the "same" catalog separately get two UUIDs; agree a canonical tree or merge by editing the file.
- Python: `asset.asset_data.catalog_id = "<uuid string>"`.

## Verify

Restart Blender, open the library: catalog tree identical, every asset in its catalog.

## Checked

Date: 2026-10-27. Documentation: Blender manual 5.3 (files/asset_libraries/catalogs.rst, editors/asset_browser.rst) and the current Python API (AssetMetaData.catalog_id).
Confirmed: menu names for create/save, one catalog per asset, child-catalog display, file name and backup name, line format and path rules, menu extension rules. Removed unconfirmed claims: an N-panel Catalog field, the "Current File" cats file location behaviour, and deleting a line returning assets to Unassigned.
Method: documentation only; no commands were run.
