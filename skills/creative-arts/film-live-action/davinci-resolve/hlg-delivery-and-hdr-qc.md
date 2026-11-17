---
id: creative-arts.film-live-action.davinci-resolve.hlg-delivery-and-hdr-qc
name: hlg-delivery-and-hdr-qc
category: creative-arts
field: film-live-action
product: davinci-resolve
tags: [davinci-resolve, resolve, film-live-action, hlg-grading, hlg-delivery, hlg-broadcast, hdr-qc, metadata-validation, hdr-deliverable-check, maxcll, maxfall, dolby-vision-xml, hdr10]
level: practitioner
status: draft
description: "Grade and deliver HLG for broadcast from Resolve, and QC HDR deliverables: PQ/HLG tags, MaxCLL/MaxFALL, Dolby Vision metadata validation and SDR trim checks."
sources:
  - "ITU-R BT.2100 (PQ and HLG) and BT.2408 (operational practices for HDR) - https://www.itu.int"
  - "https://www.dolby.com/about/support/guide/ (Dolby Vision mastering and Metafier/metadata validation)"
  - "https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_Reference_Manual.pdf (Resolve Reference Manual - HDR, HDR10 metadata, Dolby Vision)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# HLG delivery and HDR QC

**Goal:** HDR masters that play correctly on every target - broadcast HLG and streaming
PQ - with metadata that validates.

## 1. HLG (Hybrid Log-Gamma)
- Broadcast HDR (BBC/NHK): scene-referred, backwards-compatible with SDR displays,
  **no static metadata** needed.
- Resolve: colour-managed project with output colour space **Rec.2100 HLG** (timeline in
  DaVinci Wide Gamut/ Intermediate); monitor on an HLG-capable display at 1000 nits (BT.2408
  reference).
- Levels (BT.2408): **HDR reference white / graphics white at 75% HLG signal** (~203 nits
  on a 1000-nit display); skin typically around 45-56%; speculars above 75%.
- Check the SDR compatibility view (HLG on an SDR monitor or a down-conversion LUT) -
  broadcasters convert for SDR distribution.
- Deliver per broadcaster spec (e.g. UK DPP/ AS-11 UHD HDR profiles): 10-bit,
  Rec.2020 colour, HLG transfer flagged in the file.

## 2. PQ/HDR10 metadata
For HDR10 (PQ) deliverables, set **mastering display** metadata (P3-D65, 1000 or 4000
nits) and compute **MaxCLL** (max content light level) and **MaxFALL** (max frame-average
light level) - Resolve can analyse and embed (*Project Settings > Color Management >
HDR10* / Deliver options); verify values are plausible (MaxCLL below the mastering peak).

## 3. Dolby Vision
- Analyse all shots (*Dolby Vision > Analyse*), make **trims** for target displays (100-nit
  SDR at minimum, often 600/1000), export the **Dolby Vision XML** metadata (CM v4.0).
- **Validate** the XML with Dolby's Metafier/ validation tool (or the platform's tool);
  check that shot boundaries match the picture (re-analyse after any edit change).

## 4. HDR QC
- Watch the entire HDR master on a reference HDR monitor at mastering level; then the
  SDR derivatives (trims or HLG down-conversion).
- Check: clipping, banding (10-bit gradients), noise in shadows, flashing/ photosensitivity,
  out-of-gamut (CIE scope), consistent white levels for titles/graphics (203 nits PQ /
  75% HLG).
- File checks with MediaInfo: transfer characteristics (PQ = SMPTE ST 2084, HLG = ARIB
  STD-B67), colour primaries BT.2020, matrix, bit depth, HDR10 metadata present.
- Run automated QC if the spec requires.

## Gotchas
- HLG graded on a PQ monitor setting - levels wrong.
- Missing or implausible MaxCLL/MaxFALL.
- Dolby Vision XML from a previous cut - shot boundaries shifted.
- Titles at 1000 nits blinding viewers.

## Verify
- [ ] HLG output tagged correctly; reference white at 75%; SDR compatibility checked.
- [ ] HDR10 mastering metadata and MaxCLL/MaxFALL embedded and plausible.
- [ ] Dolby Vision XML analysed on the final cut and validated.
- [ ] Full HDR and SDR viewing QC plus MediaInfo checks done.
