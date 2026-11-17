---
id: creative-arts.animation.blender.collection-exclude-view-layer
name: collection-exclude-view-layer
category: creative-arts
field: animation
product: blender
tags: [blender, view-layer, collection-exclude-layer, per-layer-visibility, holdout-collection, outliner]
level: practitioner
status: docs-checked
description: "Control what each view layer renders: Include/Exclude, Holdout and Indirect Only per layer, and why Disable in Renders (camera icon) affects every view layer."
sources:
  - https://docs.blender.org/manual/en/latest/editors/outliner/interface.html
  - https://docs.blender.org/manual/en/latest/scene_layout/collections/collections.html
  - https://docs.blender.org/manual/en/latest/editors/outliner/editing.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# collection-exclude-view-layer

Goal: separate characters, background and FX into view layers that composite back together cleanly.

## Per view layer settings

Found in the Outliner (restriction toggles, enabled from the filter popover) and in the Collection Properties tab, View Layer panel (Include, Holdout, Indirect Only). They apply to the active view layer only.

- **Exclude from View Layer** (checkbox; *Include* in the Properties tab): the collection's contents are hidden in the 3D Viewport, the render and the Outliner for this view layer. Outliner context menu: *View Layer > Disable from View Layer* / *Enable in View Layer*.
- **Holdout:** objects in the collection cut a fully transparent hole into the render output of the view layer. Outliner context menu: *Set Holdout* / *Clear Holdout*.
- **Indirect Only** (Cycles only): objects do not appear directly in the image but still contribute through shadows and reflections (lighting, as the Properties tab describes it). Context menu: *Set Indirect Only* / *Clear Indirect Only*.
- **Hide in Viewports** (eye): viewport only, current view layer; the render is not affected.

## Settings that are not per view layer (the trap)

- **Disable in Renders** (camera icon) and **Disable in Viewports** (screen icon) are set on the collection itself and apply to **all** view layers. Turning off the camera icon to hide a collection from one layer hides it from every layer; use Exclude or Holdout per layer instead.
- **Disable Selection** is also a property of the collection or object, not of the view layer.

## Layer split idea

A common split is one view layer per element (for example background, characters, FX). In each layer, exclude what should not appear, use Holdout where another element must cut a matte, and Indirect Only where an element should only shade the others. Composite the layers afterwards.

## Gotchas

- An excluded collection is gone for that layer, so it casts no shadow and contributes no reflections; use Indirect Only when you need the light interaction without the object.
- Holdout produces a hard transparent cut-out; check the edges in the composite.
- Hidden-in-viewport objects still render and are still evaluated; only Disable in Viewports removes them from the view layer and from evaluation.

## Verify

Render each layer, combine them in the compositor and compare against a single-layer render of everything.

## Checked

Date: 2026-10-27. Documentation: Blender manual 5.3 (editors/outliner/interface.rst, editors/outliner/editing.rst, scene_layout/collections/collections.rst).
Confirmed: toggle names, scopes (per view layer vs all view layers), Holdout and Indirect Only semantics, Cycles-only note, Properties tab panel names, context menu entries. Removed unconfirmed claims: the layer-split table, "Ray Visibility is global per object", and motion blur and depth of field behaviour on holdouts.
Method: documentation only; no commands were run.
