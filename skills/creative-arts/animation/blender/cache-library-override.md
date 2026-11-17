---
id: creative-arts.animation.blender.cache-library-override
name: cache-library-override
category: creative-arts
field: animation
product: blender
tags: [blender, physics-bake, point-cache, cache-library-override, linked-cache, library-override]
level: practitioner
status: docs-checked
description: "Simulate and cache physics on linked assets in Blender: library overrides, Disk Cache and Use Library Path, resyncing, and an Alembic handoff via Mesh Sequence Cache."
sources:
  - https://docs.blender.org/manual/en/latest/files/linked_libraries/library_overrides.html
  - https://docs.blender.org/manual/en/latest/physics/baking.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/modify/mesh_sequence_cache.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# cache-library-override

## Problem

Linked characters (from a library .blend) are read-only; their cloth, soft body or hair dynamics cannot bake or have settings changed until the data is overridden.

## Library Overrides

1. In Object Mode, `Object > Library Override > Make` in the 3D Viewport header (also available from the Outliner context menu). Only overrides created from the selected items are user-editable; Blender creates overrides for other required data-blocks automatically and marks most of them non-editable.
2. Overridden data-blocks only support **Disk Cache** storage for physics caches (turn Disk Cache on in the Cache panel and save the file first); the cache is written to a `blendcache_<filename>` folder beside the saved blend-file.
3. Practice: override only what you need, such as the cloth meshes and the armature.

## Library-side caches

The point cache option **Use Library Path** shares the disk cache when the physics object is linked into another blend-file: linked versions reference the same disk cache. When it is off, linked versions use independent caches. Use it for simulations baked once in the asset file.

## Alembic handoff (studio pattern)

Practice: the simulation stage bakes cloth and exports Alembic (`.abc`); the lighting file links the character and uses a **Mesh Sequence Cache** modifier on the meshes so no simulation runs in lighting files.

## Gotchas

- The relationships between linked data can change, which makes overrides outdated. Overrides resync automatically on file open; manual **Resync** and **Resync Enforce** are in the Outliner context menu under Library Override > Troubleshoot. A resync can delete edited overrides if they changed in the original library (a warning states how many; it can be undone before saving). Resync Enforce is more aggressive and can lose some overrides on ID pointer properties.
- The old proxy system was deprecated in Blender 3.0 and removed in 3.2; use library overrides.
- With several caches on one object, give each a Cache Name, or an unnamed cache takes its file name from the object and files can be lost.

## Verify

Bake in the shot file: the `blendcache_<filename>` folder appears beside the shot file, and the library file itself is untouched (check its modified time).

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release RST).
Confirmed: Make an Override menu path and "only selected items are editable"; overrides support Disk Cache only and `blendcache_[filename]` folder; Use Library Path behaviour; Resync / Resync Enforce locations and warnings; proxy deprecation 3.0 and removal 3.2; Mesh Sequence Cache modifier page exists. Removed: "Library Path" label (the option is Use Library Path) and the claim that colliders in a linked environment work without overrides (no doc coverage).
Method: documentation only; no commands were run.
