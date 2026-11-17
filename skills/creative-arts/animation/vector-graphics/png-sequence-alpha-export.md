---
id: creative-arts.animation.vector-graphics.png-sequence-alpha-export
name: png-sequence-alpha-export
category: creative-arts
field: animation
product: vector-graphics
tags: [png-sequence, vector-export, svg-export, alpha-export, adobe-animate, toon-boom, transparent-background, straight-alpha, frame-padding]
level: practitioner
status: draft
description: "Export 2D vector animation as PNG sequences with alpha from Animate, Harmony or Inkscape for compositing: transparency, padding, resolution, colour and naming."
sources:
  - https://helpx.adobe.com/animate/using/export-graphics-videos.html
  - https://docs.toonboom.com/
  - https://inkscape.org/doc/inkscape-man.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PNG sequence export with alpha

**Goal:** frame-accurate, transparent renders of 2D animation layers (characters, effects) that composite
cleanly in AE, Nuke, Resolve or Blender.

## Per app

- **Adobe Animate**: File - Export - Export Movie - PNG Sequence; set size (render at final resolution, or 2x
  for downscaling), background transparent (uncheck "Include background" / set stage alpha), smoothing on.
  For per-layer passes, hide other layers or use guide layers.
- **Toon Boom Harmony**: Write node per pass with drawing type PNG4 (RGBA), path and leading zeros set;
  render via Render - Render Write Nodes or batch (`creative-arts.animation.scripting.harmony-batch-render`).
- **Inkscape** (frames as separate SVGs or layers): command-line export per frame
  (`creative-arts.animation.vector-graphics.inkscape-cli-batch-export`).

## Settings

| Setting | Value |
|---|---|
| Naming | `char_mia_v003.0001.png` (padded, start number agreed: 1 or 1001) |
| Frame range | the shot's cut range plus handles |
| Resolution | delivery resolution (or 2x for crisp downscale) |
| Alpha | RGBA, straight (PNG spec) |
| Colour | sRGB; note if the comp is linear (the comp applies the transform) |

## Comp side

PNG alpha is straight; most comp apps interpret it correctly on import. If dark/bright fringes appear, check
the alpha interpretation (`creative-arts.animation.color.premultiplied-alpha`).

## Gotchas

- Anti-aliased line edges against a transparent background pick up fringe colour from the stage background in
  some exporters; set the stage/background colour close to the line colour or to black and test.
- Animate exports "on twos" animation as duplicated frames, which is correct for frame-accurate comps; keep them.
- Huge sequences: use folders per pass, not one folder per episode.

## Verify

Import into the comp app over white and black: no fringes, frame count equals the shot range, and frame 1 aligns
with the shot's first frame in the edit.
