---
id: creative-arts.animation.blender.color-management-curves
name: color-management-curves
category: creative-arts
field: animation
product: blender
tags: [blender, color-management, curves-view, color-management-curves, rgb-curves]
level: practitioner
status: docs-checked
description: "Use Color Management > Use Curves for a global display curve: what it changes, where it is applied, and why the compositor is usually a better place for curves."
sources:
  - https://docs.blender.org/manual/en/latest/render/color_management/displays_views.html
  - https://docs.blender.org/api/current/bpy.types.ColorManagedViewSettings.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# color-management-curves

Goal: understand and use the global curve in Color Management.

## Render Properties > Color Management > Curves

Per the manual, **Curves** adjusts RGB curves to control the image colours **before the colour space conversion** (the same stage as Exposure and Look; Gamma is applied after).

Where the curve applies:
- The Render Result and Viewer images, and files saved directly by Render Animation.
- Other image data-blocks only with **View as Render**, and saved files only with **Save as Render**; both apply the view, exposure, gamma and RGB curves.

## When it is useful

- A quick show-wide contrast tweak in a single-scene project.
- Matching a look on a still without building a compositor graph.

## Why the compositor is often better

- Compositor curves are visible in the node tree and can be masked or applied per pass.
- The Color Management curve lives in a panel and is easy to forget, so settings can differ between scenes or files.
- External grading needs a clean, ungraded output.

## Python

`scene.view_settings.use_curve_mapping = True`; the curve is `scene.view_settings.curve_mapping` (Python API ColorManagedViewSettings).

## Verify

Toggle Curves while viewing a render in the Image Editor; the change should be visible, and a file saved with Save as Render should match.

## Checked
2026-10-27, Blender 5.2 manual (blender-v5.2-release RST) render/color_management/displays_views (Curves: adjusts RGB curves before the colour space conversion; View as Render and Save as Render apply curves) and Python API ColorManagedViewSettings (use_curve_mapping, curve_mapping). Fixed the claim that the curve acts on display-referred values after the view transform; removed unconfirmed multi-scene and workflow claims.
Method: documentation only; no commands were run.
