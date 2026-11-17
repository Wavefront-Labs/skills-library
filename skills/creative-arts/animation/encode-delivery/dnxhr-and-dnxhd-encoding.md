---
id: creative-arts.animation.encode-delivery.dnxhr-and-dnxhd-encoding
name: dnxhr-and-dnxhd-encoding
category: creative-arts
field: animation
product: encode-delivery
tags: [dnxhr, dnxhd, avid, mezzanine, intermediate-codec, prores-alternative, ffmpeg]
level: practitioner
status: verified
description: "Encode DNxHR and DNxHD with ffmpeg: profiles from LB to 444, pixel formats, DNxHD fixed bitrates, container and audio choices, and Avid compatibility."
sources:
  - https://ffmpeg.org/documentation.html
  - https://ffmpeg.org/ffmpeg-codecs.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# DNxHR / DNxHD

DNxHD and DNxHR are Avid's intermediate editing codecs, widely used for editorial and exchange as alternatives to ProRes. FFmpeg encodes both with the `dnxhd` encoder.

## DNxHR (resolution-independent)
Profiles (set with `-profile:v`):
| Profile | Chroma / depth | Typical use |
|---|---|---|
| `dnxhr_lb` | 4:2:2 8-bit | Offline proxy |
| `dnxhr_sq` | 4:2:2 8-bit | Standard editing |
| `dnxhr_hq` | 4:2:2 8-bit | High quality |
| `dnxhr_hqx` | 4:2:2 10-bit | UHD/HDR, higher quality |
| `dnxhr_444` | 4:4:4 10-bit | Graphics and finishing |

```bash
ffmpeg -i in.mov -c:v dnxhd -profile:v dnxhr_hq -pix_fmt yuv422p \
  -c:a pcm_s16le out.mov
# 10-bit HQX
ffmpeg -i in.mov -c:v dnxhd -profile:v dnxhr_hqx -pix_fmt yuv422p10le -c:a pcm_s24le out.mov
# 4:4:4
ffmpeg -i in.mov -c:v dnxhd -profile:v dnxhr_444 -pix_fmt yuv444p10le out.mov
```

## DNxHD (legacy, fixed combinations)
- DNxHD supports specific **resolution, frame rate and bitrate combinations** (for example 1920x1080 at defined bitrates), so you set `-b:v` to a valid value and the frame size and rate must match one of the standard formats, otherwise FFmpeg errors. Use DNxHR where you can; it removes this restriction.

## Container and audio
- `.mov` (QuickTime) or `.mxf` (Avid-friendly; use `-f mxf`); PCM audio is standard (`pcm_s16le` or `pcm_s24le`, 48 kHz).
- Set colour tags where appropriate (`colour-metadata-tags.md`); check range handling (`full-vs-limited-range.md`).

## Choosing
- Use DNxHR where the receiving team works in Avid, or the delivery spec names it. For ProRes-based pipelines see `mezzanine-master.md`.
- File sizes are large; plan storage and archive formats with `archival-master-formats.md`.

## Checked
Run with FFmpeg 8.0.1 on 2026-10-18: each profile in the table (`dnxhr_lb`, `dnxhr_sq`, `dnxhr_hq` with `yuv422p`, `dnxhr_hqx` with `yuv422p10le`, `dnxhr_444` with `yuv444p10le`) encoded and `ffprobe` reported the matching profile and pixel format; the `.mxf` command with `-f mxf` and `pcm_s16le` at 48 kHz worked; encoding DNxHD with a bitrate or frame size that is not a standard combination makes FFmpeg print `video parameters incompatible with DNxHD` and list the valid profiles.

## Verify
- [ ] `ffprobe` shows the expected profile and pixel format.
- [ ] A test import in the receiving editor plays with the correct frame size, rate and audio.
