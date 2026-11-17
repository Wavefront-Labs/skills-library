---
id: creative-arts.animation.blender.mesh-analysis-overlay
name: mesh-analysis-overlay
category: creative-arts
field: animation
product: blender
tags: [blender, mesh-analysis-overlay, overhang, thickness-analysis, mesh-analysis, 3d-printing, intersect]
level: practitioner
status: gated
description: "Inspect meshes with the Mesh Analysis overlay: overhang, thickness, intersect, distortion and sharp modes, their thresholds, and pairing it with the 3D Print Toolbox."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/meshes/mesh_analysis.html
  - https://extensions.blender.org/add-ons/print3d-toolbox/
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# mesh-analysis-overlay

Goal: find printability and quality problems visually before export.

## Enable

Edit Mode, Header → Overlays → *Mesh Analysis*. It works in Edit Mode with Solid viewport shading: areas with a high value are red, low values blue, and geometry outside the range is gray. The modes currently target 3D printing.

## Modes

| Type | Shows | Settings |
|---|---|---|
| **Overhang** | the overhang an extrusion printer must support, by angle range and axis | Minimum/Maximum angle, Axis (axis and direction used as the base for the angle) |
| **Thickness** | wall thickness by ray casting and a distance range | Minimum/Maximum thickness, Samples |
| **Intersections** | intersecting surfaces (on or off, no variance) | none |
| **Distortion** | faces that are not flat (a distorted n-gon has undefined triangulation) | Minimum/Maximum distortion |
| **Sharp Edges** | sharp edges that can form shapes too thin to print | Minimum/Maximum angle |

## Typical thresholds

Printer limits (maximum overhang angle, minimum wall thickness) depend on the printer, material and slicer; take the numbers from your printer's or slicer's documentation and enter them as the Minimum/Maximum values. Set scene units so the Thickness values are in the units you expect (practice).

## 3D Print Toolbox

The **3D Print Toolbox** ("Utilities for 3D printing") is distributed as an extension on extensions.blender.org (listing minimum Blender 4.2). Its panel contents were not checked for this review; read its listing before relying on specific checks. (gated: unconfirmed, source is paywalled or blocked)

## Gotchas

- Known limitations from the manual: currently only displayed with Deform modifiers, and performance is low while editing high-poly meshes (turn it off when not needed).

## Verify

Overhang mode on a test model highlights the down-facing areas you expect; after fixing walls, Thickness shows nothing in the range below your printer's minimum.

## Checked

2026-10-27, Blender manual, branch blender-v5.2-release (raw RST, projects.blender.org/blender/blender-manual). Confirmed against modeling/meshes/mesh_analysis.rst (modes, settings, colours, known limitations) and the extensions.blender.org listing for 3D Print Toolbox (id print3d_toolbox, tagline, minimum Blender 4.2; fetched on this date). The old 4.1 add-on manual link was replaced; toolbox panel contents are unconfirmed and gated. Removed the -Z axis default and the FDM/resin figures.

Method: documentation only; no commands were run.
