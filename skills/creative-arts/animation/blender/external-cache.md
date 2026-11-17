---
id: creative-arts.animation.blender.external-cache
name: external-cache
category: creative-arts
field: animation
product: blender
tags: [blender, physics-bake, point-cache, external-cache, cache-path, disk-cache]
level: practitioner
status: docs-checked
description: "Read external point cache files in Blender: Disk Cache folder and file naming, External checkbox with Path and Index, library paths and sharing caches between machines."
sources:
  - https://docs.blender.org/manual/en/latest/physics/baking.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# external-cache

## Disk Cache

- **Disk Cache** stores the baked simulation in a folder named `blendcache_[filename]` alongside the blend-file. The blend-file must be saved first (the UI disables the options until then).
- File names follow `name_frame_index.bphys`. The cache **Name** in the caches list gives the file prefix; unnamed caches use a name derived from the object, so give unique names when several systems share an object.
- **Use Library Path**: when a physics object is linked into another blend-file, linked versions reference the same disk cache; otherwise they use independent caches.
- Linked or library-override data-blocks only support Disk Cache storage.

## External

- The **External** checkbox (shown for particle and hair systems) reads the cache from a user-specified file path instead of the normal folder, which suits caches produced elsewhere.
- Fields: **Path** (directory of the cache files) and **Index** (the last two digits of the file name).
- The manual's note: the cache name in the Caches List and the Index must exactly match the external cache files' name for it to work.

## Pipeline

- Simulate on one machine and copy the `blendcache_` folder along with the .blend.
- To version caches per take, copy the files to a differently named folder and point External Path at it, keeping the cache name and Index matching.

## Gotchas

- If the .blend is renamed the default folder name no longer matches, so copy or rename the folder as well (this follows from the folder naming rule).
- If an External cache shows nothing, check that the cache Name and Index match the file names.

## Verify

Open the .blend on another machine: the cache info line shows the frames found and playback is immediate.

## Checked

Date 2026-10-27. Blender manual 5.2 (blender-v5.2-release RST) and properties_physics_common.py on main.
Confirmed: blendcache folder naming, file name pattern, External with Path and Index and the matching note, Use Library Path meaning, Disk Cache for linked and overridden data, saved-file requirement.
Removed as unconfirmed: the Compression None/Lite/Heavy option (no such option in the 5.2 UI source), "External caches are read-only", and the versioned folder name example.
Method: documentation only; no commands were run.
