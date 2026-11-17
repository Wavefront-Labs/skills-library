---
id: creative-arts.animation.blender.mask-parent-to-track
name: mask-parent-to-track
category: creative-arts
field: animation
product: blender
tags: [blender, masking, roto, mask-parent-track, mask-parenting, motion-tracking]
level: practitioner
status: docs-checked
description: "Make roto follow footage by parenting mask spline points or layers to point tracks or plane tracks in the Movie Clip Editor, then animate only the shape changes."
sources:
  - https://docs.blender.org/manual/en/latest/movie_clip/masking/editing.html
  - https://docs.blender.org/manual/en/latest/movie_clip/masking/sidebar.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# mask-parent-to-track

Goal: use tracking to move masks, so only shape changes need animating.

## Parent to a track

1. Track a feature in the Movie Clip Editor (Tracking mode).
2. Switch to Mask mode, select the mask points, and make sure the tracking marker you want is the active track.
3. **Mask > Make Parent** (Ctrl P) parents the selected spline points to the active motion tracker. **Mask > Clear Parent** (Alt P) removes the parenting for the selected points.
4. The **Active Point** panel (Mask tab) shows the parent: the Movie Clip, **Parent Type** (*Point Track* or *Plane Track*), **Object** (tracking object) and **Track** (track name). It is shown when both a tracking marker and a mask are selected.

## Plane tracks

Parent Type *Plane Track* lets points follow a plane track, which suits flat surfaces such as screens and signs (see `creative-arts.animation.blender.object-tracking-stabilization` for creating plane tracks).

## Whole layers

The manual notes that splines in a layer can be animated together, for example by parenting the whole set of splines to a single motion track, so one tracked point can drive the location of an entire mask layer.

## Workflow

1. Track features on each rigid part of the subject.
2. Parent the matching mask points to the tracks.
3. Insert shape keys only where the shape changes (see `creative-arts.animation.blender.mask-shape-keyframes`).

## Gotchas

- Parenting applies to the points selected when you run Make Parent; check each layer.
- A point parented to a track follows the track only where the track has data; make sure tracks cover the range you need.

## Verify

Play the clip with the mask overlay: the shapes follow the tracked parts without shape keys, and `Alt P` makes them stay put.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release branch: movie_clip/masking/editing, movie_clip/masking/sidebar) and the 5.2 source (properties_mask_common.py Active Point panel). Confirmed Make Parent Ctrl P, Clear Parent Alt P, Parent Type Point Track and Plane Track, the Active Point panel fields, and layer-level parenting. Removed unconfirmed claims about Ctrl-click selecting the track, the effect of parenting after keying, and perspective motion.
Method: documentation only; no commands were run.
