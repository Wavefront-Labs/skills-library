---
id: creative-arts.animation.blender.asset-metadata
name: asset-metadata
category: creative-arts
field: animation
product: blender
tags: [blender, asset-browser, asset-metadata, asset-tags, asset-author, licence, copyright, mark-as-asset]
level: practitioner
status: docs-checked
description: "Fill Blender asset metadata so libraries are searchable and legally clear: description, author, license, copyright, tags, and batch-setting via asset_data in Python."
sources:
  - https://docs.blender.org/manual/en/latest/editors/asset_browser.html
  - https://docs.blender.org/manual/en/latest/files/asset_libraries/introduction.html
  - https://docs.blender.org/api/current/bpy.types.AssetMetaData.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# asset-metadata

Goal: search for "oak" or "cc0" and find the right assets, with provenance recorded.

## Fields (Asset Browser, Asset Details region on the right; toggle with N)

- **Name:** unique per asset data-block type within the file.
- **Source:** full path of the .blend containing the asset, with *Open Blend File*.
- **License**, **Copyright**, **Description**, **Author:** optional free text, not used by Blender itself.
- **Tags:** free-chosen tokens; when you filter with the search field, assets whose tags partially match the term are shown too.
- **Import > Preferred Method:** lets an asset state how it should be imported (for example a sculpting base mesh that should always be appended), used when *Follow Asset or Preferences* is selected.
- Catalog assignment is separate (see `creative-arts.animation.blender.asset-catalogs`).

**Only metadata of assets contained in the current blend-file can be edited.** To change a library asset, open its .blend (via *Open Blend File*).

## Batch with Python

```python
for mat in bpy.data.materials:
    if mat.asset_data:
        ad = mat.asset_data
        ad.author = "Studio Lookdev"
        ad.license = "CC0-1.0"
        ad.copyright = "2026 Studio"
        if "wood" in mat.name.lower() and "wood" not in [t.name for t in ad.tags]:
            ad.tags.new("wood")
```

`AssetMetaData` has `author`, `license`, `copyright`, `description`, `catalog_id` and `tags`; `tags.new(name, skip_if_exists=False)` adds a tag (tested in 4.5.14: adding an existing name without `skip_if_exists` created `wood.001`). Blender 4.5.14 has no `import_method` property, so Import > Preferred Method is 5.x. The license and copyright fields are free text: an empty value does not mean the asset is free of licensing terms.

## Conventions worth adopting

- License as an SPDX identifier (`CC0-1.0`, `CC-BY-4.0`) so scripts can audit it; this is a team convention, Blender does not enforce a format.
- Tags lowercase, singular, nouns (`chair`, `oak`).
- Description: scale, source URL for downloaded assets.

## Removing asset status

- **Clear Asset** removes the asset metadata (catalog, description, author, tags), turning the asset into a regular data-block; the preview stays in the data-block, and the data-block's normal removal rules apply.
- **Clear Asset (Set Fake User)** does the same and also protects the data-block with a fake user so it survives saving.

## Verify

Browser search for a tag returns the expected set; a script listing assets with empty `license` returns nothing.

## Checked

Date: 2026-10-27. Documentation: Blender manual 5.3 (editors/asset_browser.rst, files/asset_libraries/introduction.rst) and the current Python API (AssetMetaData, AssetTags.new).
Confirmed: field names and editing restriction, tag search behaviour, Preferred Method, Clear Asset behaviours, Python attributes and tags.new signature. Removed unconfirmed claims: "4.0+" field history, tags not feeding catalog filters, third-party pack licence fields.
Run note, 2026-11-01, Blender 4.5.14 LTS headless: `AssetMetaData` has author, description, copyright, license, tags, active_tag, catalog_id and catalog_simple_name (no import method); materials, objects and collections can be marked with `asset_mark()`; `asset_clear()` exists.
Method: documentation checked against the manual and API pages; part of the claims were run headless in Blender 4.5.14 (see the run note), but other claims describe Blender 5.x features that 4.5.14 does not have, so the status stays docs-checked.
