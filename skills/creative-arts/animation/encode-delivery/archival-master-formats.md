---
id: creative-arts.animation.encode-delivery.archival-master-formats
name: archival-master-formats
category: creative-arts
field: animation
product: encode-delivery
tags: [archival-master, archive, archiving, ffv1, mkv, dpx, openexr, prores-4444, lossless, preservation, bwf, long-term-storage]
level: advanced
status: draft
description: "Choose what to archive for an animated production and in which formats: lossless picture (FFV1/EXR/DPX), PCM stems, textless, project data, and format longevity."
sources:
  - https://www.loc.gov/preservation/digital/formats/fdd/fdd000341.shtml
  - https://datatracker.ietf.org/doc/html/rfc9043
  - https://www.dpconline.org/handbook/technical-solutions-and-tools/file-formats-and-standards
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Archival master formats

**Goal:** in 10 or 20 years someone can remaster, re-version or re-deliver the show without
re-rendering. Archive what cannot be recreated cheaply, in open, documented, lossless formats.

## What to archive

| Element | Format |
|---|---|
| Graded picture master | FFV1 in Matroska (lossless, open, RFC 9043) or 16-bit TIFF/DPX sequence; keep ProRes 4444 XQ only as an access copy |
| Ungraded/linear renders (if a regrade is possible) | OpenEXR (PIZ or ZIP lossless) per shot |
| Textless picture and graphics elements | same as picture master |
| Audio | BWF (24-bit 48 kHz PCM): printmaster, stems (D, M, E), M&E, music stems |
| Timed text | IMSC/TTML plus SRT |
| Project data | scene files, rigs, assets, shotlists, edit (AAF + OTIO + EDL), colour (CDL/LUT/OCIO config) |
| Documentation | delivery bible, colour pipeline notes, font licences, music cue sheets, credits |

## FFV1 command

```bash
ffmpeg -i graded_master.mov -map 0 -c:v ffv1 -level 3 -g 1 -slices 16 -slicecrc 1 \
  -pix_fmt yuv422p10le -c:a copy -f matroska archive_master.mkv
```
- `-level 3 -slicecrc 1` adds per-slice CRCs so corruption is detectable and localised.
- `-g 1` intra-only: any frame decodes on its own.
- Keep the master's native pixel format; do not subsample further.
- Verify lossless round trip with framemd5:
```bash
ffmpeg -i graded_master.mov -map 0:v -f framemd5 a.md5
ffmpeg -i archive_master.mkv -map 0:v -f framemd5 b.md5
diff a.md5 b.md5 && echo lossless
```

## Longevity rules

- Prefer open, standardised formats with multiple independent decoders (FFV1, EXR, TIFF, WAV)
  over proprietary ones.
- Avoid application-specific project files as the only copy: export interchange alongside.
- Record software versions (renderer, DCC, plug-ins) with scene files; reopening needs them.
- Two copies, two media types, one off-site; checksums for both
  (`creative-arts.animation.encode-delivery.checksum-fixity`).

## Verify

Restore test: pull a random episode from archive, decode the FFV1 master end to end
(`ffmpeg -v error -i archive_master.mkv -f null -` prints nothing), and play the audio stems.
