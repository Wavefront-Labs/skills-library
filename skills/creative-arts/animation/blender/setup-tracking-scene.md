---
id: creative-arts.animation.blender.setup-tracking-scene
name: setup-tracking-scene
category: creative-arts
field: animation
product: blender
tags: [blender, camera-tracking, setup-tracking-scene, tracking-scene, shadow-catcher, camera-solve]
level: practitioner
status: docs-checked
description: "Use Setup Tracking Scene after a Blender camera solve: what it creates (camera solver, view layers, collections, test objects, compositor group) and how to finish it."
sources:
  - https://docs.blender.org/manual/en/latest/movie_clip/tracking/clip/editing/clip.html
  - https://docs.blender.org/manual/en/latest/movie_clip/tracking/clip/toolbar/solve.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# setup-tracking-scene

Goal: go from a solved clip to a renderable integration scene in minutes.

## Run it

Movie Clip Editor, Tracking mode: **Clip > Setup Tracking Scene** (also Solve tab > Scene Setup). It is only available when the active tracking object has a valid reconstruction. Do orientation and scale first. The manual says it creates reference objects for the floor and a test cube, a camera that matches the tracked motion, and a compositor node tree combining the render with the footage; it is a convenience starting point.

In the 5.2 source it does the following:

- Sets the clip as the scene's active clip and turns on render **Motion Blur**; sets the world's ambient-occlusion distance to 1.0 (and AO factor 0.05 when Cycles is present).
- Uses the scene camera (or creates one) and gives it a **Camera Solver** constraint using the active clip; sets sensor width, horizontal sensor fit, focal length and lens shift from the tracking camera.
- Sets the clip as the viewport camera background.
- Makes view layers named **Foreground** and **Background**, and collections named **foreground** and **background**.
- Builds a compositor node group named **Tracking Setup**: Movie Clip, Movie Distortion (set to Undistort), Scale (Render Size), two Alpha Over nodes, the Background and Foreground Render Layers and a Viewer. If a compositing tree already exists it is kept with a fake user.
- If missing, adds a point light, a **Cube** in the foreground collection, and a **Ground** plane (8 by 8 units, half-size 4) in the background collection; with Cycles it marks background-collection objects as shadow catchers.

## Finish the setup

1. Match the ground plane to the real ground and check the shadow catcher flag on it.
2. Light the scene to match the plate.
3. Put CG in the foreground collection.
4. Check the Movie Distortion node and the colour space of the clip against the scene view transform.

## Gotchas

- It does not turn on Film Transparent; check the render settings yourself.
- Generated nodes may need adjusting for your pipeline, and a clip start frame different from the scene start frame offsets the CG.

## Verify

Render a few frames: CG sits on the ground with matching shadows and does not slide.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release branch: movie_clip/tracking/clip/editing/clip) and the 5.2 source (scripts/startup/bl_operators/clip.py, class CLIP_OT_setup_tracking_scene). Replaced the generic summary with what the operator does in 5.2 and removed unconfirmed claims about scene frame range and resolution matching and generic version warnings.
Method: documentation only; no commands were run.
