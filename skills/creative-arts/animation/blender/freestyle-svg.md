---
id: creative-arts.animation.blender.freestyle-svg
name: freestyle-svg
category: creative-arts
field: animation
product: blender
tags: [blender, freestyle-svg, svg-export, freestyle, vector-output, npr, line-art]
level: practitioner
status: docs-checked
description: "Export Freestyle lines to SVG with the Freestyle SVG Exporter: install and enable, frame versus animation mode, fill contours, output location and editing in vector tools."
sources:
  - https://docs.blender.org/manual/en/4.1/addons/render/render_freestyle_svg.html
  - https://extensions.blender.org/add-ons/freestyle-svg-exporter/
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# freestyle-svg

Goal: vector line drawings (plans, diagrams, plotter or laser output) straight from a 3D scene.

## Enable

- Blender up to 4.1: Preferences → Add-ons → Render → *Freestyle SVG Exporter* (bundled add-on).
- Later releases: the extension *Freestyle SVG Exporter* on extensions.blender.org (it was part of the 4.1 bundled add-ons and is now offered as-is with limited support).
- The panel is Properties → Render → *Freestyle SVG Export*; activate Freestyle rendering first.

## Usage and options

Render with *Render Image*: the render shows as usual and the SVG is saved to the default output path (Properties → Output → Output).

- *Mode*: **Frame** renders a single frame; **Animation** bundles all rendered frames into a single .svg file (an SVG animation).
- *Split at Invisible*: split paths at invisible vertices (some modifiers such as Blueprint mark vertices invisible).
- *Fill Contours*: fills object contours with their material colour; the manual calls it unstable, especially for animations.
- *Stroke Cap Style*: Miter, Round or Bevel.

## What is exported

Freestyle styles points individually while SVG styles per path, so only some properties carry over (with no modifiers applied): base colour, base alpha, base thickness and dashes. Extra options are in View Layer Properties → *Freestyle Line Style SVG Export*.

Fills come from the Contour and External Contour edge types plus predicates; layering and ordering are imperfect and are usually fixed in Inkscape or a text editor.

## Verify

Open the SVG in a vector editor or browser and compare it with the raster render.

## Checked

2026-10-27 against the Blender 4.1 manual page for the add-on (the last manual release that documents it) and the extensions.blender.org listing. Confirmed activation path, panel location, Mode, Split at Invisible, Fill Contours, Stroke Cap Style and the exportable properties. Removed unconfirmed claims about file naming, thickness modifier approximation, units and path-count advice.
Method: documentation only; no commands were run.
