---
id: creative-arts.film-live-action.premiere-pro.lumetri-color-grading
name: lumetri-color-grading
category: creative-arts
field: film-live-action
product: premiere-pro
tags: [premiere-pro, premiere, adobe-premiere-pro, film-live-action, lumetri, lumetri-color, lumetri-colour, lumetri-scopes, color-correction, colour-correction, basic-correction, input-lut, creative-lut, look, curves, rgb-curves, hue-saturation-curves, color-wheels, colour-wheels, hsl-secondary, vignette, auto-tone, color-match, comparison-view, shot-match, log-footage, rec709, color-management, colour-management, auto-detect-log, display-color-management, hdr-in-premiere, adjustment-layer, lumetri-presets, waveform, vectorscope, parade, broadcast-safe, video-limiter, basic-correction-use, input-lut-use, lumetri-creative, lumetri-curves, lumetri-wheels, hsl-secondary-use, lumetri-secondary, lumetri-scopes-use, premiere-legal-levels, premiere-color-management, premiere-log, color-match-use, comparison-view-use, premiere-hdr, lumetri-preset-save, look-export, cube-export]
level: practitioner
status: draft
description: "Grade in Premiere Pro's Lumetri Color: colour management for log, Basic Correction with scopes, Curves and HSL Secondary, Color Match comparison view, looks on adjustment layers, video limiter."
sources:
  - "https://helpx.adobe.com/premiere-pro/using/color-workflows.html (Adobe - Color workflows and Lumetri Color panel)"
  - "https://helpx.adobe.com/premiere-pro/using/color-management.html (Adobe - Color management in Premiere Pro)"
  - "https://certifiedprofessional.adobe.com/ (Adobe Certified Professional - Premiere Pro exam objectives, Domain 4)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lumetri Color grading in Premiere Pro

**Goal:** balanced, matched, legal pictures across an edit without leaving the NLE -
good enough for broadcast and web delivery, structured so a Resolve conform can take
over if the show grows.

## 1. Set up colour management first
`Sequence > Sequence Settings > Color Management` (Premiere 2024+ / 25.x): choose
*Working Color Space* (Rec.709 for SDR, Rec.2100 PQ/HLG for HDR) and enable
**Auto Detect Log Video Color Space** / per-clip *Modify > Interpret Footage > Color
Management > Media Color Space* so log clips (S-Log3, LogC, V-Log, BRAW metadata)
are transformed to the working space automatically - no input LUT needed. Older
workflow: *Basic Correction > Input LUT* with the manufacturer's log-to-709 LUT per
clip (`Browse` and keep LUTs in a project folder). Enable `Preferences > Color >
Display Color Management` so the Program Monitor matches a calibrated display.
Open **Lumetri Scopes** (`Window`): Waveform (Luma/RGB), Parade, Vectorscope HLS/YUV,
Histogram; set the clamp to the working space and 8-bit/float as needed.

## 2. Basic Correction (the primary)
Select the clip (or an adjustment layer), `Window > Lumetri Color`:
- *White Balance*: eyedropper on a neutral, then Temperature/Tint by eye on the
  vectorscope centre.
- *Tone*: **Exposure** (overall; watch the waveform top), **Contrast**, **Highlights**,
  **Shadows**, **Whites**, **Blacks** (set black point ~0-3 IRE, white ≤100 IRE on
  the waveform), **Saturation**. *Auto* for a starting point only.
- Order per clip: exposure, contrast, white balance, then saturation.
- *Reset Effect* or disable with the `fx` toggle to compare; `Ctrl/Cmd+Shift+C`...
  rather use the panel's eyeball.
Lumetri is one effect instance per application; add a **second Lumetri** (Effects >
Lumetri Color drag) for the look so the correction stays separate - name them in
Effect Controls (click the name to rename).

## 3. Creative, Curves and Wheels
- **Creative**: *Look* dropdown (LUTs; load `.cube` via Browse), *Intensity*, Faded Film,
  Sharpen, Vibrance, Shadow/Highlight tint wheels.
- **Curves**: RGB curves (master and per channel; `Ctrl/Cmd`-click to delete a point);
  **Hue vs Sat / Hue vs Hue / Hue vs Luma / Luma vs Sat / Sat vs Sat** - eyedropper on
  the image to drop control points; pull a distracting red or lift skin.
- **Color Wheels & Match**: Shadows/Midtones/Highlights wheels + luma sliders (lift/
  gamma/gain style); **Comparison View** (button at bottom of Program Monitor) shows a
  reference shot vs current (side by side / vertical / horizontal split); **Apply Match**
  (with *Face Detection* on) auto-matches, then refine. Use the reference frame for
  every shot in the scene.
- **HSL Secondary**: Key with the eyedropper (+/−), refine H/S/L ranges, *Show Mask* to
  check, denoise/blur the mask, then correct with its own wheel/temp/contrast - for
  skin, sky, a product colour.
- **Vignette**: amount, midpoint, roundness, feather.

## 4. Workflow for a scene
1. Correct the hero shot of the scene; copy its Lumetri (`Ctrl/Cmd+C`, select other
   clips, `Ctrl/Cmd+Alt+V` *Paste Attributes* > Lumetri only).
2. Comparison View against the hero for each remaining shot; adjust Basic Correction only.
3. Apply the look on an **adjustment layer** over the scene (one Lumetri with the
   Creative/Curves work); trim the adjustment layer to the scene.
4. Keyframe Lumetri parameters in Effect Controls for changes within a shot (a window
   blowing out) - sparingly.
5. Save **Lumetri presets** (panel menu > Save Preset) for recurring looks/cameras.

## 5. Legal and delivery
Add **Video Limiter** (Effects > Color Correction) on a top adjustment layer at the end:
*Clip Level* (e.g. 100 IRE / -0 to 103 for broadcast per spec), *Compress*: Highlights/
Shadows, *Chroma* limiting. Check the waveform with `Clamp Signal` off to see excursions.
Export LUTs from Lumetri (panel menu > *Export .cube*) to hand a look to a colourist; for
a full Resolve grade, export the XML without Lumetri (or note it) - Lumetri doesn't translate.

## 6. HDR in Premiere
Rec.2100 PQ/HLG sequence, *Maximum Luminance* setting in Lumetri (HDR Graphics White),
scopes in nits, export HEVC/ProRes with HDR metadata. Only with a real HDR monitor;
otherwise finish SDR here and HDR in Resolve.

## Gotchas
- Input LUT applied on top of auto colour management; the image is double-transformed and flat or crushed.
- Grading on an uncalibrated laptop screen in a bright room.
- One Lumetri doing correction and look; copying it to other shots copies the look twice.
- HSL Secondary key without `Show Mask`; the correction bleeds into the wall.
- Forgetting the limiter; whites at 109 IRE fail broadcast QC.

## Verify
- [ ] Colour management or input LUT set once per camera/log type, not both.
- [ ] Each clip: corrected Lumetri (named), look on an adjustment layer per scene.
- [ ] Every shot compared to the scene's hero in Comparison View; skin on the vectorscope line.
- [ ] Video Limiter on top; waveform within delivery spec; LUT exported for the colourist if needed.
