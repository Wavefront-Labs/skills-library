---
id: creative-arts.film-live-action.davinci-resolve.hdr-grading-and-dolby-vision-delivery
name: hdr-grading-and-dolby-vision-delivery
category: creative-arts
field: film-live-action
product: davinci-resolve
tags: [davinci-resolve, resolve, film-live-action, colorist, colourist, hdr-grading, hdr, hdr10, hdr10-plus, dolby-vision, pq, st-2084, hlg, rec2020, bt2020, p3-d65, p3-pq, nits, 1000-nits, 4000-nits, maxcll, maxfall, hdr-palette, hdr-wheels, hdr-color-wheels, zones, tone-mapping, dolby-vision-analysis, dolby-vision-trim, trims, l1-l2, cmu, content-mapping-unit, xml-metadata, hdr-monitor, reference-monitor, x300, sony-bvm-hx310, scopes-hdr, waveform-nits, sdr-derivative, sdr-trim, rrt, aces-hdr, hdr-deliverables, imf-hdr, netflix-hdr, dolby-vision-license, hdr-monitoring-setup, hdr-reference-monitor, hdr-viewing, dolby-vision-trims, trim-pass, dolby-analysis, hdr10-metadata, maxcll-maxfall, static-metadata, sdr-derivative-workflow, sdr-from-hdr, hdr-to-sdr, hdr-highlights, specular-management, highlight-roll-off, hdr-palette-use, hdr-zones, hdr-wheels-use]
level: practitioner
status: draft
description: "Grade and deliver HDR in Resolve: colour-managed PQ/HLG setup, HDR palette zones, nits on the scopes, Dolby Vision analysis and SDR trims, HDR10 MaxCLL/MaxFALL, and monitoring requirements."
sources:
  - "https://www.blackmagicdesign.com/products/davinciresolve/training (The Colorist Guide to DaVinci Resolve - HDR grading and Dolby Vision chapters)"
  - "https://professional.dolby.com/content-creation/dolby-vision-for-content-creators/ (Dolby Vision workflow guides)"
  - "https://partnerhelp.netflixstudios.com/ (Netflix HDR and Dolby Vision delivery specifications)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HDR grading and Dolby Vision delivery

**Goal:** an HDR master that uses the extra range where the story benefits, holds
legal peak levels, and produces an SDR version that still looks like the same film -
with the metadata the platforms demand.

## 1. What HDR actually changes
- **PQ (ST 2084)**: absolute brightness; a code value = a nit level. Mastering at **1000
  nits** (most streaming) or 4000 (Dolby theatrical/premium) in **P3-D65** gamut inside
  a **Rec.2020** container. Diffuse white sits around 100-200 nits (not 1000); speculars,
  flames and skies use the headroom. HDR is mostly about **contrast and highlights**, not
  overall brightness - a bright flat grade is the beginner's HDR.
- **HLG**: relative, broadcast-friendly (BBC/NHK), backward-compatible-ish with SDR
  displays; mastered at 1000 nits reference.
- **HDR10**: PQ + static metadata (MaxCLL/MaxFALL, mastering display). **HDR10+**
  and **Dolby Vision**: dynamic per-shot metadata that tells consumer TVs how to
  tone-map; Dolby Vision also carries **trims** for SDR/100-nit and 600-nit targets.

## 2. Project setup
`Project Settings > Color Management`: *Color science: DaVinci YRGB Color Managed*,
**Color processing mode: DaVinci Wide Gamut / Intermediate** (or ACEScct), **Output
color space: Rec.2020 ST2084 1000 nits** (or P3-D65 ST2084 1000 nits; the container is
set at delivery) with *Output DRT: DaVinci* (or *None* for a pure pipeline). For HLG:
*Rec.2100 HLG*. For an SDR trim in the same project, use **Dolby Vision** (needs the
licensed CMU/analysis, free in Studio since v17) or an output-space switch per
deliverable. Timeline working space must be wide and log-like so the grade survives.

## 3. Monitoring and scopes
- A true **HDR reference monitor** (Sony BVM-HX310, Flanders XM/DM series, Canon
  DP-V2411) at the mastering nits, via Decklink/UltraStudio 12G SDI with the output set
  to PQ/Rec.2020; `Project Settings > Master Settings > Video Monitoring` with
  *Enable HDR metadata over HDMI* only for consumer-ish displays. Grade in a dim room
  (5 nits surround).
- Scopes: *Video Scopes > Waveform* with **HDR (ST2084) scale** showing nits; set
  **Scope > Settings > Display scale: HDR (ST.2084)**. Diffuse white ~100-203 nits, faces
  40-100 nits typical, speculars to 1000. Keep the integrated picture at a sane APL - a
  10,000-nit sun across the screen is painful.
- Check the SDR derivative on an SDR monitor side by side.

## 4. Grading tools
- **HDR palette** (Color page, "HDR" tab; replaces log wheels in HDR): zones **Black,
  Dark, Shadow, Light, Highlight, Specular** with adjustable ranges; **Global** offset/
  exposure; *Tone* and *Pivot* controls per zone. Expand speculars without touching
  diffuse white; roll off the top with the *Highlight/Specular* falloff.
- Primaries work as in SDR but reference **nits**, not IRE; *Soft Clip* at 1000 nits in
  the Curves palette; `Color > HDR tone mapping` in DaVinci DRT handles the SDR roll-off.
- Grade for the story first in HDR, then evaluate the SDR; two grades is worse than one
  grade with trims.

## 5. Dolby Vision
1. Enable `Project Settings > Color Management > Dolby Vision` (choose mastering
   display 1000/4000 nits, version 4.0 metadata, CM analysis in Resolve or external CMU).
2. **Analyse** every shot (Color page > Dolby Vision palette > *Analyze All* / *Analyze
   Selected*; shots re-analysed when the grade changes) - this generates **L1** metadata
   (min/mid/max per shot).
3. Set the **target display** in the palette (100-nit SDR, 600-nit) and view the mapped
   result; adjust **L2/L8 trims** (lift/gamma/gain/saturation/chroma weight/tone
   detail) per shot where the automatic map fails - typically bright skies and
   saturated highlights. Trims are per target; 100-nit is mandatory, 600 often
   requested, 1000 for HDR10 derivation.
4. Deliver page: render the **PQ master** (ProRes 4444 XQ / DPX / EXR or IMF) and
   export the **Dolby Vision XML** (`Dolby Vision > Export Metadata` or in the render
   as *Export Dolby Vision metadata XML*); the mastering house or packaging tool
   embeds it (or Resolve's **IMF** export includes it). Use the latest CM version the
   platform requires (v4.0 vs 2.9).

## 6. HDR10 and deliverables
For HDR10: Deliver page > *Advanced Settings* > **HDR10 Metadata** (MaxCLL/MaxFALL
measured by Resolve when enabled, mastering display primaries/luminance); H.265/HEVC
Main10 or ProRes with sidecar. Platforms ask for: PQ master at mastering nits, Dolby
Vision XML (or HDR10+ JSON), an SDR derivative or trims, and a QC report (nits,
MaxCLL, frame-rate, colour primaries flagged correctly in the file). IMF packages
(Resolve Studio exports IMF via the *Kakadu* JPEG 2000 encoder) carry it together.

## Gotchas
- Grading HDR on a bright TV with "HDR mode"; the master is 300 nits too hot or cold.
- Diffuse white pushed to 500+ nits; every scene glares and the SDR trim can't recover.
- Forgetting to re-analyse after regrading; trims mismatch the picture.
- Output colour space set to Rec.2020 P3-limited vs full Rec.2020 - platforms specify which.
- No Soft Clip: speculars hard-clip at 1000 nits with coloured edges.

## Verify
- [ ] Colour-managed project with a PQ/HLG output and a wide working space; reference HDR monitor at mastering nits.
- [ ] Waveform in nits: diffuse white ~100-200, peaks within mastering limit with roll-off.
- [ ] Dolby Vision analysed per shot; 100-nit trim checked on an SDR monitor.
- [ ] Deliverables rendered with correct metadata (MaxCLL/MaxFALL or DV XML) and flagged primaries.
