---
id: creative-arts.animation.blender.fluid-cache-types
name: fluid-cache-types
category: creative-arts
field: animation
product: blender
tags: [blender, fluid, mantaflow, fluid-cache-types, replay-cache, modular-cache, openvdb]
level: practitioner
status: verified
description: "Choose Mantaflow cache types (Replay, Modular, All), directories, file formats, resumable bakes and freeing caches safely."
sources:
  - https://docs.blender.org/manual/en/latest/physics/fluid/type/domain/cache.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# fluid-cache-types

## Cache panel (Domain > Cache)

- **Cache Directory**: where baked files go. Inside it each simulation type (mesh, particles, noise) gets its own directory.
- **Type**:
  - **Replay**: the cache bakes as you play the timeline; only works when Playback Sync is set to Play Every Frame (use Modular or All with Frame Dropping or Sync to Audio).
  - **Modular**: step-by-step baking; the bake buttons sit in separate panels (Bake Data in Settings, Bake Noise, Bake Mesh, Bake Particles, Bake Guides).
  - **All**: one **Bake All** button in the Cache panel bakes every enabled step; **Free All** deletes the cache. Bake All cannot be paused or resumed.
- **Frame Start / End**: the simulation is only calculated for positive frames between Start and End; raise End for longer sims. **Offset** shifts frames when loading from the cache (not when baking).
- **Resumable**: stores extra data so a paused bake can continue; avoid it at high resolutions because more data is written.
- **Volumetric Data > Format**: Uni Cache (one `.uni` file per simulation object) or OpenVDB (one `.vdb` file per frame holding all grids and particles). OpenVDB-only options: **Compression** (Zip, Blosc, None) and **Precision** (`openvdb_data_depth`; the 4.5.14 enum offers only 32 and 16, Half 16 being the default, so the Mini 8-bit step the manual mentions is not selectable here).
- **Meshes** (liquids only): Binary Object (`BOBJECT`, the default) or Object (`OBJECT`). Python defaults on a new domain: `cache_type` REPLAY, `cache_data_format` OPENVDB (items UNI, OPENVDB), `openvdb_cache_compress_type` BLOSC (items ZIP, BLOSC, NONE), `cache_frame_start` 1, `cache_frame_end` 250, `cache_particle_format` UNI only.

## Gotchas

- Fluid simulations use their own cache, not the general point-cache Bake operators.
- If the mesh has modifiers, the render settings are used when exporting the mesh to the solver.
- Esc aborts a Bake All; Modular bakes can be paused and resumed.

## Verify

After baking, the cache directory holds one sub-directory per simulation type with files per frame, and the viewport plays the sim back without re-simulating.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (physics/fluid/type/domain/cache; branch blender-v5.2-release) and the 5.2 source (rna_fluid.cc). Confirmed: Cache Directory, Type (Replay/Modular/All) and the Playback Sync requirement, Frame Start/End/Offset, Resumable, Uni Cache vs OpenVDB, Compression and Precision options, Meshes formats, Bake All/Free All behaviour.

Run check, 2026-11-01, Blender 4.5.14 LTS headless (bpy, factory settings): FluidDomainSettings cache_type items REPLAY/MODULAR/ALL, formats, compression, precision, frame start 1 and end 250, resumable, cache_directory and offset exist; fluid operators bake_all, bake_data, bake_noise, bake_mesh, bake_particles, bake_guides, free_all and pause_bake exist; shipped properties_physics_fluid.py labels the buttons Bake All and Free All. Not run (confirmed from the manual only): the Playback Sync requirement for Replay, the directory layout after baking, the Esc and pause behaviour and the modifier render-settings note.

Method: manual text and shipped UI scripts confirmed from documentation; the listed behaviour run headless in Blender 4.5.14.
