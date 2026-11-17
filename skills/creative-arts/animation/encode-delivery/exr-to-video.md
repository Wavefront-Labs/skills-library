---
id: creative-arts.animation.encode-delivery.exr-to-video
name: exr-to-video
category: creative-arts
field: animation
product: encode-delivery
tags: [exr-to-video, image-sequence, openexr, ocio, oiiotool, aces, view-transform, linear, ffmpeg, review-movie, dailies]
level: advanced
status: docs-checked
description: "Turn scene-linear EXR render sequences into correct-looking review or delivery movies: apply the OCIO view transform with oiiotool, then encode with ffmpeg."
sources:
  - https://openimageio.readthedocs.io/en/latest/oiiotool.html
  - https://opencolorio.readthedocs.io/en/latest/guides/using_ocio/using_ocio.html
  - https://ffmpeg.org/ffmpeg-formats.html#image2-1
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# EXR sequences to video

**Goal:** a movie that looks like the comp viewer. EXRs hold scene-linear light; ffmpeg reads
them, but a raw `ffmpeg -i f.%04d.exr out.mp4` applies no display transform, so scene-linear values are
encoded as if they were display values. Apply the display transform explicitly: with oiiotool as below, or with
ffmpeg's `ocio` filter in builds configured with `--enable-libopencolorio`.

## Reliable route: OIIO applies OCIO, ffmpeg encodes

```bash
export OCIO=/path/to/show/config.ocio
mkdir -p disp
oiiotool --frames 1001-1240 shot010.%04d.exr \
  --colorconvert "ACEScg" "sRGB - Display" -d uint16 -o disp/shot010.%04d.png
# or use the config's display/view pair:
oiiotool --frames 1001-1240 shot010.%04d.exr --ociodisplay "sRGB - Display" "ACES 1.0 - SDR Video" -d uint16 -o disp/shot010.%04d.png
ffmpeg -framerate 24 -start_number 1001 -i disp/shot010.%04d.png \
  -vf "scale=out_color_matrix=bt709:sws_dither=ed" -c:v libx264 -crf 16 -pix_fmt yuv420p \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 shot010_review.mp4
```

Colourspace, display and view names come from your OCIO config (the names above are examples from an ACES config); use the same ones the artists use in their comp app. ffmpeg's `ocio` filter likewise takes `input`, `output`, `display` and `view`, and uses the config named by the `OCIO` environment variable unless `config` is set.

For Rec.709 video delivery choose the config's Rec.1886/Rec.709 display, not sRGB, so the
encoded file matches a broadcast monitor.

## Choosing the layer

Multi-layer EXRs: select the beauty explicitly, e.g. `oiiotool in.exr --ch R,G,B` (see the `--ch` entry in the oiiotool manual for naming other channels). A wrong layer yields black or a utility pass.

## Burn-ins for review

Add shot/version/frame burn-ins after the colour transform in the ffmpeg step (see
`creative-arts.animation.editorial.review-burn-ins`).

## Gotchas

- Converting to 8-bit PNG before ffmpeg bands soft gradients; write 16-bit and dither once.
- Letting OIIO read the EXRs keeps the colour conversion and the read in one step.
- Alpha: premultiplied EXR over black looks fine; if comping over a colour later, keep the
  alpha (ProRes 4444) instead.

## Verify

Load one frame of the PNG output and the same EXR in the comp viewer with the show view;
pick a pixel in midtones and highlights: values must match within a code value or two.

## Checked

2026-10-28. Confirmed: oiiotool `--frames` sequence syntax, `--colorconvert`, `--ch R,G,B`, `-d uint16` and `--ociodisplay` exist in the oiiotool manual; ffmpeg `ocio` filter options (`config`, `input`, `output`, `display`, `view`, `format`) and its `--enable-libopencolorio` requirement in the ffmpeg-filters source; `scale` `sws_dither=ed`. Fixed: the claim that ffmpeg knows nothing about OCIO (recent builds have an `ocio` filter). Removed: AgX view name, the named-layer `--ch` form, the DWAA/DWAB ffmpeg compatibility claim, the dark-and-clipped description.

Run 2026-11-01 with ffmpeg and ffprobe 8.0.1 on Windows (Git Bash), scripts in a scratch folder: ffmpeg wrote and read a 24-frame EXR sequence and encoded it with the skill's `scale=out_color_matrix=bt709:sws_dither=ed` chain (the stream kept the linear transfer tag); the `ocio` filter does not exist in this build (`No such filter: 'ocio'`), as the skill's build caveat says. Not run: oiiotool (not installed) and all OCIO conversions, so the skill stays docs-checked.

Method: documentation plus partial commands run (ffmpeg 8.0.1).
