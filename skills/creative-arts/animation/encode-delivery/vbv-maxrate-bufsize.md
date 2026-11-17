---
id: creative-arts.animation.encode-delivery.vbv-maxrate-bufsize
name: vbv-maxrate-bufsize
category: creative-arts
field: animation
product: encode-delivery
tags: [vbv, rate-control, maxrate, bufsize, capped-crf, ffmpeg, libx264, streaming, broadcast, peak-bitrate]
level: advanced
status: verified
description: "Cap peak bitrate with VBV (-maxrate/-bufsize) for streaming and broadcast encodes: capped CRF, buffer sizing, HRD signalling and verification."
sources:
  - https://trac.ffmpeg.org/wiki/Limiting%20the%20output%20bitrate
  - https://trac.ffmpeg.org/wiki/Encode/H.264
  - https://ffmpeg.org/ffmpeg-codecs.html#libx264_002c-libx264rgb
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# VBV: maxrate and bufsize

**Goal:** stop bitrate spikes that make a player stall or a broadcast/streaming validator reject
the file. The Video Buffering Verifier models a decoder buffer of `bufsize` bits filled at
`maxrate`; the encoder may not produce a stream that overflows it.

## Capped CRF (best default for streaming renditions)

```bash
ffmpeg -i master.mov -c:v libx264 -preset slow -crf 20 -maxrate 6M -bufsize 12M \
  -pix_fmt yuv420p -g 48 -keyint_min 48 -sc_threshold 0 -c:a aac -b:a 128k out.mp4
```

Quality targeted by CRF in easy scenes; the encoder raises the CRF when the output would exceed `-maxrate`. libx264 does not strictly control the maximum rate (FFmpeg wiki); use two-pass for tighter control.

## Constrained ABR (spec names an average and a peak)

```bash
ffmpeg -i master.mov -c:v libx264 -b:v 5M -maxrate 7.5M -bufsize 10M -pass 2 ...
```

## Sizing bufsize

- The FFmpeg wiki suggests starting with `-bufsize` equal to (or even half of) the `-b:v` value and increasing it until the bitrate varies too much, then backing off. A smaller buffer lowers variation but too small a buffer degrades quality.
- Its capped-CRF example uses `-crf 23 -maxrate 1M -bufsize 2M`.
- Spec values win: when a delivery spec or device profile states a buffer size, use it.

## HRD signalling

For broadcast/IPTV that checks conformance, add `-x264-params nal-hrd=vbr`, or `nal-hrd=cbr` with matching `-b:v`, `-minrate` and `-maxrate` as in the FFmpeg wiki's MPEG-TS example. Plain MP4 VOD does not normally need it.

## Gotchas

- ffmpeg documents `-maxrate` as requiring `-bufsize`; set both.
- VBV constrains the video the encoder writes; budget audio inside a total cap.
- Codec level limits also cap bitrate (see the level table in the H.264 standard). Set `-level:v` when a device list demands it.

## Verify

Plot or list per-second bitrate and look at the peak:

```bash
ffprobe -v error -select_streams v:0 -show_entries packet=pts_time,size -of csv=p=0 out.mp4 \
 | awk -F, '{s=int($1); b[s]+=$2*8} END {for (k in b) if (b[k]>m) m=b[k]; print "peak bps", m}'
```

The one-second peak should sit near `maxrate` and never far above it.

## Checked

2026-10-28. Confirmed: ffmpeg `maxrate` requires `bufsize` (ffmpeg-codecs); the FFmpeg wiki pages on H.264 and 'Limiting the output bitrate' (capped CRF example, bufsize guidance, `nal-hrd=cbr` MPEG-TS example); libx264 `nal-hrd` option. Removed: bufsize 2x and 1x rules, the 0.5x claim, the libx264-ignores-maxrate warning claim, the muxer audio-burst claim, the level 4.1 50 Mbps figure (it is not correct for High profile).

2026-11-01 run check: the capped-CRF command ran; the constrained-ABR options `-b:v 5M -maxrate 7.5M -bufsize 10M` ran (one pass, together with `-x264-params nal-hrd=vbr`); `-x264-params nal-hrd=vbr` and `nal-hrd=cbr` (MPEG-TS, `-minrate`/`-maxrate` equal to `-b:v`) ran; `-level:v 4.1` ran; the per-second peak `awk` pipeline from Verify ran and printed `peak bps` (about 1.06 Mb/s for a low-complexity clip well under its 6 Mb/s cap, so it shows the command works, not that the cap binds).

Method: commands run with ffmpeg 8.0.1 (Windows build) on synthetic lavfi inputs, plus the FFmpeg wiki for the bufsize guidance.
