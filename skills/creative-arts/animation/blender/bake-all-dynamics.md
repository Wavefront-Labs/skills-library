---
id: creative-arts.animation.blender.bake-all-dynamics
name: bake-all-dynamics
category: creative-arts
field: animation
product: blender
tags: [blender, physics-bake, point-cache, bake-all-dynamics, free-all-bakes]
level: practitioner
status: docs-checked
description: "Bake all physics in a Blender scene at once with Bake All Dynamics, Delete All Bakes and Update All to Frame, plus disk cache, cache naming and staged baking."
sources:
  - https://docs.blender.org/manual/en/latest/physics/baking.html
  - https://docs.blender.org/manual/en/latest/physics/rigid_body/world.html
  - https://docs.blender.org/api/current/bpy.ops.ptcache.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# bake-all-dynamics

## Where

The point-cache buttons live in the Cache panels of the physics systems (for example Rigid Body World under Scene properties, and the cloth, soft body and particle caches). The scene-wide buttons are:

- **Bake All Dynamics**: bakes all physics systems in the scene, even those of different types.
- **Delete All Bakes**: deletes the bakes of all physics systems in the scene.
- **Update All to Frame**: bakes all physics systems to the current frame.

Per-system buttons are **Bake**, **Delete Bake**, **Calculate to Frame** and **Current Cache to Bake**. You need to be in Object Mode to bake.

## What it covers

Systems that use the general point cache: particles, cloth, soft body, rigid body world. Fluid (Mantaflow) simulations use their own cache and bake operators on the domain, not the general ones. Geometry Nodes Simulation and Bake nodes have their own bake controls (practice: bake them from their own panel, not from here).

## Order

Baking everything at once is useful for setups where different physics types interact. When one simulation depends on the final result of another (practice: cloth colliding with rigid bodies), bake the upstream one first, check it, then bake the dependent one.

## Cache naming and storage

- When there are several caches on one object, always give each a Cache Name: an unnamed cache takes its file name from the object, so several unnamed caches on one object conflict and can lose cache files (warning in the manual).
- **Disk Cache** writes the cache to a `blendcache_<filename>` folder beside the saved blend-file (save the file first). Without it the baked cache is stored inside the blend-file when saved.
- Data-blocks that are library overrides only support Disk Cache storage.
- **Cache Step** greater than 1 stores every nth frame for systems that support it (for example particles): smaller cache, result may differ from the original simulation.

## Command line

```bash
blender -b shot.blend --python-expr "import bpy; bpy.ops.ptcache.bake_all(bake=True); bpy.ops.wm.save_mainfile()"
```

`bpy.ops.ptcache.bake_all(bake=True)` is the scripted equivalent; `bpy.ops.ptcache.free_bake_all()` frees all bakes. Practice: enable Disk Cache first so the baked data is written to disk rather than depending on the saved blend-file.

## Gotchas

- Once baked, the cache is protected and simulation settings cannot be changed until the bake is deleted.
- Bake All Dynamics bakes every system in the scene, including ones you were happy with. Practice: to protect them, bake per system instead.
- Rigid Body World cache is created in memory until the file is saved: save the file first or the cache may be lost.

## Verify

After baking, the Delete Bake button becomes available on each system; changing a simulation setting is locked until you delete the bake.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release RST) and the current Python API docs.
Confirmed: Bake All Dynamics, Delete All Bakes and Update All to Frame wording and meaning; Disk Cache folder name and the library-override limitation; cache-name warning; `bpy.ops.ptcache.bake_all(bake=True)` and `free_bake_all()` signatures; Mantaflow uses its own cache. Removed: "Free All Bakes" label (the button is Delete All Bakes), claims about orange timeline bars and undo behaviour, and the Dynamic Paint listing (no doc coverage).
Method: documentation only; no commands were run.
