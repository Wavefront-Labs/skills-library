---
id: creative-arts.animation.encode-delivery.chroma-subsampling
name: chroma-subsampling
category: creative-arts
field: animation
product: encode-delivery
tags: [chroma-subsampling, pixel-format, pix-fmt, yuv420p, yuv422p10le, yuv444p, ffmpeg, red-edges, line-art, color-bleed]
level: practitioner
status: verified
description: "Choose 4:4:4, 4:2:2 or 4:2:0 for animation masters and deliveries; avoid soft red line edges; set -pix_fmt and scaler chroma flags correctly."
sources:
  - https://trac.ffmpeg.org/wiki/Chroma%20Subsampling
  - https://ffmpeg.org/ffmpeg-scaler.html
  - https://support.apple.com/en-us/102207
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Chroma subsampling for animation

**Goal:** keep saturated line art and flat colour edges crisp through the chain. Y'CbCr formats
store colour at reduced resolution: 4:4:4 full, 4:2:2 half horizontal, 4:2:0 half in both
directions. Flat-colour animation (red outlines, saturated text, UI graphics) is where 4:2:0
damage is most visible: edges bleed and look soft or stair-stepped.

## Which where

| Stage | Format | ffmpeg pix_fmt |
|---|---|---|
| Renders/comp | RGB(A) EXR/PNG/TIFF, no subsampling | `rgb48le`, `rgba` |
| Edit/master mezzanine | 4:2:2 10-bit (ProRes 422 HQ) | `yuv422p10le` |
| Graphics-heavy master, archival | 4:4:4 (ProRes 4444) | `yuva444p10le` |
| Web/streaming delivery | 4:2:0 8-bit (or 10-bit HEVC/AV1) | `yuv420p` |

Deliver 4:2:0 only at the last encode; never round-trip through 4:2:0 twice.

## Commands

```bash
# RGB PNG frames to 4:2:0 delivery with a good scaler for the chroma downsample
ffmpeg -framerate 24 -i f_%04d.png -vf "scale=out_color_matrix=bt709:flags=lanczos+accurate_rnd+full_chroma_int,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv" \
  -c:v libx264 -crf 18 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 out.mp4

# 4:4:4 H.264 for an internal review copy where edges matter (High 4:4:4 Predictive;
# player support is limited)
ffmpeg -i in.mov -c:v libx264 -crf 16 -pix_fmt yuv444p review444.mp4
```

`accurate_rnd` and `full_chroma_int` are swscale flags (ffmpeg-scaler manual); compare the result on red-on-black line art.

## Design-side mitigation

If a show must ship 4:2:0, avoid 1-pixel saturated red/blue lines on contrasting colour, and
keep small text strokes wide enough to survive halved chroma resolution. Test the style frames through the delivery encode early.

## Gotchas

- 4:2:0 needs even width and height (the `colorspace` filter entry also requires an even input size). Scale or pad odd sizes first (`scale=trunc(iw/2)*2:trunc(ih/2)*2`).
- Player support for 4:4:4 and 4:2:2 H.264 is limited; deliver web files as `yuv420p` and test on the target players.
- With ffmpeg 8.0.1 the `-color_primaries` and `-color_trc` output options alone did not reach the file for untagged RGB input (ffprobe showed `unknown`); the `setparams` filter above does, as the command shows.
- With `auto`, the `scale` filter leaves matrix and range to negotiation, and RGB to YUV then prefers BT.601 limited range (ffmpeg-filters): set `out_color_matrix` and tag the stream
  (`creative-arts.animation.encode-delivery.colour-metadata-tags`).

## Verify

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=pix_fmt -of default=nk=1:nw=1 out.mp4
```

Then view a red-outline frame at 400% against the source PNG.

## Checked

2026-10-28. Confirmed: `scale` flags `accurate_rnd`, `full_chroma_int`, `lanczos` and `out_color_matrix` (ffmpeg-scaler, ffmpeg-filters); the `scale` note that `auto` prefers BT.601 limited range for RGB to YUV; ffprobe `-of default=nk=1:nw=1`; ProRes `4444` profile. Removed: the 'width not divisible by 2' error text, browser playback claims, the BT.601-for-SD claim, DNxHR HQX, the 2 px stroke figure.

2026-11-01 run check: the PNG-to-yuv420p command and the yuv444p command ran (ffprobe: `yuv420p`; profile `High 4:4:4 Predictive` for the 4:4:4 file); an odd-sized source (321x241) failed with `width not divisible by 2` and encoded after `scale=trunc(iw/2)*2:trunc(ih/2)*2` (320x240); with the added `setparams` the four colour fields probed as bt709/bt709/bt709/tv. Fixed: the original command left primaries and transfer `unknown`.

Method: commands run with ffmpeg 8.0.1 (Windows build) on synthetic lavfi inputs, plus the ffmpeg manuals for the options above.
