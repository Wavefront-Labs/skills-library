---
id: creative-arts.animation.blender.bake-path-packed
name: bake-path-packed
category: creative-arts
field: animation
product: blender
tags: [blender, bake-path-packed, packed-bake, bake-directory, bake-node, simulation-nodes, geometry-nodes]
level: practitioner
status: docs-checked
description: "Choose where geometry node bakes live: packed in the .blend versus a disk bake directory, default and custom bake paths, relative paths, farms and cleaning stale bake files."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/baking.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/geometry/operations/bake.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---
# bake-path-packed

Goal: choose where geometry node bakes (Bake node and simulation zones) are stored.

## Rules from the manual

- The .blend file must be saved to disk before data can be baked.
- Baked data is not guaranteed to be readable by another Blender version.
- Data is not written until the Bake operation is run. *Bake Geometry Node* bakes the simulations and Bake nodes in all modifiers of the selected objects.

## Bake Target (per Bake node)

- **Inherit from Modifier**: copies the setting from the modifier containing the node; this is the default.
- **Packed**: the baked data is packed into the .blend file, so no separate file is needed.
- **Disk**: the baked data is stored in a separate directory on disk.
- **Custom Path** with **Bake Path**: where on disk the data is stored. This path is also used for simulation zones.
- **Pack / Unpack**: pack or unpack already baked data. When unpacking, the options are the same as the *Unpack Resources* operator.
- **Delete Geometry Node Bake** (trash icon): deletes the bake data.

## Gotchas

- An unsaved file cannot bake: save first.
- Baked geometry that references other data-blocks (currently materials only) is listed in Sidebar → Node → Data-Block References, where the references can be changed after baking.

## Verify

Bake, save and reopen the file: the Bake node shows the baked frame count; for a Disk bake check the Bake Path exists; a Packed bake works on another machine without a cache folder.

## Checked

2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch) and the 5.2 source UI scripts. Confirmed: Bake Target options (Inherit from Modifier, Packed, Disk), Custom Path and Bake Path, Pack/Unpack, Delete Geometry Node Bake, Bake Geometry Node scope, save-first and cross-version warnings, Data-Block References (Geometry Nodes baking and Bake node pages). Removed the unsupported default path pattern, version gate, farm advice and cleanup claims.

Method: documentation only; no commands were run.
