---
id: creative-arts.animation.encode-delivery.colour-metadata-tags
name: colour-metadata-tags
category: creative-arts
field: animation
product: encode-delivery
tags: [color-tags, pixel-format, color-primaries, color-trc, colorspace, bt709, nclc, gamma-shift, quicktime-gamma, ffmpeg, encode]
level: advanced
status: verified
description: "Tag colour primaries, transfer and matrix in ffmpeg encodes so players show the right colours; fix the QuickTime gamma shift and untagged files."
sources:
  - https://ffmpeg.org/ffmpeg-codecs.html#Codec-Options
  - https://trac.ffmpeg.org/wiki/colorspace
  - https://www.itu.int/rec/R-REC-BT.709
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Colour metadata tags in encodes

**Goal:** the encoded file carries correct colour primaries, transfer characteristic and
matrix coefficients, so every player decodes it the way the grade was viewed. Untagged files
are guessed at, and players can guess differently.

## The three tags

| Flag | Meaning | SDR HD value |
|---|---|---|
| `-color_primaries` | gamut | `bt709` |
| `-color_trc` | transfer function | `bt709` (or `iec61966-2-1` for sRGB) |
| `-colorspace` | Y'CbCr matrix | `bt709` |
| `-color_range` | levels | `tv` (limited) |

## Standard SDR delivery

```bash
ffmpeg -i graded.mov -vf "scale=out_color_matrix=bt709:out_range=tv,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv" \
  -c:v libx264 -crf 18 -pix_fmt yuv420p \
  -color_primaries bt709 -color_trc bt709 -colorspace bt709 -color_range tv \
  -movflags +faststart -c:a aac out.mp4
```

With ffmpeg 8.0.1 the `-color_primaries` / `-color_trc` options alone left both fields `unknown` in ffprobe for an untagged source (only `-colorspace` and `-color_range` reached the file); the `setparams` filter puts all four in the frames and the file. The tags only label; the `scale` filter (or `zscale`/`colorspace`) does the actual conversion.
Labelling without converting, or converting without labelling, both produce wrong colour.

## Converting between spaces (not just retagging)

```bash
# BT.601 SD source to BT.709 HD
ffmpeg -i sd.mov -vf "scale=1920:1080,colorspace=all=bt709:iall=bt601-6-625:fast=0" ...
# with zimg for accurate transfer handling
ffmpeg -i in.mov -vf "setparams=colorspace=smpte170m:color_primaries=smpte170m:color_trc=smpte170m:range=limited,zscale=matrix=709:primaries=709:transfer=709:range=limited,format=yuv420p" ...
# zscale needs to know the input: on an untagged source it fails with 'no path between colorspaces',
# so tag the source with its real values first (setparams), and keep -colorspace/-color_primaries/-color_trc on the output
```

## The QuickTime gamma shift

Renders that look right in the comp app but different in QuickTime on macOS usually mean the
viewing assumption and the tag disagree. Policy:
- Grade on the reference display your delivery spec names and tag to match (`bt709` for Rec.709 deliveries).
- For web-first shows, some studios tag `iec61966-2-1` (sRGB) instead. Pick one show-wide and write it in the delivery bible.
- Never "fix" the shift by baking a gamma curve into pixels and keeping the old tag.

## Gotchas

- PNG/EXR frames into ffmpeg are RGB; with `auto`, the `scale` filter prefers BT.601 limited range for RGB to YUV unless the graph requires otherwise. Always set `out_color_matrix=bt709`.
- `-c copy` keeps stream tags from the input; retagging a stream copy needs a bitstream filter,
  for example `-bsf:v h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1`.

## Verify

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=color_space,color_transfer,color_primaries,color_range -of default=nw=1 out.mp4
```

All four fields present and equal to the delivery spec; then compare a still in two players.

## Checked

2026-10-28. Confirmed: codec options `-color_primaries`, `-color_trc`, `-colorspace`, `-color_range` and the values `bt709` and `iec61966-2-1` (ffmpeg-codecs); `colorspace` filter options `all`, `iall`, `fast` and `bt601-6-625` (ffmpeg-filters, ffmpeg colorspace wiki); `h264_metadata` options `video_full_range_flag`, `colour_primaries`, `transfer_characteristics`, `matrix_coefficients` (ffmpeg bitstream filters source); `scale` `auto` behaviour. Removed: the ColorSync explanation, the gamma 2.4 and 2.2 statements, the `colr`/`nclc` atom statement, the cross-player guess claim.

2026-11-01 run check: with `setparams` the SDR command probed as color_space bt709, color_transfer bt709, color_primaries bt709, color_range tv; without it primaries and transfer were `unknown` (fixed above). `colorspace=all=bt709:iall=bt601-6-625:fast=0` ran and tagged bt709; `-color_trc iec61966-2-1` via `setparams` probed as `iec61966-2-1`; the `h264_metadata` bitstream-filter retag on `-c copy` ran and probed bt709; the zscale chain ran once the source was tagged.

Method: commands run with ffmpeg 8.0.1 (Windows build, with libzimg) on synthetic lavfi inputs, plus the ffmpeg manuals for the options above.
