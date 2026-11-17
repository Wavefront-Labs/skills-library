---
id: creative-arts.animation.blender.multiple-caches
name: multiple-caches
category: creative-arts
field: animation
product: blender
tags: [blender, physics-bake, point-cache, multiple-caches, cache-list]
level: practitioner
status: docs-checked
description: "Manage multiple point caches on one Blender physics object: the caches list, naming for disk files, adding and removing caches, and what is not stored per cache."
sources:
  - https://docs.blender.org/manual/en/latest/physics/baking.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# multiple-caches

## Caches list

The point cache panel shows a list of caches, with + and - buttons to add or remove a cache. The manual says Blender allows storing and managing multiple caches at once for the same physics object. Double-click an entry to give it a name. The active cache is the one used.

## Naming and disk files

- A named cache is stored in files starting with that name: for example `MyCache_xxxxxx_yy.bphys`.
- An unnamed cache (the default) uses a filename derived from the object name, for example `43756265_xxxxxx_yy.bphys`.
- Manual warning: with several caches on one object, always specify a cache name. An object with several physics systems that all have unnamed caches causes conflicts and can result in losing cache files.

## Uses

- Takes: bake cloth with different settings into differently named caches and switch the active cache to compare without re-baking. Note the settings in the cache name, because the list is described by the manual only as managing caches, not their settings (practical advice).
- Different frame ranges for different shots in one file.

## Gotchas

- Deleting a cache entry with the minus button removes that cache.
- Geometry Nodes bakes and Mantaflow fluid caches use their own systems, not this list (Bake nodes: see bake-still-animation). The point-cache UI source marks Fluid as using its own cache.
- Rigid body caches do not show the caches list in the UI source.

## Verify

Switch the active cache: playback changes to the other take without simulating again.

## Checked

Date 2026-10-27. Blender manual 5.2 (blender-v5.2-release RST) and properties_physics_common.py on main.
Confirmed: caches list management, double-click naming, file name patterns, unnamed-cache conflict warning, add and remove operators in the UI source, Fluid using its own cache, no list for Rigid Body.
Removed as unconfirmed: that deleting a slot deletes its bake in every case beyond the remove operator, that settings are or are not snapshotted per cache, and the "per-system indices" claim.
Method: documentation only; no commands were run.
