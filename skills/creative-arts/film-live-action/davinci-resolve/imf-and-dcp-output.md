---
id: creative-arts.film-live-action.davinci-resolve.imf-and-dcp-output
name: imf-and-dcp-output
category: creative-arts
field: film-live-action
product: davinci-resolve
tags: [davinci-resolve, resolve, film-live-action, imf-output, dcp-output, easydcp, kakadu, imf-app2e, dcp-kdm, cpl, supplemental-imf, interop-smpte-dcp]
level: practitioner
status: draft
description: "Render IMF and DCP packages from Resolve Studio: native vs easyDCP/Kakadu encoding, IMF App 2E settings and CPL metadata, DCP SMPTE vs Interop, encryption, and verification."
sources:
  - "https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_Reference_Manual.pdf (Resolve Reference Manual - IMF and DCP rendering)"
  - "https://partnerhelp.netflixstudios.com (Netflix - IMF delivery specifications)"
  - "https://www.easydcp.com (Fraunhofer easyDCP - DCP and IMF creation)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IMF and DCP output

**Goal:** a valid IMF package for streaming/distribution masters and a valid DCP for
cinema - rendered and verified before they leave the building.

## 1. Encoders
Resolve Studio includes a **native (Kakadu-based) JPEG 2000** encoder for IMF and DCP,
plus optional **easyDCP** licensed integration (more options, encryption, KDMs) - choose in
the Format menu (IMF / DCP vs easyDCP) on the Deliver page.

## 2. IMF
- Common profile: **IMF App 2E** (JPEG 2000, up to UHD, HDR support); Netflix requires
  specific constraints (see its IMF spec).
- Settings: resolution/frame rate, colour (Rec.709/ P3D65 PQ/ Rec.2020 PQ) and HDR
  metadata, bitrate/ quality, **CPL metadata** (title, content kind, version), audio
  channel configuration (soundfield groups such as 5.1 + stereo), subtitles (IMSC1 TTML).
- **Supplemental packages** reference an existing original version (OV) to add/replace
  segments or tracks (localisation) - Resolve supports creating supplemental IMF in
  recent versions; check spec acceptance.

## 3. DCP
- **SMPTE DCP** (modern standard) vs **Interop** (legacy, still accepted by some festivals -
  check their requirement).
- Resolution: 2K (1998x1080 flat, 2048x858 scope) or 4K equivalents; 24 fps (others if
  the venue supports); XYZ colour conversion from P3 (Resolve handles the transform -
  grade in P3-D65/DCI as per the colour pipeline).
- Audio: 5.1 or 7.1 PCM 24-bit 48 kHz in standard channel order; reel splitting optional.
- **Encryption** (KDMs) requires easyDCP or a mastering tool for key generation.
- Naming: follow the **Digital Cinema Naming Convention** (title_type_aspect_language
  _territory-rating_audio_resolution_studio_date_facility_standard_package).

## 4. Verify
- IMF: validate with **Netflix Photon** (open-source IMF validator) or the platform's
  tool; play in an IMF player (e.g. easyDCP Player+, Colorfront).
- DCP: validate with **DCP-o-matic's** checker or easyDCP Player; test in a cinema/
  projector if at all possible (subtitles, reels, audio routing).

## Gotchas
- Wrong colour/HDR metadata in the CPL - platform rejects.
- Interop DCP sent to a SMPTE-only festival (or vice versa).
- Unvalidated packages; failures discovered at ingest.
- Audio channel config in IMF not matching the spec's soundfield groups.

## Verify
- [ ] Encoder and profile match the spec (IMF App 2E / DCP SMPTE vs Interop).
- [ ] CPL metadata, colour, audio groups and subtitles correct.
- [ ] Package validated (Photon / DCP checker) and played back.
- [ ] Naming convention and encryption/KDMs handled.
