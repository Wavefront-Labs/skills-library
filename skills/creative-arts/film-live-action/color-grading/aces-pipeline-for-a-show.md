---
id: creative-arts.film-live-action.color-grading.aces-pipeline-for-a-show
name: aces-pipeline-for-a-show
category: creative-arts
field: film-live-action
product: color-grading
tags: [color-grading, colour-grading, film-live-action, colorist, colourist, aces-pipeline, aces-workflow, aces, aces-1-3, aces-2-0, acescct, acescc, acescg, ap0, ap1, idt, input-transform, odt, output-transform, rrt, reference-rendering-transform, lmt, look-modification-transform, ocio, opencolorio, color-managed-pipeline, scene-referred, display-referred, vfx-exr, linear-exr, camera-input-transforms, davinci-resolve-aces, baselight-aces, nuke-aces, academy-aces, amf, aces-metadata-file, wide-gamut, p3-d65, rec2020, deliverable-matrix, aces-version, acescct-vs-acescc, working-space, idt-selection, camera-idt, input-device-transform, lmt-use, look-modification, aces-look, aces-output, aces-hdr-output, output-device-transform, aces-exr, acescg-exchange, vfx-aces, amf-files, aces-metadata, ocio-config, aces-ocio, aces-baselight]
level: practitioner
status: draft
description: "Run an ACES pipeline across camera, VFX and grade: IDTs per camera, ACEScct working space, LMT looks, output transforms per deliverable, EXR exchange with VFX, AMF notes."
sources:
  - "https://acescentral.com/ (Academy ACES documentation and workflow guides)"
  - "https://docs.acescentral.com/ (ACES technical documentation - transforms, ACEScct, AMF)"
  - "https://www.blackmagicdesign.com/products/davinciresolve/training (The Colorist Guide to DaVinci Resolve - ACES chapter)"
  - "https://opencolorio.org/ (OpenColorIO ACES configs)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ACES pipeline for a show

**Goal:** one scene-referred working space from on-set to delivery, so a shot from an
Alexa, a RED and a drone look the same after the input transform, VFX render into it
without guessing, and SDR/HDR/DCP outputs are transforms of one grade instead of three grades.

## 1. The pieces
- **AP0 / AP1**: ACES primaries. AP0 (ACES2065-1, linear) is the archival/interchange
  space; **AP1** is the working gamut for ACEScg (linear, VFX) and **ACEScct** (log-like,
  grading - the one colourists use; ACEScc is the older variant with a harsher toe).
- **IDT / Input Transform**: camera log + gamut -> ACES. One per camera/log type
  (ARRI LogC3/LogC4 AWG3/AWG4, Sony S-Log3/S-Gamut3.Cine, RED IPP2/Log3G10 RWG,
  Blackmagic Film Gen5, Canon Log2/3 Cinema Gamut, Panasonic V-Log/V-Gamut). Stills and
  graphics use sRGB/Rec.709 IDTs. Wrong IDT = wrong colour; verify with a chart.
- **RRT + ODT = Output Transform**: ACES -> display (Rec.709 2.4, P3-D65 DCI, P3-D65
  PQ 1000 nits, Rec.2020 PQ/HLG). ACES 1.x has the "ACES look" (RRT) baked into every
  output; **ACES 2.0** (2024/25) replaces the RRT/ODT with a new output transform with
  better hue handling and less gamut clipping - choose the version per show and never mix.
- **LMT (Look Modification Transform)**: a look applied in ACES space before the output
  transform - the show LUT's proper home; the same LMT renders correctly to every output.
- **AMF (ACES Metadata File)**: XML describing the exact transforms for a clip/show;
  travels with dailies/VFX so everyone reproduces the same picture.

## 2. Decide in prep (write it in the pipeline doc)
1. ACES version (1.3 or 2.0) and working space (**ACEScct** for grade, **ACEScg** for VFX).
2. IDT per camera, and the EI/white balance policy (IDTs assume the camera's native
   white; keep shooting WB sensible, correct in ACEScct).
3. Output transforms per deliverable: e.g. `Rec.709 (2.4 gamma, 100 nit)` for dailies/
   TV, `P3-D65 ST2084 1000 nit` for HDR streaming, `P3-DCI (48 nit)` for DCP.
4. Show LMT built from the DP's look (on a test day), delivered to the dailies system
   and VFX as a LUT/CLF *within* the ACES chain (ACEScct -> ACEScct).
5. VFX exchange: **OpenEXR half-float ACEScg (AP1 linear)** plates, delivered with the
   IDT applied; comps returned in the same; any show LMT shown but not baked.
6. Monitoring: every reference display calibrated to the output transform it shows.

## 3. Software setup
- **Resolve**: `Project Settings > Color Management > Color science: DaVinci YRGB Color
  Managed > Color processing mode: ACEScct` (or legacy *ACEScct* colour science), ACES
  version, *ACES Input Transform* per clip (auto from RAW metadata; set manually per
  camera via right-click clip > ACES Input Transform or by media pool column), *ACES
  Output Transform* per project/timeline/deliverable. LMT via a node with the LUT in
  ACEScct, or a *Color Space Transform* sandwich if the LUT expects log.
- **Baselight**: DRT set to ACES; input colour space per shot; look as a Truelight
  LMT. **Nuke/Fusion/Flame**: OCIO config `aces_1.3` / `studio-config-v2 ACES 2.0`,
  working ACEScg, view transform per monitor.
- Dailies (Colorfront, Resolve, Silverstack Lab): same IDT + LMT + ODT so the editor's
  picture matches the DIT's.

## 4. Grading in ACEScct
- Primaries behave like log grading (offset/lift/gamma/gain in ACEScct feel natural;
  use Log wheels/HDR palette). Saturation and hue tools are gamut-aware in AP1 but
  highly saturated LEDs can still clip - use the *Gamut Compress* (ACES Reference Gamut
  Compression, 1.3+) as an early node for neon/stage LED footage.
- Build the grade in a node tree: `Gamut compress -> balance -> secondaries -> LMT/look`;
  the output transform happens after the tree, invisibly.
- Deliverables: switch the output transform and render; check highlights roll-off per
  output; HDR trims via Dolby Vision analysis on top.

## 5. Checks
Shoot a **colour chart and grey card** per camera on the test day; after the IDT, the
chart patches should align across cameras on the vectorscope and the grey card hit the
same value (ACEScct middle grey ≈ 0.414 / 18% linear ≈ 0.18). Compare the dailies LUT
output with the grading suite on the same clip before the shoot starts.

## Gotchas
- An IDT for the wrong log curve (LogC3 vs LogC4) - everything flat and green or crushed.
- The show LUT designed for log-to-709 inserted directly into an ACEScct node; double transform.
- VFX rendering sRGB-gamma EXRs; comps look wrong only in the grade.
- Mixed ACES versions between dailies (1.2) and finishing (2.0); the editor's reference doesn't match.
- Grading saturated stage LEDs without gamut compression; blue clips to purple.

## Verify
- [ ] Pipeline doc states ACES version, working space, IDT per camera, output transforms, LMT, EXR spec.
- [ ] Chart/grey card matched across cameras after IDT.
- [ ] Dailies, VFX viewer and grading suite show the same test clip identically.
- [ ] Each deliverable is a transform of one grade; HDR/SDR checked on reference monitors.
