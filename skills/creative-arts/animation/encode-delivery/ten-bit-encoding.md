---
id: creative-arts.animation.encode-delivery.ten-bit-encoding
name: ten-bit-encoding
category: creative-arts
field: animation
product: encode-delivery
tags: [10-bit, pixel-format, yuv420p10le, banding, gradients, hevc, main10, av1, prores, dither, ffmpeg]
level: advanced
status: verified
description: "Use 10-bit encodes to stop gradient banding in animation (skies, glows, fog): codec/profile support, dithering down to 8-bit, compatibility checks."
sources:
  - https://trac.ffmpeg.org/wiki/Encode/H.265
  - https://ffmpeg.org/ffmpeg-scaler.html#scaler_005foptions
  - https://support.google.com/youtube/answer/1722171
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# 10-bit encoding against banding

**Goal:** smooth gradients. Flat-shaded animation with soft skies, rim glows, fog and vignette
falloffs bands badly in 8-bit 4:2:0 at streaming bitrates. 10-bit gives 4x the code values per
channel (two extra bits).

## Where 10-bit is safe

| Codec/profile | Playback support |
|---|---|
| HEVC Main10 (`libx265 -pix_fmt yuv420p10le`) | check decoder support on the target devices; Apple's HLS specification allows HEVC up to Main 10 |
| AV1 10-bit (`libsvtav1`) | check decoder support on the target devices |
| ProRes | 10-bit mezzanine use |
| H.264 High 10 (`libx264 -pix_fmt yuv420p10le`) | decoder support varies; check the target first |

Rule: for broad compatibility keep H.264 delivery at 8-bit; when banding matters, use 10-bit HEVC or AV1 where the target decodes it, or upload a
10-bit ProRes mezzanine to platforms that re-encode.

```bash
ffmpeg -i master_prores.mov -c:v libx265 -preset slow -crf 20 -pix_fmt yuv420p10le \
  -x265-params profile=main10 -tag:v hvc1 -c:a aac -b:a 192k out_hevc10.mp4
```

## When you must ship 8-bit: dither, do not truncate

Render and grade in 16-bit/float, then dither once at the final conversion:

```bash
ffmpeg -i master16.mov -vf "scale=out_color_matrix=bt709:flags=lanczos+accurate_rnd:sws_dither=ed,format=yuv420p" \
  -c:v libx264 -crf 16 -tune animation out8.mp4
```

Error-diffusion dither (`sws_dither=ed`) breaks bands into fine noise that the encoder keeps
better at low CRF. A small amount of grain added in comp can help survive the
platform's own re-encode; test on the target.

## Gotchas

- Rendering 8-bit PNGs and encoding to 10-bit does not remove banding already baked in. Keep
  16-bit PNG/EXR or ProRes 4444 from the renderer.
- Use ProRes for editing and HEVC for delivery.
- `-tag:v hvc1` sets the `hvc1` HEVC sample entry; Apple's HLS examples use `hvc1` codec strings.

## Verify

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,profile,pix_fmt -of default=nw=1 out_hevc10.mp4
```

Expect `hevc`, `Main 10`, `yuv420p10le`. Then view the worst gradient shot on a calibrated
display at 100% next to the 8-bit version.

## Checked

2026-10-28. Confirmed: `sws_dither=ed` error diffusion (ffmpeg-scaler), libsvtav1 encoder and libx265 pass-through of `-x265-params`, Apple HLS specification HEVC limits and `hvc1` codec strings, 2 extra bits = 4x code values (arithmetic). Removed: the 'often smaller at equal quality' claim, the browser and TV support claims, DNxHR HQX, the grain percentage, the QuickTime requirement for `hvc1`.

2026-11-01 run check: the HEVC command ran and the Verify query reported `hevc`, `Main 10`, `yuv420p10le`, tag `hvc1`; the `sws_dither=ed` 8-bit command ran; `libx264 -pix_fmt yuv420p10le` gave profile `High 10`. `libsvtav1` is not compiled into the test build, so that table row rests on the ffmpeg encoder documentation only.

Method: commands run with ffmpeg 8.0.1 (Windows build) on synthetic lavfi inputs, plus the ffmpeg manuals and Apple HLS specification for the claims above.
