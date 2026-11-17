---
id: creative-arts.film-live-action.premiere-pro.opacity-blend-modes-and-compositing
name: opacity-blend-modes-and-compositing
category: creative-arts
field: film-live-action
product: premiere-pro
tags: [premiere-pro, film-live-action, blend-mode-use, opacity-keyframes, compositing-premiere, blend-modes, opacity, track-matte-key, alpha-channel, luma-matte, screen-blend, multiply-blend, overlay, light-leaks, picture-in-picture]
level: practitioner
status: draft
description: "Composite in Premiere Pro: opacity keyframes, blend modes for overlays and light leaks, Track Matte Key with alpha or luma mattes, and alpha interpretation of graphics."
sources:
  - "https://helpx.adobe.com/premiere-pro/using/compositing-alpha-channels-adjusting-clip.html (Adobe - Compositing, alpha channels and opacity)"
  - "https://helpx.adobe.com/premiere-pro/using/blend-modes.html (Adobe - Blend modes in Premiere Pro)"
  - "https://helpx.adobe.com/premiere-pro/using/masking-tracking.html (Adobe - Masking and tracking)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Opacity, blend modes and compositing in Premiere Pro

**Goal:** layered shots (overlays, picture-in-picture, matte reveals, texture passes)
done in Premiere without a trip to After Effects, and rendering the same on export.

## 1. Opacity and its keyframes
- Every clip has *Effect Controls > Opacity*: the value, **Blend Mode**, and the
  mask buttons.
- Fade a layer: keyframe Opacity (stopwatch on), or on the timeline enlarge the track,
  *Show Clip Keyframes > Opacity*, and Ctrl/Cmd-click the rubber band to add points.
- For eased fades right-click the keyframe > *Ease In/Ease Out*; linear opacity fades
  read as a dip.
- A cross dissolve between two clips on one track is simpler than stacked opacity ramps.

## 2. Blend modes that get used
| Mode | Use |
|---|---|
| Screen / Linear Dodge (Add) | Light leaks, flares, fire, sparks shot on black - black drops out |
| Multiply | Paper/grunge textures, shadows, ink on white - white drops out |
| Overlay / Soft Light | Contrast textures, film-burn tints, grain plates on mid-grey |
| Difference | Alignment check: two identical frames go black when lined up |
| Color / Luminosity | Apply a tint plate's colour only, or a layer's luminance only |
Set mode on the **upper** layer; it combines with everything beneath. Lower opacity to
taste after choosing the mode.

## 3. Mattes
- **Track Matte Key** (Effects > Keying): put it on the fill clip, choose the matte
  track, *Composite Using* Matte Alpha (graphic with transparency) or Matte Luma
  (white = visible). Reverse inverts.
- Text reveals: title on the track above the footage, Track Matte Key on the footage
  pointing at the title track.
- Masks on Opacity (ellipse/pen) with tracking for blurs, spotlights, sky swaps.

## 4. Alpha channel handling
- ProRes 4444, PNG and PSD layers carry alpha. If edges show a dark/light fringe,
  *Modify > Interpret Footage > Alpha Channel* and toggle *Premultiplied* / *Ignore*.
- H.264 has no alpha; graphics delivered as H.264 on black need Screen blend instead.

## Gotchas
- Blend modes on an adjustment layer affect every track below it, including titles.
- Nested sequences flatten blend modes inside; apply the mode on the nest itself.
- Some blend results differ between preview render and export if the GPU path differs;
  scrub the export.
- Screen on footage that isn't true black leaves a haze; crush the overlay's blacks first.

## Verify
- [ ] Each overlay's mode chosen on purpose; no stray haze or fringe.
- [ ] Opacity fades eased; keyframes visible on the timeline.
- [ ] Mattes track the intended layer after re-ordering tracks.
- [ ] Exported frames match the Program monitor.
