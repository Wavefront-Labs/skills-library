---
id: creative-arts.animation.color.ocio-looks-per-shot
name: ocio-looks-per-shot
category: creative-arts
field: animation
product: color
tags: [ocio-looks, ocio, cdl, asc-cdl, per-shot-grade, looks, context-variables, colour-management, lighting-preview]
level: advanced
status: draft
description: "Use OCIO looks with ASC CDLs and context variables so lighters and compositors preview each shot's grade in their viewer, driven by a per-shot file."
sources:
  - https://opencolorio.readthedocs.io/en/latest/guides/authoring/looks.html
  - https://opencolorio.readthedocs.io/en/latest/guides/authoring/contexts.html
  - https://theasc.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# OCIO looks for per-shot grades

**Goal:** artists see the colourist's (or lead lighter's) per-shot grade while they work, without baking it into
renders.

## Mechanism

A **look** is a named transform applied in a process space before the view transform. Combined with a **context
variable** in a file path, one look definition resolves to a different CDL per shot:

```yaml
environment:
  SHOT: default
search_path: "luts:grades"
looks:
  - !<Look>
    name: shot_grade
    process_space: ACEScct
    transform: !<FileTransform> {src: "grades/${SHOT}.cdl", interpolation: linear}
  - !<Look>
    name: show_look
    process_space: ACEScct
    transform: !<FileTransform> {src: show_look_v003.cube, interpolation: tetrahedral}
displays:
  sRGB - Display:
    - !<View> {name: Shot Graded, view_transform: ACES 1.0 - SDR Video, display_colorspace: sRGB - Display, looks: "+show_look, +shot_grade"}
```

Set `SHOT=sq020_sh0040` in the environment when launching the DCC (launcher or Ayon environment, see
`creative-arts.animation.pipeline.ayon-launcher-environments`); a `grades/default.cdl` identity file keeps shots
without a grade valid.

## CDL files

ASC CDL is 10 numbers: slope (R,G,B), offset (R,G,B), power (R,G,B), saturation. `.cdl`/`.cc` XML:

```xml
<ColorCorrection id="sq020_sh0040">
  <SOPNode><Slope>1.02 1.00 0.97</Slope><Offset>0.01 0.00 -0.005</Offset><Power>1.0 1.0 1.0</Power></SOPNode>
  <SatNode><Saturation>0.95</Saturation></SatNode>
</ColorCorrection>
```

Resolve exports CDLs per clip (timeline > Export > EDL with CDL, or right-click a clip > Export LUT/CDL). Only
primary corrections fit in a CDL; windows and qualifiers do not.

## Verify

Launch the compositor with two different `SHOT` values: the *Shot Graded* view changes accordingly, the render
written to disk is identical in both cases, and the preview matches the colourist's Resolve output within a small
tolerance.
