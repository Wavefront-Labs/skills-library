---
id: creative-arts.film-live-action.davinci-resolve.primary-correction-wheels-bars-and-curves
name: primary-correction-wheels-bars-and-curves
category: creative-arts
field: film-live-action
product: davinci-resolve
tags: [davinci-resolve, resolve, film-live-action, colorist, colourist, color-page, primary-correction, primaries, lift-gamma-gain, lift, gamma, gain, offset, color-wheels, colour-wheels, primaries-bars, log-wheels, shadows-midtones-highlights, log-grading, contrast-pivot, saturation, hue, temperature-tint, midtone-detail, colour-boost, color-boost, curves, custom-curves, hue-vs-hue, hue-vs-sat, lum-vs-sat, sat-vs-sat, waveform, parade, vectorscope, histogram, auto-balance, picker, balancing, exposure-correction, white-balance-fix, primary-grade, normalise, normalize]
level: practitioner
status: draft
description: "Do the primary grade in Resolve: balance with wheels, bars and log wheels, offset/contrast/pivot/saturation and temperature/tint, read the scopes as you go, finish with curves, in a colourist's order."
sources:
  - "https://www.blackmagicdesign.com/products/davinciresolve/training (The Colorist Guide to DaVinci Resolve - Primary corrections chapters)"
  - "https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_Reference_Manual.pdf (Color page - Primaries palette, Curves)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Primary correction: wheels, bars and curves

**Goal:** a neutral, correctly exposed, technically sound image on the first node of
every shot - the base that every look and every match sits on. Primaries are
"everything in the frame"; secondaries come later.

## 1. Read before you touch
Open the **Scopes** (`Workspace > Video Scopes`) - Parade (RGB balance per tonal
range), Waveform (exposure, clipping), Vectorscope (hue/saturation; skin on the
indicator line), Histogram. Set the scope to the timeline colour space; for log-managed
projects judge on the *output* (post colour management) not the raw log signal.
Decide what's wrong in order: exposure, contrast, colour balance, saturation.

## 2. The Primaries palette, in order
**Primaries Wheels** (log footage? consider the Log palette first - see 3):
1. **Offset** (master wheel + dial): moves the whole signal - the "exposure" of the grade.
   Use it for global exposure and overall colour cast before touching lift/gamma/gain.
2. **Lift** (shadows): set black level with the master dial; neutralise shadow cast by
   dragging the wheel toward the opposite colour until the bottom of the Parade aligns.
3. **Gain** (highlights): set white level; neutralise highlights until the top of the
   Parade aligns.
4. **Gamma** (midtones): overall brightness feel; skin tone balance.
5. **Contrast / Pivot**: stretch around the pivot (set pivot to the tone you want fixed -
   middle grey ~0.435 in Rec.709 2.4, lower for log). More precise than lift+gain for S-curves.
6. **Saturation** (overall), **Hue** (rotate), **Lum Mix**, **Color Boost** (saturation
   of low-saturation areas only - subtle, for skin), **Midtone Detail** (local contrast;
   negative values soften), **Shadows/Highlights** (recover roll-offs).
7. **Temperature / Tint** dials: a white-balance fix that behaves like camera WB.
Shift-drag a wheel for fine adjustment; double-click the wheel to reset; `Alt`-drag
master dials for luma only in YRGB mode.

**Primaries Bars**: the same controls as RGB sliders per range - precise when fixing a
single channel (a magenta shadow = pull red and blue lift down).

## 3. Log wheels (Shadows / Midtones / Highlights)
Toggle to **Log** in the palette (or `Alt+Z`). The ranges are tonal bands with
adjustable **Low/High Range** and **Low/High Softness**; adjustments are more
"zoned" and film-like than LGG (which overlap across the whole range). Ideal for
colour-managed log pipelines (DaVinci Wide Gamut/Intermediate): offset for exposure,
log wheels for shadow/highlight colour, then contrast/pivot. Many colourists do the
primary in Log and reserve LGG for finesse.

## 4. Auto and pickers
**Auto Balance** (`A` icon in the Primaries) does a reasonable neutralisation on normal
footage - a starting point, never the end. The **white/black pickers** under the wheels
neutralise from a sampled area (grey card, white wall). Use them for a fast match of
a series of shots, then refine.

## 5. Curves
- **Custom curves** (YRGB): an S-curve for contrast with precise pivot points; drag the
  individual R/G/B curves for channel-specific balance (unlink *Y* to avoid luma shifts);
  *Soft Clip* in the curve palette for gentle roll-off instead of clipping.
- **Hue vs Hue** (shift one hue - fix a magenta skin tilt), **Hue vs Sat** (desaturate a
  distracting colour), **Lum vs Sat** (desaturate shadows/highlights for a film look),
  **Sat vs Sat** (reduce only high saturation), **Sat vs Lum**, **Hue vs Lum**.
  Pick the colour with the eyedropper to drop control points; keep ranges soft.
Curves are powerful and easy to overdo - watch the vectorscope.

## 6. Discipline
- Primaries on node 1 ("balance"), look on later nodes; label nodes.
- Keep the white point legal: in a Rec.709 output, white ≤ 100 IRE / 1023, black ≥ 0.
  Use Soft Clip or the *Highlight* recovery rather than clipping.
- Compare with the previous shot (`Wipe` and *Image Wipe*, stills in the Gallery) as
  you balance - a correct image that doesn't match its neighbour is wrong.
- Copy a primary grade to the next shot of the same setup with the middle mouse button
  (or `Alt+Shift+C` / append), then adjust offset only.

## Gotchas
- Fixing exposure with Gamma; the image looks washed - use Offset or Contrast/Pivot.
- Lift pulled down past black, crushing shadow detail that the editor needed.
- Saturation up on everything; skin turns orange - use Color Boost or Sat vs Sat instead.
- Scopes reading the log signal while judging a Rec.709 monitor.
- Correcting a shot in isolation and not against the scene.

## Verify
- [ ] Parade balanced (R=G=B in neutrals) top and bottom; no unintended clipping on the waveform.
- [ ] Skin on or near the vectorscope skin line; saturation moderate.
- [ ] Contrast set with pivot at the chosen grey; black/white levels legal for the output.
- [ ] Node 1 labelled "balance"; matches neighbours in a wipe.
