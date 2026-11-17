---
id: creative-arts.animation.blender.set-scene-orientation
name: set-scene-orientation
category: creative-arts
field: animation
product: blender
tags: [blender, camera-solve, set-scene-orientation, set-floor, set-origin, set-scale, camera-tracking]
level: practitioner
status: docs-checked
description: "Orient a solved camera in Blender: set floor from three tracks, origin, X or Y axis, wall, and real-world scale from two tracks with a known distance."
sources:
  - https://docs.blender.org/manual/en/latest/movie_clip/tracking/clip/toolbar/solve.html
  - https://docs.blender.org/api/current/bpy.ops.clip.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# set-scene-orientation

Goal: the solved scene sits on the ground plane, at the origin, with the right axes and real scale.

## Tools (Toolbar > Solve > Orientation)

The operators work on solved tracks (those with 3D bundles) and move, rotate or scale the camera (or its parent if present), per the Python API documentation:
- **Floor** and **Wall** (`clip.set_plane`, plane FLOOR or WALL): sets the plane based on 3 selected bundles.
- **Set Origin** (`clip.set_origin`): sets the active marker as the origin; the `use_median` option uses the median point of the selected bundles instead.
- **Set X Axis / Set Y Axis** (`clip.set_axis`): sets the direction of a scene axis; this assumes the selected track lies on a real axis connecting it to the origin.
- **Set Scale** (`clip.set_scale`): sets the scale of the scene by scaling the camera (or its parent), using the **Distance** between the selected tracks, in the active scene's units.
- **Apply Scale** (`clip.apply_solution_scale`): applies the scale to the solution itself so the distance between the selected tracks equals the desired Distance.

## Order

A sensible order (practice): Floor with 3 ground tracks, Set Origin on the track where CG will go, Set X Axis on a track along a real line, then Set Scale with 2 tracks at a measured distance.

## Gotchas

- Floor tracks that are not exactly on the ground tilt the scene; choose tracks clearly on the ground and spread apart (practice).
- Orient first, then place CG; objects placed earlier are not re-oriented with the camera (practice).
- A wrong Distance gives wrong-size CG; measure on set if possible (practice).

## Verify

Add a cube of known size at the origin. It should sit flat on the ground, look the right size against real objects, and not slide during the shot.

## Checked

2026-10-27, Blender manual branch blender-v5.2-release; Python API docs.blender.org/api/current. Confirmed against movie_clip/tracking/clip/toolbar/solve.rst (Orientation section: Floor, Wall, Set Origin, Set X/Y Axis, Set Scale, Apply Scale, Distance in active scene units) and the Python API docs for bpy.ops.clip.set_plane, set_origin, set_axis, set_scale and apply_solution_scale (docs.blender.org/api/current, fetched on this date). Removed the XY/XZ plane wording, the metres claim, the camera-keeps-size wording for Apply Scale and the Setup Tracking Scene test-plane claim as unconfirmed.

Method: documentation only; no commands were run.
