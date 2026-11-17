---
id: creative-arts.animation.encode-delivery.imf-package-delivery
name: imf-package-delivery
category: creative-arts
field: animation
product: encode-delivery
tags: [imf, delivery-spec, imp, cpl, smpte-st-2067, jpeg2000, app2e, photon, mxf, supplemental-package, netflix]
level: sme
status: draft
description: "Understand, build and validate an IMF package (IMP): CPL, PKL, ASSETMAP, MXF track files, App 2E profile, supplemental versions, Photon validation."
sources:
  - https://www.smpte.org/standards/st2067
  - https://github.com/Netflix/photon
  - https://partnerhelp.netflixstudios.com/hc/en-us
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IMF package delivery

**Goal:** deliver a master as an Interoperable Master Format package that a streamer's ingest
accepts first time. IMF (SMPTE ST 2067) replaces "one ProRes per version" with one set of
track files plus playlists that describe each version.

## Anatomy of an IMP (one folder)

| File | Role |
|---|---|
| `ASSETMAP.xml` | lists every file in the package by UUID |
| `PKL_<uuid>.xml` | packing list: file hashes (SHA-1) and sizes |
| `CPL_<uuid>.xml` | Composition Playlist: timeline of video, audio, subtitle segments; one per version |
| `VOLINDEX.xml` | volume index |
| `*.mxf` | track files: one per essence (video JPEG 2000, each audio language, IMSC timed text) |
| `OPL_<uuid>.xml` (optional) | output profile list, how to render a CPL |

**Supplemental package:** a later IMP containing only new track files (say a French dub or a
fixed shot) plus a new CPL that references the original package's assets by UUID. This is how
versions and fixes are delivered without resending terabytes.

## Profiles

- **App 2E** (ST 2067-21): JPEG 2000 (lossless or high-bitrate lossy) up to 4K, HDR and SDR,
  the common streaming profile. Netflix requires App 2E IMF for most originals.
- Audio: 24-bit 48 kHz PCM in MXF, one track file per sound field group (5.1, stereo, M&E),
  with MCA labels (SMPTE ST 377-4) identifying language and channel roles.
- Timed text: IMSC1 in MXF (see `creative-arts.animation.encode-delivery.subtitles-captions` for authoring).

## Making one

IMF mastering is done in dedicated tools (Resolve Studio IMF export, Clipster, Colorfront,
Rhozet/Vantage, or the open-source `asdcplib`-based toolchains). Workflow:
1. Final graded master and final mix approved and conformed to the same edit.
2. Export App 2E video track file, audio track files with MCA labels, IMSC timed text.
3. Build CPL with correct edit rate (e.g. 24/1 or 24000/1001), content title, content kind,
   and per-segment entry points.
4. Generate PKL hashes, ASSETMAP, then validate.

## Validate with Photon (Netflix open source)

```bash
java -cp photon-all.jar com.netflix.imflibrary.app.IMPAnalyzer /path/to/IMP_folder
```
Fix every error; warnings are often accepted but read them (MCA label mistakes are common).

## Gotchas

- Edit rates must match across video, audio and timed text in a CPL.
- Renaming files after PKL generation breaks hashes and the asset map.
- Audio channel MCA labels wrong = language or layout misidentified at ingest.

## Verify

Photon reports no errors; the CPL opens in an IMF player (e.g. Resolve, or a vendor viewer)
and plays every version with the right audio and subtitles.
