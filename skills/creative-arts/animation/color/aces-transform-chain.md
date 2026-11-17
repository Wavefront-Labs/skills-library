---
id: creative-arts.animation.color.aces-transform-chain
name: aces-transform-chain
category: creative-arts
field: animation
product: color
tags: [aces-transforms, aces, idt, rrt, odt, lmt, output-transform, input-transform, aces2065-1, acescct, colour-management]
level: advanced
status: draft
description: "Understand and apply the ACES chain for animation: input transforms, LMTs, RRT/ODT (ACES 1.x) or the unified ACES 2 output transform, and where each sits."
sources:
  - https://docs.acescentral.com/
  - https://opencolorio.readthedocs.io/en/latest/configurations/aces_studio.html
  - https://github.com/ampas/aces-dev
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# The ACES transform chain

**Goal:** know which transform does what so a frame goes from source to screen exactly once through each stage.

## The chain

```
source image --(Input Transform / IDT)--> ACES2065-1 (AP0 linear, archive/interchange)
      working: ACEScg (AP1 linear, render/comp)  |  ACEScct (AP1 log, grading)
      --(LMT: optional creative look, scene-referred)-->
      --(RRT + ODT in ACES 1.x  |  single Output Transform in ACES 2.0)--> display (sRGB, Rec.709, P3-D65, Rec.2100 PQ)
```

- **Input Transform (IDT):** camera-specific or file-specific conversion into ACES. For CG, renders are already
  ACEScg so the "input" is just ACEScg to AP0; textures use an sRGB-texture input (Utility - sRGB - Texture).
- **LMT (Look Modification Transform):** a scene-referred look (e.g. a show desaturation) applied before output.
- **RRT (Reference Rendering Transform) + ODT (Output Device Transform):** ACES 1.x tone-maps scene values to a
  standard output, then encodes for the display. In OCIO these appear as views like *ACES 1.0 - SDR Video*.
- **ACES 2.0** (2024/25) replaces RRT+ODT with one output transform family with better hue preservation and
  highlight handling. Do not mix ACES 1.x and 2.0 views in one show.

## Rules

1. Exactly one input transform per source, exactly one output transform per display. Double application (an sRGB
   texture tagged ACEScg, then a view transform) is the most common error.
2. Grade in ACEScct, render and composite in ACEScg, archive in ACES2065-1 EXR
   (see `creative-arts.animation.encode-delivery.archival-master-formats`).
3. The output transform belongs to the **viewer**, not the pixels, until the final display-referred deliverable is
   baked.

## Stylized animation note

Cel and flat-shaded looks often fight the ACES tone curve (saturated brand colours desaturate and shift).
Options: a stylized LMT, a show-specific view, or a display-referred pipeline for 2D elements. Decide this in look
development (`creative-arts.animation.color.look-development-for-color-pipelines`), not at grading.

## Verify

Render a colour chart (Macbeth-like patches as ACEScg values) and view through the show view: patch values measured
on the display output match the reference values for the chosen ACES version within a small tolerance.
