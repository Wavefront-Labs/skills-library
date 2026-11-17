---
id: creative-arts.animation.motion-graphics.ae-output-modules
name: ae-output-modules
category: creative-arts
field: animation
product: motion-graphics
tags: [output-modules, render-queue, after-effects, render-settings, templates, prores-4444, png-sequence, alpha-channel, post-render-action]
level: practitioner
status: draft
description: "Set up After Effects Render Queue render settings and output module templates: codecs, alpha, sequences, multiple outputs per item, and post-render actions."
sources:
  - https://helpx.adobe.com/after-effects/using/basics-rendering-exporting.html
  - https://helpx.adobe.com/after-effects/using/render-settings.html
  - https://helpx.adobe.com/after-effects/using/output-modules-output-module-settings.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Render Queue output modules

**Goal:** consistent, correct renders from AE every time, by using saved templates instead of
clicking settings per render.

## Render settings vs output module

- **Render Settings**: how frames are computed: quality (Best), resolution (Full), frame rate, time
  span, motion blur and frame blending switches, proxy use. Template "Best Settings" is the norm for
  finals; "Draft" for tests.
- **Output Module**: how frames are written: format, codec, channels (RGB, RGB+Alpha), depth,
  colour (premultiplied/straight), audio, resize/crop, post-render action.

## Useful output module templates

| Template | Settings |
|---|---|
| ProRes 422 HQ master | QuickTime, Apple ProRes 422 HQ, RGB, audio 48k 24-bit |
| ProRes 4444 alpha | QuickTime, ProRes 4444, RGB + Alpha, Straight (or Premultiplied as agreed), Trillions of colours |
| PNG sequence alpha | PNG Sequence, RGB + Alpha, Straight; file name `[compName]_[#####].png` |
| EXR for comp | OpenEXR sequence, 16-bit half (32 bpc project), RGB+Alpha |

Edit - Templates - Output Module to save and set defaults. Templates export as `.ars`/`.aom` files for
the team.

## Multiple outputs per item

Select a queued item - Composition - Add Output Module: render ProRes master and an H.264 review in
one pass. (H.264 output goes through Adobe Media Encoder in recent versions:
`creative-arts.animation.motion-graphics.media-encoder-queue`.)

## Naming

Use file name templates: `[compName]_[dateYear][dateMonth][dateDay]` or project-specific tokens.
Comp names should already carry shot/version (`SH010_titles_v003`).

## Post-render actions

Import, Import & Replace Usage (swap a heavy precomp for its render), Set Proxy. Import & Replace
Usage is a fast way to pre-render expensive nested comps.

## Gotchas

- Project bit depth (8/16/32 bpc) limits output depth; 8 bpc projects band on gradients.
- Colour management: with a project working space, output modules can convert to an output profile;
  check "Preserve RGB" vs conversion so masters are not double-converted.
- Straight vs premultiplied must match what the receiving app expects
  (`creative-arts.animation.color.premultiplied-alpha`).

## Verify

ffprobe or MediaInfo on the output shows the intended codec, alpha channel presence and frame rate;
an alpha render composited over white shows no dark fringe.
