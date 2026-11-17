---
id: creative-arts.animation.blender.mesh-sequence-cache
name: mesh-sequence-cache
category: creative-arts
field: animation
product: blender
tags: [blender, mesh-sequence-cache, alembic, usd, modifiers, cache, motion-blur]
level: practitioner
status: docs-checked
description: "Load animated Alembic or USD geometry in Blender with the Mesh Sequence Cache modifier: Object Path, Read Data, Sequence, Frame Offset and velocity settings."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/modify/mesh_sequence_cache.html
  - https://docs.blender.org/manual/en/latest/files/import_export/alembic.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# mesh-sequence-cache

The modifier loads data from Alembic and USD files. It supports static meshes but mostly loads animated ones, also curves, file sequences, and meshes with varying topology (such as fluid simulation results). Importing an Alembic or USD file automatically adds it to time-varying meshes.

Time-varying object transforms (location, rotation, scale) use the Transform Cache constraint. Other cache formats (MDD, PC2) load through the Mesh Cache modifier instead.

## Options

- **Cache File** (data-block) and **File Path**: the Alembic or USD file.
- **Object Path**: path of the object inside the archive or stage.
- **Read Data**: Vertices (positions and deformation per frame), Faces (topology), UV, Color (vertex colour attributes if present), Attributes (custom attributes such as creases, custom normals, generic).
- **Time**: *Sequence* (cache split into a series of files); *Override Frame* with a *Frame* value to look up a custom time instead of the scene frame; *Frame Offset*, subtracted from the current frame for the lookup.
- **Velocity** (Alembic only): *Velocity Attribute* (default `.velocities`, standard in most Alembic files), *Velocity Unit* (Frame: not scaled by FPS; Second: scaled by 1/FPS), *Velocity Scale* (multiplier for motion blur).

## Gotchas

- If the Object Path no longer matches the file's hierarchy (for example after re-export with renamed nodes), the object cannot find its data; re-select the path.
- Check source and scene units yourself; the manual page does not describe unit scaling options on this modifier.

## Verify

Scrub the timeline: motion matches the source application; with a velocity attribute, motion blur renders correctly.

## Checked

Date: 2026-10-27. Documentation release: Blender manual, 5.2 release branch (Mesh Sequence Cache page). Confirmed options, Alembic-only velocity settings, auto-add on import, USD support and Mesh Cache/Transform Cache pointers. Removed the unconfirmed Manual Scale, Render Procedural and Maya-unit claims.
Method: documentation only; no commands were run.
