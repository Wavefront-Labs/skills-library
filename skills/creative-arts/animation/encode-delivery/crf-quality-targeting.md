---
id: creative-arts.animation.encode-delivery.crf-quality-targeting
name: crf-quality-targeting
category: creative-arts
field: animation
product: encode-delivery
tags: [crf, rate-control, ffmpeg, libx264, libx265, constant-rate-factor, preset, tune-animation, quality, encode]
level: practitioner
status: verified
description: "Pick and verify a CRF value for libx264/libx265 animation encodes: preset trade-offs, tune animation, CRF ranges, when CRF is the wrong mode."
sources:
  - https://trac.ffmpeg.org/wiki/Encode/H.264
  - https://trac.ffmpeg.org/wiki/Encode/H.265
  - https://ffmpeg.org/ffmpeg-codecs.html#libx264_002c-libx264rgb
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# CRF quality targeting

**Goal:** a file whose quality is constant and known, with the bitrate left to float. CRF
(constant rate factor) is the right mode for masters you keep, review copies and uploads to
platforms that re-encode anyway (YouTube, Vimeo). It is the wrong mode when a delivery spec
names a bitrate or a file-size ceiling (use two-pass, see
`creative-arts.animation.encode-delivery.two-pass-abr-encoding`) or when a player has a buffer
limit (add VBV, see `creative-arts.animation.encode-delivery.vbv-maxrate-bufsize`).

## The command

```bash
ffmpeg -i in.mov -c:v libx264 -preset slow -crf 18 -tune animation \
  -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart out.mp4
```

- **Scale:** x264 CRF 0-51, lower = better; 0 is lossless for 8-bit only (use `-qp 0` for 10-bit) and gives huge files. Each +6 roughly halves the bitrate. The x265 default is 28, which the FFmpeg wiki says should look about like libx264 at CRF 23 at about half the file size.
- **Starting points:** the FFmpeg wiki treats 17 or 18 as visually lossless or nearly so, 17-28 as a subjectively sane range, and 23 as the x264 default. Go lower if you see banding in gradients.
- **Preset** changes speed and compression efficiency, not the quality target: at the same CRF
  `veryslow` gives a smaller file than `fast`, at very similar quality. Lock the preset per show
  so file sizes are comparable between versions. Never use `ultrafast` for anything kept.
- **`-tune animation`** is described by the FFmpeg wiki as good for cartoons, with higher deblocking and more reference frames. Use it for cel/toon renders; skip it for photoreal CG with grain (use `-tune grain`
  if grain must survive).

## Choosing the number by test, not by habit

1. Pick a 10-20 s stress section: fast motion, gradients (skies, glows), fine line art.
2. Encode it at CRF 14, 18, 22, 26 with the show preset.
3. Score each against the source (`creative-arts.animation.encode-delivery.vmaf-scoring`) and
   look at a gradient frame at 200% zoom.
4. Take the highest CRF whose VMAF meets your chosen threshold and that shows no banding or ringing on line art.

```bash
for q in 14 18 22 26; do
  ffmpeg -v error -ss 120 -t 15 -i master.mov -c:v libx264 -preset slow -tune animation \
    -crf $q -pix_fmt yuv420p -an test_crf$q.mp4
done
ls -l test_crf*.mp4
```

## Gotchas

- CRF output size is unpredictable: bitrate follows the content at the same CRF. Do not use CRF where a size cap applies.
- CRF results are only comparable with the same encoder, preset, tune and pixel format.
- A capped CRF encode (`-crf` with `-maxrate` and `-bufsize`) raises the CRF when the output would exceed the cap, and libx264 does not strictly control the maximum rate (FFmpeg wiki). Do not add those options by accident from a copied command.
- 10-bit x264 (`-pix_fmt yuv420p10le`) can cut banding, but not every player decodes High 10. Check the target first.

## Verify

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,profile,pix_fmt,bit_rate -of default=nw=1 out.mp4
ffmpeg -i out.mp4 -i master.mov -lavfi libvmaf -f null -
```

Profile and pixel format are what you asked for, and VMAF is at or above the threshold you
chose in the test.

## Checked

2026-10-28. Confirmed in the FFmpeg H.264 and H.265 encoding wikis: CRF range 0-51, 0 lossless for 8-bit only (`-qp 0` for 10-bit), 23 default, 17-18 visually lossless, +6 roughly halves the bitrate, x265 default 28 corresponding to x264 CRF 23, `-tune animation` description, `-tune grain` for x265, capped CRF with `-maxrate`/`-bufsize`, presets. Removed: x265 22-24 equals x264 18-20, 20-23 web range, 14-16 banding range, the 3x bitrate example, the `-b:v` ignore claim, the VMAF 95 threshold, the 10-bit CRF scale claim and browser decode claim.

2026-11-01 run check: the main command and the four-CRF loop ran (sizes fell monotonically 14 > 18 > 22 > 26: 553, 421, 309, 214 kB on a 3 s synthetic clip); the verify `ffprobe` query reported `h264`, `High`, `yuv420p`; `-lavfi libvmaf` ran; `-pix_fmt yuv420p10le` gave profile `High 10`; `-crf 0` with yuv420p gave `High 4:4:4 Predictive` (the lossless profile).

Method: commands run with ffmpeg 8.0.1 (Windows build) on synthetic lavfi inputs, plus the FFmpeg wiki and manuals for the CRF scale and tune claims.
