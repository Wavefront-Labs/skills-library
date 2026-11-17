---
id: creative-arts.animation.blender.brush-assets
name: brush-assets
category: creative-arts
field: animation
product: blender
tags: [blender, brush-assets, brush-asset-shelf, asset-shelf, sculpting, texture-painting, custom-brushes]
level: practitioner
status: docs-checked
description: "Manage Blender 4.3+ brushes as assets: Essentials library, Duplicate Asset, Save Changes to Asset, catalogs, metadata, preview images and migrating older brushes."
sources:
  - https://docs.blender.org/manual/en/latest/sculpt_paint/brush/brush_management.html
  - https://docs.blender.org/manual/en/latest/sculpt_paint/brush/brush_settings.html
  - https://developer.blender.org/docs/release_notes/4.3/sculpt/
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# brush-assets

Goal: a personal brush kit that survives across files and Blender versions.

## How it works (4.3 and later)

- Brushes are assets stored in asset libraries so they are available in any Blender session. Blender 4.3 introduced this; its release notes describe the asset shelf at the bottom of the 3D Viewport and Image Editor and the default Essentials brush assets.
- Changes to the settings of a brush asset are temporary and are discarded when Blender closes. Keep them with **Save Changes to Asset**, or make a new brush with **Duplicate Asset**. Loading another file while Blender stays open does not discard them.
- Two ways to manage brushes: asset operators (Blender manages storage in `.asset.blend` files) and manual storage (mark brush data-blocks as assets in blend files inside a library).

## Asset operators

Found in Sidebar > Tool > Brush Asset, Properties > Tool > Brush Asset, and the asset shelf context menu.

- **Duplicate Asset...**: copies the active brush as a new asset and activates it; a popup asks for Name, Library (configured in the Preferences) and Catalog (typing a new name or path creates a catalog).
- **Delete Asset**: permanently removes the asset from its library after confirmation.
- **Edit Metadata...**: Catalog, Author, Description. **Edit Preview Image...** opens a file browser to choose the preview.
- **Save Changes to Asset** and **Revert to Asset**.
- Only assets created with Duplicate Asset can be edited with these operators; others are greyed out. Brushes from the Essentials library cannot be edited.

## Manual storage

Append a brush into a file (it appears under Brushes in the Outliner's Blender File mode), right-click it and choose **Mark as Asset**, then save the file inside an asset library directory; add a library directory in the Preferences if needed. Use this for careful curation or sharing, and for converting pre-4.3 brushes.

## Gotchas

- Setting edits are lost on closing Blender unless saved with Save Changes to Asset (duplicated assets only).
- The unified icon on size, strength and colour shares a value across brushes.

## Verify

Start a new file: the custom brush appears in the asset shelf under its catalog with the saved settings.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release branch) and the Blender 4.3 sculpt release notes. Confirmed against sculpt_paint/brush/brush_management and brush_settings: temporary settings changes, Duplicate Asset popup fields, Delete Asset, Edit Metadata fields, Edit Preview Image (not a Load Custom Preview button), Save Changes and Revert, Essentials not editable, manual Mark as Asset workflow, .asset.blend storage, 4.3 introduction. Removed unconfirmed claims: Essentials brushes being linked on selection, pinning catalogs, shelf search and texture packing advice.
Method: documentation only; no commands were run.
