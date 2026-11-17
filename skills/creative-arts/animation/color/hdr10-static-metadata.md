---
id: creative-arts.animation.color.hdr10-static-metadata
name: hdr10-static-metadata
category: creative-arts
field: animation
product: color
tags: [hdr10-metadata, hdr, maxcll, maxfall, mastering-display, st-2086, x265, master-display, ffmpeg, hdr10]
level: advanced
status: draft
description: "Measure and write HDR10 static metadata (ST 2086 mastering display, MaxCLL, MaxFALL) into HEVC encodes with x265 and verify it with ffprobe/MediaInfo."
sources:
  - https://x265.readthedocs.io/en/master/cli.html#vui-video-usability-information-options
  - https://www.itu.int/rec/R-REC-BT.2100
  - https://ffmpeg.org/ffprobe.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# HDR10 static metadata

**Goal:** HDR10 files that TVs tone map correctly. Static metadata describes the mastering display
(SMPTE ST 2086) and the content light levels (MaxCLL: brightest pixel; MaxFALL: brightest frame
average), for the whole programme.

## Getting the values

- Mastering display: from the reference monitor used (primaries, white point, min/max luminance).
  P3-D65 1000-nit monitor is the common case.
- MaxCLL/MaxFALL: measured from the final graded content. Resolve: Colour page, HDR analysis or
  the Dolby Vision analysis results; dedicated tools also compute them. Do not type the monitor
  peak as MaxCLL.

## x265 encode with metadata

```bash
ffmpeg -i master_pq.mov -c:v libx265 -pix_fmt yuv420p10le -crf 18 -preset slow -tag:v hvc1 \
 -x265-params "hdr10=1:repeat-headers=1:colorprim=bt2020:transfer=smpte2084:colormatrix=bt2020nc:\
master-display=G(13250,34500)B(7500,3000)R(34000,16000)WP(15635,16450)L(10000000,50):max-cll=850,350" \
 -c:a copy out_hdr10.mp4
```

- `master-display` uses 0.00002 units for chromaticity and 0.0001 cd/m2 for luminance. The string
  above is P3-D65 primaries, D65 white, 1000 nits max, 0.005 nits min.
- `max-cll=MaxCLL,MaxFALL` in nits.
- `hdr10=1` and `repeat-headers=1` put SEI messages on every keyframe so seeking/streaming players
  see them.

## Verify

```bash
ffprobe -v error -select_streams v:0 -show_frames -read_intervals %+#1 \
  -show_entries frame=side_data_list -of json out_hdr10.mp4
mediainfo out_hdr10.mp4 | grep -i -E "mastering|maximum (content|frame)"
```

Mastering display luminance/primaries and MaxCLL/MaxFALL read back as set; colour tags read
`bt2020`/`smpte2084`/`bt2020nc`.

## Gotchas

- Wrong-order primaries in `master-display` (x265 expects G, B, R) is a common error.
- Exceeding the declared MaxCLL in content leads TVs to clip; measure from the final master, after
  all trims and fixes.
- Some deliveries (Netflix) want Dolby Vision plus HDR10 fallback; the HDR10 values then come from
  the Dolby analysis (L1 max/avg across the programme).
