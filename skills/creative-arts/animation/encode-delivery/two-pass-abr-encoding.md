---
id: creative-arts.animation.encode-delivery.two-pass-abr-encoding
name: two-pass-abr-encoding
category: creative-arts
field: animation
product: encode-delivery
tags: [two-pass, rate-control, abr, average-bitrate, ffmpeg, libx264, libx265, file-size, bitrate-budget, encode]
level: practitioner
status: verified
description: "Two-pass average-bitrate encodes in ffmpeg to hit a target bitrate or file size exactly: pass logs, null output, size arithmetic and pitfalls."
sources:
  - https://trac.ffmpeg.org/wiki/Encode/H.264#twopass
  - https://trac.ffmpeg.org/wiki/Encode/H.265#Two-PassEncoding
  - https://ffmpeg.org/ffmpeg.html#Video-Options
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Two-pass ABR encoding

**Goal:** hit a named average bitrate or file size while spending bits where the picture needs
them. Use when a spec says "10 Mbps H.264" or "under 2 GB", or a festival portal caps size.
For quality-targeted masters use CRF instead
(`creative-arts.animation.encode-delivery.crf-quality-targeting`).

## Bitrate from a size budget

```
video_kbps = (target_MB * 8192 / duration_s) - audio_kbps
```

Example: 22 min (1320 s) episode under 1500 MB with 320 kbps audio:
1500 * 8192 / 1320 = 9309 kbps total, minus 320 = ~8990 kbps video. Leave a margin for container
overhead: use `-b:v 8700k`.

## x264 two-pass

```bash
ffmpeg -y -i master.mov -c:v libx264 -preset slow -b:v 8700k -pass 1 \
  -passlogfile ep101 -pix_fmt yuv420p -an -f null /dev/null          # NUL on Windows cmd
ffmpeg -i master.mov -c:v libx264 -preset slow -b:v 8700k -pass 2 \
  -passlogfile ep101 -pix_fmt yuv420p -c:a aac -b:a 320k -movflags +faststart ep101.mp4
```

- Pass 1 writes `ep101-0.log` (the manual: PREFIX-N.log) and any encoder side files; pass 2 reads them. Keep the same
  preset, resolution, filters and frame rate in both passes or the stats do not line up.
- `-an -f null` on pass 1 skips writing a real file.
- Give both passes the same `-pix_fmt`. With a 10-bit ProRes master and `-pix_fmt yuv420p` only on pass 2, pass 2 failed with `different bitdepth setting than first pass (8 vs 10)`.
- Use a unique `-passlogfile` per job; two farm jobs in one folder with the default
  `ffmpeg2pass` name overwrite each other's stats.

## x265 two-pass

```bash
ffmpeg -y -i master.mov -c:v libx265 -b:v 6000k -x265-params pass=1:stats=ep101.x265 -an -f null /dev/null
ffmpeg -i master.mov -c:v libx265 -b:v 6000k -x265-params pass=2:stats=ep101.x265 -tag:v hvc1 -c:a aac out.mp4
```

`-tag:v hvc1` sets the `hvc1` HEVC sample entry.

## When a cap is also required

Two-pass ABR controls the average only; peaks can still exceed a player buffer. If the spec
also names a peak (e.g. "max 15 Mbps"), add `-maxrate 15M -bufsize 30M` to pass 2 (see
`creative-arts.animation.encode-delivery.vbv-maxrate-bufsize`).

## Gotchas

- Too low a bitrate shows as banding and noise around outlines. Check gradients.
- Changing anything between passes (scaling filter added only in pass 2) silently degrades.
- Pass logs left in the render folder confuse the next run; delete them after success.

## Verify

```bash
ffprobe -v error -show_entries format=bit_rate,size,duration -of default=nw=1 ep101.mp4
```

Overall bitrate close to the target and size under the cap.

## Checked

2026-10-28. Confirmed: ffmpeg `-pass`, `-passlogfile` with default prefix `ffmpeg2pass` and file name PREFIX-N.log (ffmpeg manual); the FFmpeg H.264 and H.265 wikis' two-pass and capped-rate examples; arithmetic of the size-budget example (1500 x 8192 / 1320 = 9309 kbps total, 8989 kbps video). Removed: the mbtree file name, the 2-3% overhead figure, the garbage-quality and Apple-player claims, the mosquito-noise claim.

2026-11-01 run check: the x264 two-pass pair ran (after adding `-pix_fmt` to pass 1) and left `ep101-0.log` plus `ep101-0.log.mbtree`; an 800 kb/s target gave 959 kb/s overall on a short synthetic clip; the capped pass 2 (`-maxrate`/`-bufsize`) ran; the x265 pair with `pass=1:stats=` / `pass=2:stats=` and `-tag:v hvc1` ran. Fixed: pass 1 without `-pix_fmt` broke pass 2 for a 10-bit source.

Method: commands run with ffmpeg 8.0.1 (Windows build) on synthetic lavfi inputs, plus the ffmpeg manual for `-pass` and `-passlogfile`.
