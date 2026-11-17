---
id: creative-arts.animation.blender.essentials-library
name: essentials-library
category: creative-arts
field: animation
product: blender
tags: [blender, asset-library, essentials-library, asset-bundles, bundled-assets, hair-node-groups, brushes]
level: practitioner
status: docs-checked
description: "Use Blender's bundled Essentials asset library (hair node groups, Smooth by Angle, brushes), the online Essentials option, and asset bundles from the blender.org Demo Files page."
sources:
  - https://docs.blender.org/manual/en/latest/files/asset_libraries/introduction.html
  - https://docs.blender.org/manual/en/latest/editors/preferences/asset_libraries.html
  - https://docs.blender.org/manual/en/latest/editors/asset_browser.html
  - https://www.blender.org/download/demo-files/
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# essentials-library

Goal: know what ships with Blender as assets so you do not rebuild it, and how to add official bundles.

## The Essentials library

- Blender includes assets out of the box in the **Essentials** library, selectable in the Asset Browser's Asset Library region. When Essentials or Current File is selected, the header's Import Method control is not shown.
- Contents per the manual: hair node groups (Geometry Nodes hair), the **Smooth By Angle** node group, and brushes for mesh sculpt, curve sculpt, texture paint, vertex paint and weight paint.
- The Smooth By Angle page describes it as a node group asset included in Essentials, with inputs Mesh, Angle and Ignore Sharpness.
- **Include Online Essentials** (Preferences > Asset Libraries > Essentials Library) adds more Essentials assets hosted online; downloading needs *Online Access* enabled in Preferences.
- Brush assets are preset assets: loaded and activated, not stored permanently in the file. Brush assets are saved in special `.asset.blend` files (asset system files) that can be opened but not saved normally; use Save As to make a normal copy.

## Asset bundles

- blender.org's *Demo Files* page has an **Asset Bundles** section ("Ready-to-use files to add to your Asset Libraries") by Blender Studio and community contributions.
- An *asset bundle*, as the manual defines it, is a .blend that references no other file, whose name ends in `_bundle.blend`, with external files packed. Open it, switch the Asset Browser to **Current File** and use **Copy Bundle to Asset Library**; pick the target library, choose the location in the File Browser and press *Copy to Asset Library*. The bundle's catalogs merge into the target library.
- Check each bundle's licence on its download page and record it in the asset metadata if you redistribute (see `creative-arts.animation.blender.asset-metadata`).

## Gotchas

- Edit copies, not the shipped library: Essentials is built in, so duplicate an appended asset (or use a library you own) for customisation.
- Different Blender releases ship different Essentials contents; check the Asset Browser of the version you use.
- Not everything described as an "asset bundle" has the Copy to Asset Library function; the file must follow the definition above.

## Verify

The Asset Browser shows the Essentials library with the hair and brush assets, and a copied bundle's assets appear under its own library.

## Checked

Date: 2026-10-27. Documentation: Blender manual 5.3 (files/asset_libraries/introduction.rst, editors/preferences/asset_libraries.rst, editors/asset_browser.rst, modeling/geometry_nodes/normals/smooth_by_angle.rst) and the blender.org Demo Files page (fetched 2026-10-27).
Confirmed: bundled contents, online Essentials option, asset bundle definition and copy workflow, brush preset behaviour, .asset.blend rules, the Demo Files Asset Bundles section. Removed unconfirmed claims: the install directory path, individual hair node names, Grease Pencil materials in Essentials, `Shade Auto Smooth` linkage, "import method is always Append (Reuse Data)", licence mix of bundles, Blender Studio site details, and version notes about 4.1 versus 4.2.
Method: documentation only; no commands were run.
