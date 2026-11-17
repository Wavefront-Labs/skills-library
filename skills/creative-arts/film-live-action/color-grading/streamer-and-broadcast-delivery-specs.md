---
id: creative-arts.film-live-action.color-grading.streamer-and-broadcast-delivery-specs
name: streamer-and-broadcast-delivery-specs
category: creative-arts
field: film-live-action
product: color-grading
tags: [color-grading, film-live-action, netflix-spec, netflix-delivery, netflix-imf, broadcast-spec, as-11, dpp-delivery, ebu-r103, ebu-r128, legal-levels, textless, localisation-masters, versioning]
level: practitioner
status: draft
description: "Meet streamer and broadcast delivery specs: Netflix IMF and colour requirements, UK DPP AS-11 and EBU R103 legal levels, loudness, textless elements and versioned masters."
sources:
  - "https://partnerhelp.netflixstudios.com (Netflix Partner Help Center - Originals Delivery Specifications)"
  - "https://www.thedpp.com (DPP - AS-11 UK technical delivery specifications)"
  - "https://tech.ebu.ch/publications/r103 (EBU R103 - video signal tolerance in file-based delivery)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Streamer and broadcast delivery specs

**Goal:** masters that pass the distributor's technical QC first time.

## 1. Read the spec first
Get the current spec PDF from the distributor at the start of post (not at delivery);
specs change yearly. Build a checklist from it.

## 2. Netflix (example of a streamer spec)
- **IMF** (App 2E) primary deliverable, Dolby Vision HDR (P3-D65 PQ) master + SDR derived
  via Dolby Vision trims for Originals; UHD resolution; native frame rate.
- **Approved cameras** list for originals; colour pipeline documented.
- Audio: 5.1 and Atmos where required, with loudness at **-27 LKFS (+/-2) dialogue-gated**
  per their spec; M&E; stereo.
- Timed text (IMSC1.1), audio description, forced narratives; textless and
  title/credit specs; QC via their vendors.

## 3. UK broadcast (DPP AS-11 UK DPP HD)
- MXF OP1a with **AVC-Intra 100** (HD) video, specific audio track layout and metadata
  (programme title, segmentation of parts, lines, captioning flags) in the AS-11 schema.
- **EBU R103** levels: luma -1% to 103% (RGB components within -5% to 105%) - preferred
  range 0-100%; out-of-range excursions fail QC.
- **Loudness EBU R128**: -23 LUFS integrated (+/-0.5 in UK DPP), max true peak -1 dBTP.
- **Photosensitive epilepsy** check (Ofcom guidance; Harding test) mandatory.
- Line-up: bars and tone, clock/ ident, black between parts per spec.

## 4. US broadcast
Typically ATSC/ network specs: -24 LKFS (ATSC A/85), closed captions (CEA-608/708),
legal range 7.5/ 0 IRE setups per network spec; ProRes or XDCAM deliverables.

## 5. Textless and versions
- **Textless** elements: every shot with text over picture delivered clean (as a
  separate textless reel or appended at the end of the master, with handles) for
  localisation.
- **Versions**: theatrical, airline, broadcast-edited (language/ nudity), territory
  versions; manage with version-named timelines and an EDL of differences; IMF supplemental
  packages handle many versions efficiently.

## Gotchas
- Working from last year's spec.
- Graphics/titles outside legal levels (illegal whites, super-saturated colours).
- Loudness measured on the wrong gating/ standard.
- Textless shots missing handles.

## Verify
- [ ] Current spec obtained and checklist built.
- [ ] Levels legal per EBU R103/ network; loudness per spec.
- [ ] Container, codec, metadata and audio layout match the spec.
- [ ] Textless and version masters delivered with handles.
